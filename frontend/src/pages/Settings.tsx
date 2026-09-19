import { useEffect, useState } from "react";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function Settings() {
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [aiStatus, setAiStatus] = useState("Checking...");
  const [databaseStatus, setDatabaseStatus] = useState("Checking...");

  useEffect(() => {
    checkSystemStatus();
  }, []);

  const checkSystemStatus = async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/system/status`
      );

      if (!response.ok) {
        throw new Error("Failed to get system status");
      }

      const data = await response.json();

      setBackendStatus(data.backend || "Unknown");
      setAiStatus(data.ai || "Unknown");
      setDatabaseStatus(data.database || "Unknown");
    } catch (error) {
      console.error(error);

      setBackendStatus("Offline");
      setAiStatus("Unknown");
      setDatabaseStatus("Unknown");
    }
  };

  return (
    <div>
      <div className="page-header">
        <h2>Settings</h2>

        <p>
          View and monitor ChronoMed system configuration.
        </p>
      </div>

      <div className="card">
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <div>
            <h3>System Status</h3>

            <p className="card-subtitle">
              Current status of ChronoMed services.
            </p>
          </div>

          <button
            className="primary-button"
            onClick={checkSystemStatus}
          >
            Refresh
          </button>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit, minmax(200px, 1fr))",
            gap: "15px",
            marginTop: "20px",
          }}
        >
          <div
            style={{
              padding: "20px",
              border: "1px solid #e5e7eb",
              borderRadius: "10px",
            }}
          >
            <strong>Backend</strong>

            <p style={{ marginTop: "8px" }}>
              {backendStatus}
            </p>
          </div>

          <div
            style={{
              padding: "20px",
              border: "1px solid #e5e7eb",
              borderRadius: "10px",
            }}
          >
            <strong>AI Service</strong>

            <p style={{ marginTop: "8px" }}>
              {aiStatus}
            </p>
          </div>

          <div
            style={{
              padding: "20px",
              border: "1px solid #e5e7eb",
              borderRadius: "10px",
            }}
          >
            <strong>Database</strong>

            <p style={{ marginTop: "8px" }}>
              {databaseStatus}
            </p>
          </div>
        </div>
      </div>

      <div className="card" style={{ marginTop: "20px" }}>
        <h3>API Configuration</h3>

        <p className="card-subtitle">
          Backend API endpoint currently used by the frontend.
        </p>

        <div
          style={{
            marginTop: "15px",
            padding: "15px",
            background: "#f8fafc",
            borderRadius: "8px",
            wordBreak: "break-word",
          }}
        >
          {API_BASE_URL}
        </div>
      </div>
    </div>
  );
}

export default Settings;