🚸 Cross Wizely – Smart Traffic AI

Cross Wisely is an AI-powered pedestrian crossing system that dynamically calculates safe road-crossing windows using real-time vehicle speed and distance. This system aims to replace traditional traffic signals and zebra crossings with a smarter, risk-assessed solution for pedestrians.

🌟 Features:

Real-time Vehicle Detection using YOLOv8

Pedestrian Safe Crossing Time calculated from vehicle speed and distance

Frame-by-frame Progress Tracking of video processing

Multi-language Voice Alerts: English and Hindi for safe crossing time

Processed Video Download after AI analysis

Sign Language Integration Placeholder (Coming Soon)

Professional UI with tables, borders, and progress bars

🛠️ Technologies Used

Backend:

FastAPI (Python)

YOLOv8 (Ultralytics) for object detection

Supervision library for tracking and video processing

Frontend:

React.js

Real-time UI updates with state hooks

Frame-by-frame progress bar

Voice synthesis for crossing guidance

Other Tools:

ThreadPoolExecutor for async video processing

CORS middleware for frontend-backend communication

⚡ Usage
Backend (Python – FastAPI)

Clone the repository:

git clone https://github.com/your-username/cross-wisely.git
cd cross-wisely

Install dependencies:

pip install -r requirements.txt

Run the backend server:

uvicorn app:app --reload
Frontend (React.js)

Navigate to the frontend folder (if separate) and install dependencies:

npm install

Start the React app:

npm start

Open in browser:

http://localhost:3000
🖼️ UI Overview

Header: Project name and description

Upload Section: Upload your video file

Frame Progress: Live frame processing with percentage bar

Vehicle Table: Shows vehicle ID, speed, distance, and safe crossing time

Voice Alerts: Play safe crossing time in English or Hindi

Download: Processed video download

Sign Language Placeholder: Coming soon!

Future Improvements

Sign Language Integration for safe crossing guidance

Improved vehicle tracking and risk prediction

Mobile-friendly responsive UI

Support for multiple cameras and intersections
