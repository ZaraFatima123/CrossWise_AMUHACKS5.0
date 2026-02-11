# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# from ultralytics import YOLO
# from PIL import Image
# import io

# # ------------------ App Init ------------------
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # Vite frontend
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ------------------ Load YOLO Model ------------------
# model = YOLO("yolov8n.pt")

# # ------------------ Root ------------------
# @app.get("/")
# def root():
#     return {"status": "Backend running 🚦"}

# # ------------------ Detection API ------------------
# @app.post("/detect")
# async def detect(file: UploadFile = File(...)):
#     image_bytes = await file.read()
#     image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

#     results = model(image)

#     detections = []

#     for box in results[0].boxes:
#         cls_id = int(box.cls[0])
#         cls_name = results[0].names[cls_id]
#         conf = float(box.conf[0])
#         x1, y1, x2, y2 = box.xyxy[0].tolist()

#         # 🚦 Color logic
#         if cls_name == "person":
#             color = "green"
#             category = "human"
#         else:
#             color = "red"
#             category = "vehicle_or_object"

#         detections.append({
#             "class": cls_name,
#             "confidence": round(conf, 2),
#             "bbox": [x1, y1, x2, y2],
#             "color": color,
#             "category": category
#         })

#     return {"detections": detections}

# 2nd code:
# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# from ultralytics import YOLO
# from PIL import Image
# import io

# # ------------------ App Init ------------------
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # Vite frontend
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ------------------ Load YOLO Model ------------------
# model = YOLO("yolov8n.pt")

# # ------------------ Root ------------------
# @app.get("/")
# def root():
#     return {"status": "Backend running 🚦"}

# # ------------------ Detection API ------------------
# @app.post("/detect")
# async def detect(file: UploadFile = File(...)):
#     image_bytes = await file.read()
#     image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

#     results = model(image)

#     detections = []

#     for box in results[0].boxes:
#         cls_id = int(box.cls[0])
#         cls_name = results[0].names[cls_id]
#         conf = float(box.conf[0])
#         x1, y1, x2, y2 = box.xyxy[0].tolist()

#         # 🚦 Color logic
#         if cls_name == "person":
#             color = "green"
#             category = "human"
#             thickness = 5  # thicker for humans
#         else:
#             color = "red"
#             category = "vehicle_or_object"
#             thickness = 7  # thicker for vehicles

#         detections.append({
#             "class": cls_name,
#             "confidence": round(conf, 2),
#             "bbox": [x1, y1, x2, y2],
#             "color": color,
#             "category": category,
#             "thickness": thickness  # <-- Added thickness here
#         })

#     return {"detections": detections}

# 2nd code:
# import asyncio
# from concurrent.futures import ThreadPoolExecutor

# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from fastapi.staticfiles import StaticFiles

# from ultralytics import YOLO
# import cv2
# import os
# import uuid
# import shutil

# # ------------------ APP INIT ------------------
# app = FastAPI(title="YOLO Video Detection API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ------------------ DIRS ------------------
# UPLOAD_DIR = "uploads"
# OUTPUT_DIR = "outputs"
# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # ------------------ STATIC FILES ------------------
# app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")

# # ------------------ MODEL ------------------
# model = YOLO("yolov8x.pt")

# # ------------------ EXECUTOR ------------------
# executor = ThreadPoolExecutor(max_workers=1)

# # ------------------ ROOT ------------------
# @app.get("/")
# def root():
#     return {"status": "Backend running 🚦"}

# # ------------------ VIDEO PROCESSOR (SYNC) ------------------
# def process_video(input_path: str, output_path: str):
#     cap = cv2.VideoCapture(input_path)

#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = cap.get(cv2.CAP_PROP_FPS)

#     out = cv2.VideoWriter(
#         output_path,
#         cv2.VideoWriter_fourcc(*"mp4v"),
#         fps,
#         (width, height),
#     )

#     frame_count = 0

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame_count += 1
#         if frame_count % 30 == 0:
#             print(f"Processing frame {frame_count}")

#         results = model(frame, verbose=False)[0]

#         for box in results.boxes:
#             cls_id = int(box.cls[0])
#             cls_name = results.names[cls_id]
#             conf = float(box.conf[0])
#             x1, y1, x2, y2 = map(int, box.xyxy[0])

#             if cls_name == "person":
#                 color = (0, 255, 0)
#                 thickness = 4
#             else:
#                 color = (0, 0, 255)
#                 thickness = 6

#             cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
#             cv2.putText(
#                 frame,
#                 f"{cls_name} {conf:.2f}",
#                 (x1, y1 - 8),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.6,
#                 color,
#                 2,
#             )

#         out.write(frame)

#     cap.release()
#     out.release()
#     print("✅ Video processing finished")

# # ------------------ VIDEO DETECTION (ASYNC SAFE) ------------------
# @app.post("/detect-video")
# async def detect_video(file: UploadFile = File(...)):
#     uid = str(uuid.uuid4())
#     input_path = f"{UPLOAD_DIR}/{uid}_{file.filename}"
#     output_path = f"{OUTPUT_DIR}/{uid}_processed.mp4"

#     # Save uploaded file
#     with open(input_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     # Run heavy processing in background thread
#     loop = asyncio.get_event_loop()
#     await loop.run_in_executor(
#         executor,
#         process_video,
#         input_path,
#         output_path,
#     )

#     filename = os.path.basename(output_path)

#     return {
#         "video_url": f"http://127.0.0.1:8000/outputs/{filename}",
#         "download_url": f"http://127.0.0.1:8000/outputs/{filename}",
#     }

# # ------------------ DOWNLOAD (OPTIONAL) ------------------
# @app.get("/download/{video_name}")
# def download_video(video_name: str):
#     return FileResponse(
#         path=f"{OUTPUT_DIR}/{video_name}",
#         media_type="video/mp4",
#         filename=video_name,
#     )

# # 3rd code
# import asyncio
# from concurrent.futures import ThreadPoolExecutor
# from collections import defaultdict, deque
# import uuid
# import os
# import shutil

# import cv2
# import numpy as np
# import supervision as sv
# from ultralytics import YOLO

# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles

# # ------------------ APP INIT ------------------
# app = FastAPI(title="Cross Wisely – Smart Traffic AI")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ------------------ DIRS ------------------
# UPLOAD_DIR = "uploads"
# OUTPUT_DIR = "outputs"
# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")

# # ------------------ MODEL (CPU SAFE) ------------------
# model = YOLO("yolov8n.pt")  # CPU friendly

# executor = ThreadPoolExecutor(max_workers=1)
# video_progress = {}

# # ------------------ VIEW TRANSFORM ------------------
# SOURCE = np.array([
#     [1252, 787],
#     [2298, 803],
#     [5039, 2159],
#     [-550, 2159]
# ])

# TARGET = np.array([
#     [0, 0],
#     [24, 0],
#     [24, 249],
#     [0, 249]
# ])

# class ViewTransformer:
#     def __init__(self, source, target):
#         self.m = cv2.getPerspectiveTransform(
#             source.astype(np.float32),
#             target.astype(np.float32)
#         )

#     def transform_points(self, points):
#         if len(points) == 0:
#             return points
#         points = points.reshape(-1, 1, 2).astype(np.float32)
#         return cv2.perspectiveTransform(points, self.m).reshape(-1, 2)

# view_transformer = ViewTransformer(SOURCE, TARGET)

# # ------------------ VIDEO PROCESSOR ------------------
# def process_video(video_id, input_path, output_path):
#     video_info = sv.VideoInfo.from_video_path(input_path)
#     frame_gen = sv.get_video_frames_generator(input_path)

#     tracker = sv.ByteTrack(frame_rate=video_info.fps)
#     coordinates = defaultdict(lambda: deque(maxlen=video_info.fps))

#     video_progress[video_id] = {
#         "total_frames": video_info.total_frames,
#         "processed_frames": 0,
#         "status": "processing",
#     }

#     with sv.VideoSink(output_path, video_info) as sink:
#         for i, frame in enumerate(frame_gen):

#             result = model(frame, imgsz=1280, verbose=False)[0]
#             detections = sv.Detections.from_ultralytics(result)

#             detections = detections[detections.confidence > 0.3]
#             detections = detections.with_nms(0.5)
#             detections = tracker.update_with_detections(detections)

#             points = detections.get_anchors_coordinates(
#                 anchor=sv.Position.BOTTOM_CENTER
#             )
#             points = view_transformer.transform_points(points).astype(int)

#             for tid, (_, y) in zip(detections.tracker_id, points):
#                 coordinates[tid].append(y)

#             for box, tid in zip(detections.xyxy, detections.tracker_id):
#                 x1, y1, x2, y2 = map(int, box)

#                 if len(coordinates[tid]) > video_info.fps / 2:
#                     dist = abs(coordinates[tid][-1] - coordinates[tid][0])
#                     time = len(coordinates[tid]) / video_info.fps
#                     speed = int((dist / time) * 3.6)
#                     label = f"ID {tid} | {speed} km/h"
#                 else:
#                     label = f"ID {tid}"

#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
#                 cv2.putText(
#                     frame,
#                     label,
#                     (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.7,
#                     (0, 0, 0),
#                     2,
#                 )

#             sink.write_frame(frame)
#             video_progress[video_id]["processed_frames"] = i + 1

#     video_progress[video_id]["status"] = "completed"

# # ------------------ API ------------------
# @app.post("/detect-video")
# async def detect_video(file: UploadFile = File(...)):
#     video_id = str(uuid.uuid4())

#     input_path = f"{UPLOAD_DIR}/{video_id}_{file.filename}"
#     output_path = f"{OUTPUT_DIR}/{video_id}_processed.mp4"

#     with open(input_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     loop = asyncio.get_event_loop()
#     await loop.run_in_executor(
#         executor,
#         process_video,
#         video_id,
#         input_path,
#         output_path,
#     )

#     return {
#         "video_id": video_id,
#         "video_url": f"http://127.0.0.1:8000/outputs/{os.path.basename(output_path)}"
#     }

# @app.get("/progress/{video_id}")
# def progress(video_id: str):
#     return video_progress.get(video_id, {})

#working code#1
# import asyncio
# from concurrent.futures import ThreadPoolExecutor
# from collections import defaultdict, deque
# import uuid
# import os
# import shutil

# import cv2
# import numpy as np
# import supervision as sv
# from ultralytics import YOLO

# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles

# # ------------------ APP INIT ------------------
# app = FastAPI(title="Cross Wisely – Smart Traffic AI")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ------------------ DIRS ------------------
# UPLOAD_DIR = "uploads"
# OUTPUT_DIR = "outputs"
# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")

# # ------------------ MODEL ------------------
# model = YOLO("yolov8n.pt")  # CPU safe

# executor = ThreadPoolExecutor(max_workers=1)
# video_progress = {}

# # ------------------ VIEW TRANSFORM ------------------
# SOURCE = np.array([
#     [1252, 787],
#     [2298, 803],
#     [5039, 2159],
#     [-550, 2159]
# ])

# TARGET = np.array([
#     [0, 0],
#     [24, 0],
#     [24, 249],
#     [0, 249]
# ])

# class ViewTransformer:
#     def __init__(self, source, target):
#         self.m = cv2.getPerspectiveTransform(
#             source.astype(np.float32),
#             target.astype(np.float32)
#         )

#     def transform_points(self, points):
#         if len(points) == 0:
#             return points
#         points = points.reshape(-1, 1, 2).astype(np.float32)
#         return cv2.perspectiveTransform(points, self.m).reshape(-1, 2)

# view_transformer = ViewTransformer(SOURCE, TARGET)

# # ------------------ VIDEO PROCESSOR ------------------
# def process_video(video_id, input_path, output_path):
#     video_info = sv.VideoInfo.from_video_path(input_path)
#     frame_gen = sv.get_video_frames_generator(input_path)

#     tracker = sv.ByteTrack(frame_rate=video_info.fps)
#     coordinates = defaultdict(lambda: deque(maxlen=int(video_info.fps)))

#     video_progress[video_id] = {
#         "total_frames": video_info.total_frames,
#         "processed_frames": 0,
#         "status": "processing",
#         "video_url": None
#     }

#     with sv.VideoSink(output_path, video_info) as sink:
#         for i, frame in enumerate(frame_gen):

#             result = model(frame, imgsz=1280, verbose=False)[0]
#             detections = sv.Detections.from_ultralytics(result)

#             detections = detections[detections.confidence > 0.3]
#             detections = detections.with_nms(0.5)
#             detections = tracker.update_with_detections(detections)

#             points = detections.get_anchors_coordinates(
#                 anchor=sv.Position.BOTTOM_CENTER
#             )
#             points = view_transformer.transform_points(points).astype(int)

#             for tid, (_, y) in zip(detections.tracker_id, points):
#                 coordinates[tid].append(y)

#             for box, tid in zip(detections.xyxy, detections.tracker_id):
#                 x1, y1, x2, y2 = map(int, box)

#                 if len(coordinates[tid]) > video_info.fps / 2:
#                     dist = abs(coordinates[tid][-1] - coordinates[tid][0])
#                     time = len(coordinates[tid]) / video_info.fps
#                     speed = int((dist / time) * 3.6)
#                     label = f"ID {tid} | {speed} km/h"
#                 else:
#                     label = f"ID {tid}"

#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
#                 cv2.putText(
#                     frame,
#                     label,
#                     (x1, y1 - 8),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.7,
#                     (0, 0, 0),
#                     2
#                 )

#             sink.write_frame(frame)
#             video_progress[video_id]["processed_frames"] = i + 1

#     video_progress[video_id]["status"] = "completed"
#     video_progress[video_id]["video_url"] = (
#         f"http://127.0.0.1:8000/outputs/{os.path.basename(output_path)}"
#     )

# # ------------------ API ------------------
# @app.post("/detect-video")
# async def detect_video(file: UploadFile = File(...)):
#     video_id = str(uuid.uuid4())

#     input_path = f"{UPLOAD_DIR}/{video_id}_{file.filename}"
#     output_path = f"{OUTPUT_DIR}/{video_id}_processed.mp4"

#     with open(input_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     # 🔥 RUN IN BACKGROUND (DO NOT AWAIT)
#     loop = asyncio.get_event_loop()
#     loop.run_in_executor(
#         executor,
#         process_video,
#         video_id,
#         input_path,
#         output_path,
#     )

#     return {"video_id": video_id}

# @app.get("/progress/{video_id}")
# def progress(video_id: str):
#     return video_progress.get(video_id, {})

#4th:
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