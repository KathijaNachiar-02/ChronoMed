import { useEffect, useState } from "react";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function Timeline() {
  const [patientId, setPatientId] = useState("P001");
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const loadTimeline = async () => {
    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/patients/${patientId}/timeline`
      );

      if (!response.ok) {
        throw new Error("Failed to load timeline");
      }

      const data = await response.json();

      setEvents(data.timeline || []);
    } catch (error) {
      console.error(error);
      setMessage("Could not load patient timeline.");
      setEvents([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTimeline();
  }, []);

  return (
    <div>
      <div className="page-header">
        <h2>Patient Timeline</h2>
        <p>
          View medical events in chronological order for a patient.
        </p>
      </div>

      <div className="card">
        <h3>Select Patient</h3>

        <div
          style={{
            display: "flex",
            gap: "10px",
            marginTop: "15px",
          }}
        >
          <input
            type="text"
            value={patientId}
            onChange={(e) => setPatientId(e.target.value)}
            placeholder="Enter Patient ID"
            style={{
              padding: "10px",
              border: "1px solid #d1d5db",
              borderRadius: "6px",
            }}
          />

          <button
            className="primary-button"
            onClick={loadTimeline}
          >
            View Timeline
          </button>
        </div>
      </div>

      <div className="card">
        <h3>Medical Events</h3>

        {loading && <p>Loading timeline...</p>}

        {!loading && message && <p>{message}</p>}

        {!loading && !message && events.length === 0 && (
          <p>
            No timeline events found for patient {patientId}.
          </p>
        )}

        {!loading && events.length > 0 && (
          <div>
            {events.map((event) => (
              <div
                key={event.id}
                style={{
                  padding: "15px",
                  marginTop: "15px",
                  borderLeft: "4px solid #2563eb",
                  background: "#f8fafc",
                }}
              >
                <strong>{event.event_type}</strong>

                <div style={{ marginTop: "5px" }}>
                  Date: {event.date}
                </div>

                <div style={{ marginTop: "5px" }}>
                  {event.description}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Timeline;