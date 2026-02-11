// import { useRef, useState } from "react";

// function App() {
//   const canvasRef = useRef(null);
//   const imgRef = useRef(null);
//   const [status, setStatus] = useState("Upload an image");

//   const detectImage = async (file) => {
//     setStatus("Detecting... 🚦");

//     const formData = new FormData();
//     formData.append("file", file);

//     const res = await fetch("http://127.0.0.1:8000/detect", {
//       method: "POST",
//       body: formData,
//     });

//     const data = await res.json();
//     drawBoxes(data.detections);
//     setStatus("Detection complete ✅");
//   };

//   const drawBoxes = (detections) => {
//     const canvas = canvasRef.current;
//     const ctx = canvas.getContext("2d");
//     canvas.width = imgRef.current.width;
//     canvas.height = imgRef.current.height;

//     ctx.drawImage(imgRef.current, 0, 0);

//     detections.forEach((det) => {
//       const [x1, y1, x2, y2] = det.bbox;
//       ctx.strokeStyle = det.color;
//       // ctx.lineWidth = 3;
//       ctx.lineWidth = det.thickness; // use thickness from backend
//       ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

//       ctx.fillStyle = det.color;
//       ctx.font = "16px Arial";
//       ctx.fillText(
//         `${det.class} (${det.confidence})`,
//         x1,
//         y1 > 20 ? y1 - 5 : y1 + 20
//       );
//     });
//   };

//   return (
//     <div className="app">
//       <h1>🚸 Smart Zebra Crossing Detection</h1>
//       <p className="subtitle">
//         Green = Pedestrian | Red = Vehicle / Obstacle
//       </p>

//       <input
//         type="file"
//         accept="image/*"
//         onChange={(e) => {
//           const file = e.target.files[0];
//           imgRef.current.src = URL.createObjectURL(file);
//           imgRef.current.onload = () => detectImage(file);
//         }}
//       />

//       <div className="canvas-box">
//         <img ref={imgRef} alt="" hidden />
//         <canvas ref={canvasRef}></canvas>
//       </div>

//       <p className="status">{status}</p>
//     </div>
//   );
// }

// export default App;

// #new code

// import { useState } from "react";

// function App() {
//   const [status, setStatus] = useState("Upload a video 🎥");
//   const [videoURL, setVideoURL] = useState(null);
//   const [downloadURL, setDownloadURL] = useState(null);

//   const uploadVideo = async (file) => {
//     setStatus("Processing video... 🚦");

//     const formData = new FormData();
//     formData.append("file", file);

//     const res = await fetch("http://127.0.0.1:8000/detect-video", {
//       method: "POST",
//       body: formData,
//     });

//     const data = await res.json();

//     setVideoURL(data.video_url);
//     setDownloadURL(data.download_url);
//     setStatus("Processing complete ✅");
//   };

//   return (
//     <div style={{ textAlign: "center", padding: "30px" }}>
//       <h1>🚸 CrozzWizely – Video Detection</h1>

//       <input
//         type="file"
//         accept="video/*"
//         onChange={(e) => uploadVideo(e.target.files[0])}
//       />

//       <p>{status}</p>

//       {videoURL && (
//         <>
//           <video
//             src={videoURL}
//             controls
//             autoPlay
//             width="800"
//             style={{
//               marginTop: "20px",
//               borderRadius: "10px",
//               boxShadow: "0 0 10px rgba(0,0,0,0.4)"
//             }}
//           />

//           <br /><br />

//           <a
//             href={downloadURL}
//             download
//             style={{
//               padding: "10px 20px",
//               background: "#28a745",
//               color: "#fff",
//               textDecoration: "none",
//               borderRadius: "6px",
//               fontWeight: "bold"
//             }}
//           >
//             ⬇ Download Processed Video
//           </a>
//         </>
//       )}
//     </div>
//   );
// }

// export default App;


// import { useState } from "react";

// function App() {
//   const [status, setStatus] = useState("Upload a video 🎥");
//   const [videoURL, setVideoURL] = useState(null);
//   const [downloadURL, setDownloadURL] = useState(null);
//   const [frameInfo, setFrameInfo] = useState(null);

//   const uploadVideo = async (file) => {
//     setStatus("Processing video... 🚦");
//     setFrameInfo(null);

//     const formData = new FormData();
//     formData.append("file", file);

//     const res = await fetch("http://127.0.0.1:8000/detect-video", {
//       method: "POST",
//       body: formData,
//     });

//     const data = await res.json();

//     setVideoURL(data.video_url);
//     setDownloadURL(data.download_url);
//     setFrameInfo({
//       total: data.total_frames,
//       processed: data.processed_frames,
//     });

//     setStatus("Processing complete ✅");
//   };

//   return (
//     <div style={{ textAlign: "center", padding: "30px" }}>
//       <h1>🚸 CrozzWizely – Video Detection</h1>

//       <input
//         type="file"
//         accept="video/*"
//         onChange={(e) => uploadVideo(e.target.files[0])}
//       />

//       <p>{status}</p>

//       {frameInfo && (
//         <p style={{ fontWeight: "bold" }}>
//           🎞️ Frames Processed: {frameInfo.processed} / {frameInfo.total}
//         </p>
//       )}

//       {videoURL && (
//         <>
//           <video
//             src={videoURL}
//             controls
//             autoPlay
//             width="800"
//             style={{
//               marginTop: "20px",
//               borderRadius: "10px",
//               boxShadow: "0 0 10px rgba(0,0,0,0.4)",
//             }}
//           />

//           <br /><br />

//           <a
//             href={downloadURL}
//             download
//             style={{
//               padding: "10px 20px",
//               background: "#28a745",
//               color: "#fff",
//               textDecoration: "none",
//               borderRadius: "6px",
//               fontWeight: "bold",
//             }}
//           >
//             ⬇ Download Processed Video
//           </a>
//         </>
//       )}
//     </div>
//   );
// }

// export default App;

// #working
import { useState } from "react";

function App() {
  const [status, setStatus] = useState("Upload a video 🎥");
  const [videoURL, setVideoURL] = useState(null);
  const [frameInfo, setFrameInfo] = useState(null);

  const uploadVideo = async (file) => {
    setStatus("Processing video... 🚦");
    setVideoURL(null);
    setFrameInfo(null);

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/detect-video", {
      method: "POST",
      body: formData,
    });

    const { video_id } = await res.json();

    const interval = setInterval(async () => {
      const p = await fetch(`http://127.0.0.1:8000/progress/${video_id}`);
      const data = await p.json();

      if (data.total_frames) {
        setFrameInfo({
          processed: data.processed_frames,
          total: data.total_frames,
        });
      }

      if (data.status === "completed") {
        clearInterval(interval);
        setVideoURL(data.video_url);
        setStatus("Processing complete ✅");
      }
    }, 1000);
  };

  return (
    <div style={{ textAlign: "center", padding: "30px" }}>
      <h1>🚸 Cross Wisely – Smart Traffic AI</h1>

      <input
        type="file"
        accept="video/*"
        onChange={(e) => uploadVideo(e.target.files[0])}
      />

      <p>{status}</p>

      {frameInfo && (
        <p style={{ fontWeight: "bold" }}>
          🎞️ Frames Processed: {frameInfo.processed} / {frameInfo.total}
        </p>
      )}

      {videoURL && (
        <video
          src={videoURL}
          controls
          width="800"
          style={{
            marginTop: "20px",
            borderRadius: "10px",
            boxShadow: "0 0 10px rgba(0,0,0,0.4)",
          }}
        />
      )}
    </div>
  );
}

export default App;