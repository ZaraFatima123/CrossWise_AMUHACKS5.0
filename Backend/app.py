
import asyncio
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, deque
import uuid, os, shutil

import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ------------------ APP ------------------
app = FastAPI(title="Cross Wisely – Smart Traffic AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")

# ------------------ MODEL ------------------
model = YOLO("yolov8n.pt")  # CPU safe
executor = ThreadPoolExecutor(max_workers=1)
video_progress = {}

# ------------------ VIEW TRANSFORM ------------------
SOURCE = np.array([[1252, 787], [2298, 803], [5039, 2159], [-550, 2159]])
TARGET = np.array([[0, 0], [24, 0], [24, 249], [0, 249]])  # meters

class ViewTransformer:
    def __init__(self, source, target):
        self.m = cv2.getPerspectiveTransform(
            source.astype(np.float32),
            target.astype(np.float32)
        )

    def transform(self, pts):
        if len(pts) == 0:
            return pts
        pts = pts.reshape(-1, 1, 2).astype(np.float32)
        return cv2.perspectiveTransform(pts, self.m).reshape(-1, 2)

view = ViewTransformer(SOURCE, TARGET)

# ------------------ VIDEO PROCESSOR ------------------
def process_video(video_id, input_path, output_path):
    info = sv.VideoInfo.from_video_path(input_path)
    frames = sv.get_video_frames_generator(input_path)

    tracker = sv.ByteTrack(frame_rate=info.fps)
    tracks = defaultdict(lambda: deque(maxlen=int(info.fps)))
    last_speed = {}

    video_progress[video_id] = {
        "total_frames": int(info.total_frames),
        "processed_frames": 0,
        "status": "processing",
        "video_url": None,
        "risk_assessment": None,
    }

    with sv.VideoSink(output_path, info) as sink:
        for i, frame in enumerate(frames):
            result = model(frame, imgsz=1280, verbose=False)[0]
            det = sv.Detections.from_ultralytics(result)
            det = det[det.confidence > 0.3]
            det = det.with_nms(0.5)
            det = tracker.update_with_detections(det)

            pts = det.get_anchors_coordinates(anchor=sv.Position.BOTTOM_CENTER)
            pts = view.transform(pts)

            speeds = {}
            distances = {}

            for tid, (_, y) in zip(det.tracker_id, pts):
                tracks[int(tid)].append(float(y))

            for box, tid in zip(det.xyxy, det.tracker_id):
                tid = int(tid)
                x1, y1, x2, y2 = map(int, box)

                if len(tracks[tid]) > info.fps / 2:
                    dy = abs(tracks[tid][-1] - tracks[tid][0])
                    t = len(tracks[tid]) / info.fps

                    speed_mps = dy / max(t, 0.1)
                    speed_kmph = speed_mps * 3.6
                else:
                    speed_kmph = last_speed.get(tid, 0)

                # 🔒 Clamp & round speed
                speed_kmph = min(speed_kmph, 120.0)
                speed_kmph = round(speed_kmph, 1)
                last_speed[tid] = speed_kmph

                # 📏 Distance using s = v × t (2.5s lookahead)
                distance_m = round((speed_kmph / 3.6) * 2.5, 2)

                speeds[tid] = speed_kmph
                distances[tid] = distance_m

                label = f"ID {tid} | {speed_kmph} km/h"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

            video_progress[video_id]["risk_assessment"] = {
                "vehicle_speeds": {int(k): float(v) for k, v in speeds.items()},
                "vehicle_distances": {int(k): float(v) for k, v in distances.items()},
            }

            sink.write_frame(frame)
            video_progress[video_id]["processed_frames"] = i + 1

    video_progress[video_id]["status"] = "completed"
    video_progress[video_id]["video_url"] = os.path.basename(output_path)

# ------------------ API ------------------
@app.post("/detect-video")
async def detect_video(file: UploadFile = File(...)):
    vid = str(uuid.uuid4())
    ip = f"{UPLOAD_DIR}/{vid}_{file.filename}"
    op = f"{OUTPUT_DIR}/{vid}_processed.mp4"

    with open(ip, "wb") as f:
        shutil.copyfileobj(file.file, f)

    asyncio.get_event_loop().run_in_executor(
        executor, process_video, vid, ip, op
    )

    return {"video_id": vid}

@app.get("/progress/{video_id}")
def progress(video_id: str):
    return video_progress.get(video_id, {})

@app.get("/download/{video_name}")
def download(video_name: str):
    return FileResponse(
        os.path.join(OUTPUT_DIR, video_name),
        filename=video_name
    )
