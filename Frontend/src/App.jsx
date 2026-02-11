import { useState } from "react";

function App() {
  const [status, setStatus] = useState("Upload a video 🎥");
  const [frameInfo, setFrameInfo] = useState({
    processed: 0,
    total: 0,
    percent: 0,
  });
  const [videoURL, setVideoURL] = useState(null);
  const [vehicles, setVehicles] = useState([]);
  const [error, setError] = useState(null);

  // 🔊 Voice Output (English + Hindi)
  const speakSafeTime = (time, lang = "en-IN") => {
    if (!("speechSynthesis" in window)) return;

    const msg =
      lang === "hi-IN"
        ? `आप ${time} सेकंड में सुरक्षित रूप से सड़क पार कर सकते हैं`
        : `You can safely cross the road within ${time} seconds`;

    const u = new SpeechSynthesisUtterance(msg);
    u.lang = lang;
    u.rate = 0.9;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(u);
  };

  // 🎥 Upload + Poll Progress
  const uploadVideo = async (file) => {
    setStatus("Processing video… 🚦");
    setFrameInfo({ processed: 0, total: 0, percent: 0 });
    setVehicles([]);
    setVideoURL(null);
    setError(null);

    try {
      const fd = new FormData();
      fd.append("file", file);

      const res = await fetch("http://127.0.0.1:8000/detect-video", {
        method: "POST",
        body: fd,
      });

      if (!res.ok) throw new Error("Upload failed");

      const { video_id } = await res.json();
      let maxPercent = 0;

      const interval = setInterval(async () => {
        try {
          const p = await fetch(
            `http://127.0.0.1:8000/progress/${video_id}`
          );
          const data = await p.json();

          if (!data?.total_frames) return;

          const percent = Math.max(
            maxPercent,
            ((data.processed_frames / data.total_frames) * 100).toFixed(1)
          );
          maxPercent = percent;

          setFrameInfo({
            processed: data.processed_frames,
            total: data.total_frames,
            percent,
          });

          if (data.risk_assessment) {
            const list = Object.entries(
              data.risk_assessment.vehicle_speeds || {}
            ).map(([id, speed]) => {
              const distance =
                data.risk_assessment.vehicle_distances?.[id] ?? 0;

              const crossingTime =
                speed > 0
                  ? Math.max(2, (distance / (speed / 3.6)).toFixed(1))
                  : "-";

              return {
                id,
                speed: Math.round(speed),
                distance: distance.toFixed(1),
                crossingTime,
              };
            });

            setVehicles(list);
          }

          if (data.status === "completed") {
            clearInterval(interval);
            setStatus("Processing complete ✅");
            setVideoURL(data.video_url);
          }
        } catch {
          clearInterval(interval);
          setStatus("Failed ❌");
          setError("Backend error");
        }
      }, 800);
    } catch {
      setStatus("Failed ❌");
      setError("Upload failed");
    }
  };

  return (
    <div
      style={{
        background: "#1a2b3c",
        minHeight: "100vh",
        color: "#fff",
        padding: 30,
        fontFamily: "Segoe UI, sans-serif",
      }}
    >
      {/* HEADER */}
      <h1 style={{ color: "#FFB400", textAlign: "center" }}>
        🚸 Cross Wizely
      </h1>

      <p
        style={{
          textAlign: "center",
          maxWidth: 700,
          margin: "0 auto",
          color: "#ccc",
        }}
      >
        AI-powered pedestrian crossing system that dynamically calculates
        safe road-crossing windows using real-time vehicle speed and distance.
      </p>

      {/* UPLOAD */}
      <div style={{ textAlign: "center", marginTop: 20 }}>
        <input
          type="file"
          accept="video/*"
          onChange={(e) => uploadVideo(e.target.files[0])}
        />
        <p style={{ marginTop: 10, fontWeight: "bold" }}>{status}</p>
      </div>

      {/* 🎞️ FRAME PROGRESS */}
      {frameInfo.total > 0 && (
        <div
          style={{
            border: "1px solid #4CAF50",
            borderRadius: 8,
            padding: 15,
            maxWidth: 900,
            margin: "20px auto",
            background: "#233040",
          }}
        >
          <h3 style={{ color: "#FFB400" }}>
            🎞️ Video Processing Status
          </h3>

          <table width="100%">
            <tbody>
              <tr>
                <td>Frames Processed</td>
                <td>
                  {frameInfo.processed} / {frameInfo.total}
                </td>
              </tr>
              <tr>
                <td>Progress</td>
                <td>{frameInfo.percent}%</td>
              </tr>
            </tbody>
          </table>

          <div
            style={{
              width: "100%",
              height: 16,
              background: "#555",
              borderRadius: 10,
              marginTop: 8,
            }}
          >
            <div
              style={{
                width: `${frameInfo.percent}%`,
                height: "100%",
                background: "#4CAF50",
                borderRadius: 10,
                transition: "width 0.4s",
              }}
            />
          </div>
        </div>
      )}

      {/* 🚦 SAFE CROSSING TABLE */}
      <div
        style={{
          border: "1px solid #4CAF50",
          borderRadius: 10,
          padding: 15,
          maxWidth: 900,
          margin: "20px auto",
          background: "#233040",
        }}
      >
        <h3 style={{ color: "#FFB400" }}>
          📝 Pedestrian Safe Crossing (Live)
        </h3>

        {vehicles.length === 0 ? (
          <p style={{ color: "#aaa" }}>Waiting for vehicle detection…</p>
        ) : (
          <table width="100%" style={{ borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ borderBottom: "2px solid #4CAF50" }}>
                <th align="left">Vehicle ID</th>
                <th align="left">Speed (km/h)</th>
                <th align="left">Distance (m)</th>
                <th align="left">Safe Time</th>
              </tr>
            </thead>
            <tbody>
              {vehicles.map((v) => (
                <tr key={v.id} style={{ borderBottom: "1px solid #555" }}>
                  <td>{v.id}</td>
                  <td>{v.speed}</td>
                  <td>{v.distance}</td>
                  <td>
                    <strong>{v.crossingTime} sec</strong>
                    <br />
                    <button onClick={() => speakSafeTime(v.crossingTime, "en-IN")}>
                      🔊 EN
                    </button>{" "}
                    <button onClick={() => speakSafeTime(v.crossingTime, "hi-IN")}>
                      🔊 हिंदी
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* 🤟 Sign Language Placeholder */}
<div
  style={{
    border: "1px dashed #FFB400",
    borderRadius: 10,
    padding: 15,
    maxWidth: 900,
    margin: "20px auto",
    background: "#233040",
    textAlign: "center",
    color: "#FFB400",
    fontStyle: "italic",
  }}
>
  🤟 Sign Language Integration will be added soon!
</div>

      {/* ⬇️ DOWNLOAD */}
      {videoURL && (
        <div style={{ textAlign: "center", marginTop: 20 }}>
          <a
            href={`http://127.0.0.1:8000/download/${videoURL}`}
            download
            style={{
              padding: "10px 20px",
              background: "#4CAF50",
              color: "#fff",
              borderRadius: 6,
              textDecoration: "none",
              fontWeight: "bold",
            }}
          >
            ⬇️ Download Processed Video
          </a>
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default App;
