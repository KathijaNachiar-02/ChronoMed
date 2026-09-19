import { useEffect, useState } from "react";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function WhatChanged() {
  const [changes, setChanges] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    loadChanges();
  }, []);

  const loadChanges = async () => {
    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/changes`);

      if (!response.ok) {
        throw new Error("Failed to load changes");
      }

      const data = await response.json();
      setChanges(data);
    } catch (error) {
      console.error(error);
      setMessage("Could not load changes.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h2>What Changed</h2>

        <p>
          Track important changes detected across patient records.
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
            <h3>Record Changes</h3>

            <p className="card-subtitle">
              Review changes identified between medical records.
            </p>
          </div>

          <button
            className="primary-button"
            onClick={loadChanges}
          >
            Refresh
          </button>
        </div>

        <div style={{ marginTop: "20px" }}>
          {loading && <p>Loading changes...</p>}

          {!loading && message && <p>{message}</p>}

          {!loading && !message && changes.length === 0 && (
            <div
              style={{
                padding: "30px",
                textAlign: "center",
                background: "#f8fafc",
                borderRadius: "10px",
              }}
            >
              <div style={{ fontSize: "35px" }}>↕</div>

              <h3 style={{ marginTop: "10px" }}>
                No changes found
              </h3>

              <p style={{ marginTop: "5px" }}>
                No record changes are currently available for review.
              </p>
            </div>
          )}

          {!loading && !message && changes.length > 0 && (
            <div>
              {changes.map((change) => (
                <div
                  key={change.id}
                  style={{
                    padding: "18px",
                    marginBottom: "15px",
                    border: "1px solid #e5e7eb",
                    borderRadius: "10px",
                  }}
                >
                  <h3>
                    {change.title || "Record Change"}
                  </h3>

                  <p style={{ marginTop: "8px" }}>
                    <strong>Patient:</strong>{" "}
                    {change.patient_id || "Unknown"}
                  </p>

                  <p style={{ marginTop: "5px" }}>
                    <strong>Status:</strong>{" "}
                    {change.status || "Detected"}
                  </p>

                  {change.description && (
                    <p style={{ marginTop: "10px" }}>
                      {change.description}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default WhatChanged;