import { useEffect, useState } from "react";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function Conflicts() {
  const [conflicts, setConflicts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    loadConflicts();
  }, []);

  const loadConflicts = async () => {
    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/conflicts`);

      if (!response.ok) {
        throw new Error("Failed to load conflicts");
      }

      const data = await response.json();

      setConflicts(data);
    } catch (error) {
      console.error(error);
      setMessage("Could not load conflicts.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h2>Conflicts</h2>

        <p>
          Review inconsistencies identified across patient records.
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
            <h3>Record Conflicts</h3>

            <p className="card-subtitle">
              Conflicting information requiring review.
            </p>
          </div>

          <button
            className="primary-button"
            onClick={loadConflicts}
          >
            Refresh
          </button>
        </div>

        <div style={{ marginTop: "20px" }}>
          {loading && <p>Loading conflicts...</p>}

          {!loading && message && <p>{message}</p>}

          {!loading && !message && conflicts.length === 0 && (
            <div
              style={{
                padding: "30px",
                textAlign: "center",
                background: "#f8fafc",
                borderRadius: "10px",
              }}
            >
              <div style={{ fontSize: "35px" }}>✓</div>

              <h3 style={{ marginTop: "10px" }}>
                No conflicts found
              </h3>

              <p style={{ marginTop: "5px" }}>
                No conflicting records are currently available
                for review.
              </p>
            </div>
          )}

          {!loading && !message && conflicts.length > 0 && (
            <div>
              {conflicts.map((conflict) => (
                <div
                  key={conflict.id}
                  style={{
                    padding: "18px",
                    marginBottom: "15px",
                    border: "1px solid #e5e7eb",
                    borderRadius: "10px",
                  }}
                >
                  <h3>{conflict.title || "Record Conflict"}</h3>

                  <p style={{ marginTop: "8px" }}>
                    <strong>Patient:</strong>{" "}
                    {conflict.patient_id || "Unknown"}
                  </p>

                  <p style={{ marginTop: "5px" }}>
                    <strong>Status:</strong>{" "}
                    {conflict.status || "Needs Review"}
                  </p>

                  {conflict.description && (
                    <p style={{ marginTop: "10px" }}>
                      {conflict.description}
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

export default Conflicts;