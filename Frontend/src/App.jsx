import { useState } from "react";

function App() {
  const [status, setStatus] = useState("Upload a video 🎥");
  const [frameInfo, setFrameInfo] = useState({ processed: 0, total: 0, percent: 0 });
  const [videoURL, setVideoURL] = useState(null);
  const [vehicles, setVehicles] = useState([]);
  const [error, setError] = useState(null);

  const speakSafeTime = (time, lang = "en-IN") => {
    const msg =
      lang === "hi-IN"
        ? `आप ${time} सेकंड में सुरक्षित रूप से सड़क पार कर सकते हैं`
        : `You can safely cross the road within ${time} seconds`;

    const u = new SpeechSynthesisUtterance(msg);
    u.lang = lang;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(u);
  };

  const uploadVideo = async (file) => {
    setStatus("Processing video… 🚦");
    setFrameInfo({ processed: 0, total: 0, percent: 0 });
    setVehicles([]);
    setVideoURL(null);
    setError(null);

    const fd = new FormData();
    fd.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/detect-video", {
      method: "POST",
      body: fd,
    });

    const { video_id } = await res.json();

    let maxPercent = 0;

    const interval = setInterval(async () => {
      const p = await fetch(`http://127.0.0.1:8000/progress/${video_id}`);
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
        const incoming = Object.entries(
          data.risk_assessment.vehicle_speeds || {}
        ).map(([id, speed]) => {
          const distance =
            data.risk_assessment.vehicle_distances?.[id] ?? 50;

          const crossingTime = Math.max(
            2,
            (distance / (speed / 3.6)).toFixed(1)
          );

          return { id, speed, distance, crossingTime };
        });

        setVehicles(incoming);
      }

      if (data.status === "completed") {
        clearInterval(interval);
        setStatus("Processing complete ✅");
        setVideoURL(data.video_url);
      }
    }, 800);
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
        🚸 Cross Wisely
      </h1>

      <p style={{ textAlign: "center", maxWidth: 700, margin: "0 auto", color: "#ccc" }}>
        AI-powered pedestrian crossing system that calculates safe road-crossing
        time using real-time vehicle speed and distance.
      </p>

      {/* UPLOAD */}
      <div style={{ textAlign: "center", marginTop: 20 }}>
        <input type="file" accept="video/*" onChange={(e) => uploadVideo(e.target.files[0])} />
        <p style={{ marginTop: 10, fontWeight: "bold" }}>{status}</p>
      </div>

      {/* FRAME PROGRESS (TABLE STYLE) */}
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
          <h3 style={{ color: "#FFB400", marginBottom: 10 }}>
            🎞️ Video Processing Status
          </h3>

          <table width="100%" style={{ borderCollapse: "collapse" }}>
            <tbody>
              <tr>
                <td width="30%">Frames</td>
                <td>
                  {frameInfo.processed} / {frameInfo.total}
                </td>
              </tr>
              <tr>
                <td>Progress</td>
                <td>{frameInfo.percent}%</td>
              </tr>
              <tr>
                <td colSpan="2">
                  <div
                    style={{
                      width: "100%",
                      height: 16,
                      background: "#555",
                      borderRadius: 10,
                      marginTop: 6,
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
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      )}

      {/* SAFE CROSSING TABLE */}
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
        <h3 style={{ color: "#FFB400" }}>📝 Pedestrian Safe Crossing (Live)</h3>

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
                    <b>{v.crossingTime} sec</b>
                    <br />
                    <button onClick={() => speakSafeTime(v.crossingTime, "en-IN")}>
                      🔊 EN
                    </button>
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

      {/* DOWNLOAD */}
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
