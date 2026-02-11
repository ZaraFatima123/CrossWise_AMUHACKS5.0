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
model = YOLO("yolov8n.pt")  # keep CPU-safe
executor = ThreadPoolExecutor(max_workers=1)
video_progress = {}

# ------------------ VIEW TRANSFORM ------------------
SOURCE = np.array([
    [1252, 787],
    [2298, 803],
    [5039, 2159],
    [-550, 2159]
])

TARGET = np.array([
    [0, 0],
    [24, 0],
    [24, 249],
    [0, 249]
])

class ViewTransformer:
    def __init__(self, source, target):
        self.m = cv2.getPerspectiveTransform(
            source.astype(np.float32),
            target.astype(np.float32)
        )

    def transform_points(self, points):
        if len(points) == 0:
            return points
        points = points.reshape(-1, 1, 2).astype(np.float32)
        return cv2.perspectiveTransform(points, self.m).reshape(-1, 2)

view_transformer = ViewTransformer(SOURCE, TARGET)

# ------------------ VIDEO PROCESSOR ------------------
def process_video(video_id, input_path, output_path):
    video_info = sv.VideoInfo.from_video_path(input_path)
    frames = sv.get_video_frames_generator(input_path)

    tracker = sv.ByteTrack(frame_rate=video_info.fps)
    coordinates = defaultdict(lambda: deque(maxlen=int(video_info.fps)))

    video_progress[video_id] = {
        "total_frames": video_info.total_frames,
        "processed_frames": 0,
        "status": "processing",
        "video_url": None,
    }

    with sv.VideoSink(output_path, video_info) as sink:
        for i, frame in enumerate(frames):

            result = model(frame, imgsz=1280, verbose=False)[0]
            detections = sv.Detections.from_ultralytics(result)
            detections = detections[detections.confidence > 0.3]
            detections = detections.with_nms(0.5)
            detections = tracker.update_with_detections(detections)

            points = detections.get_anchors_coordinates(
                anchor=sv.Position.BOTTOM_CENTER
            )
            points = view_transformer.transform_points(points).astype(int)

            for tid, (_, y) in zip(detections.tracker_id, points):
                coordinates[tid].append(y)

            for box, tid in zip(detections.xyxy, detections.tracker_id):
                x1, y1, x2, y2 = map(int, box)

                if len(coordinates[tid]) > video_info.fps / 2:
                    dist = abs(coordinates[tid][-1] - coordinates[tid][0])
                    time = len(coordinates[tid]) / video_info.fps
                    speed = int((dist / time) * 3.6)
                    label = f"ID {tid} | {speed} km/h"
                else:
                    label = f"ID {tid}"

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 5)
                cv2.putText(frame, label, (x1, y1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)

            sink.write_frame(frame)
            video_progress[video_id]["processed_frames"] = i + 1

    video_progress[video_id]["status"] = "completed"
    video_progress[video_id]["video_url"] = (
        f"http://127.0.0.1:8000/outputs/{os.path.basename(output_path)}"
    )

# ------------------ API ------------------
@app.post("/detect-video")
async def detect_video(file: UploadFile = File(...)):
    video_id = str(uuid.uuid4())
    input_path = f"{UPLOAD_DIR}/{video_id}_{file.filename}"
    output_path = f"{OUTPUT_DIR}/{video_id}_processed.mp4"

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    asyncio.get_event_loop().run_in_executor(
        executor, process_video, video_id, input_path, output_path
    )

    return {"video_id": video_id}

@app.get("/progress/{video_id}")
def get_progress(video_id: str):
    return video_progress.get(video_id, {})
