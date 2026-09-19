import { useEffect, useState } from "react";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function Events() {
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    loadEvents();
  }, []);

  const loadEvents = async () => {
    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/events`);

      if (!response.ok) {
        throw new Error("Failed to load events");
      }

      const data = await response.json();

      setEvents(data);
    } catch (error) {
      console.error(error);
      setMessage("Could not load events.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h2>Medical Events</h2>

        <p>
          View medical events recorded for ChronoMed patients.
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
            <h3>Event Records</h3>

            <p className="card-subtitle">
              Medical events currently available in the system.
            </p>
          </div>

          <button
            className="primary-button"
            onClick={loadEvents}
          >
            Refresh
          </button>
        </div>

        <div style={{ marginTop: "20px" }}>
          {loading && <p>Loading events...</p>}

          {!loading && message && <p>{message}</p>}

          {!loading && !message && events.length === 0 && (
            <p>No medical events found.</p>
          )}

          {!loading && !message && events.length > 0 && (
            <div>
              {events.map((event) => (
                <div
                  key={event.id}
                  style={{
                    padding: "18px",
                    marginBottom: "15px",
                    border: "1px solid #e5e7eb",
                    borderRadius: "10px",
                    background: "#ffffff",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      gap: "20px",
                      flexWrap: "wrap",
                    }}
                  >
                    <div>
                      <strong>Event ID</strong>
                      <div style={{ marginTop: "5px" }}>
                        {event.id}
                      </div>
                    </div>

                    <div>
                      <strong>Patient ID</strong>
                      <div style={{ marginTop: "5px" }}>
                        {event.patient_id}
                      </div>
                    </div>

                    <div>
                      <strong>Event Type</strong>
                      <div style={{ marginTop: "5px" }}>
                        {event.event_type}
                      </div>
                    </div>

                    <div>
                      <strong>Date</strong>
                      <div style={{ marginTop: "5px" }}>
                        {event.date}
                      </div>
                    </div>
                  </div>

                  <div
                    style={{
                      marginTop: "15px",
                      paddingTop: "15px",
                      borderTop: "1px solid #e5e7eb",
                    }}
                  >
                    <strong>Description</strong>

                    <p style={{ marginTop: "5px" }}>
                      {event.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Events;