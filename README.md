# 🚸 Cross Wizely – Smart Traffic AI

**Cross Wizely** is an AI-powered pedestrian crossing system that dynamically calculates safe road-crossing windows using real-time vehicle speed and distance. This system aims to replace traditional traffic signals and zebra crossings with a smarter, risk-assessed solution for pedestrians.

![image alt](https://github.com/ZaraFatima123/CrossWise_AMUHACKS5.0/blob/beff768d9dac78faa30b67cf6c4bf676d3563d1f/WhatsApp%20Image%202026-02-12%20at%201.10.12%20AM.jpeg)
![image alt](https://github.com/ZaraFatima123/CrossWise_AMUHACKS5.0/blob/904451662644f75d9f30b978a277f5eb818dea98/WhatsApp%20Image%202026-02-12%20at%201.23.54%20AM.jpeg)


---

## 🌟 Features

- **Real-time Vehicle Detection** using YOLOv8  
- **Pedestrian Safe Crossing Time** calculated from vehicle speed and distance  
- **Frame-by-frame Progress Tracking** of video processing  
- **Multi-language Voice Alerts**: English and Hindi for safe crossing time  
- **Processed Video Download** after AI analysis  
- **Sign Language Integration Placeholder** (Coming Soon)  
- **Professional UI** with tables, borders, and progress bars  

---

## 🛠️ Technologies Used

**Backend:**  
- FastAPI (Python)  
- YOLOv8 (Ultralytics) for object detection  
- Supervision library for tracking and video processing  

**Frontend:**  
- React.js  
- Real-time UI updates with state hooks  
- Frame-by-frame progress bar  
- Voice synthesis for crossing guidance  

**Other Tools:**  
- ThreadPoolExecutor for async video processing  
- CORS middleware for frontend-backend communication  

---

## ⚡ Usage

### Backend (Python – FastAPI)
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/cross-wisely.git
   cd cross-wisely
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
3. Run the backend server:
   ```bash
    uvicorn app:app --reload
4. Frontend Setup (React)

Navigate to frontend folder:

```bash
cd Frontend
```

Install dependencies:

```bash
npm install
```

Run development server:

```bash
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---


## 🖥️ UI Overview


- **Header:** Project name and description
- **Upload Section:** Upload your video file
- **Frame Progress:** Live frame processing with percentage bar
- **Vehicle Table:** Shows vehicle ID, speed, distance, and safe crossing time
- **Voice Alerts:** Play safe crossing time in English or Hindi
- **Download:** Processed video download
- **Sign Language Placeholder:** Coming soon

---

## 🚀 Future Improvements

- Sign Language Integration for safe crossing guidance
- Improved vehicle tracking and risk prediction
- Mobile-friendly responsive UI
- Support for multiple cameras and intersections




