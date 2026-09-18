import { useEffect, useState } from "react";
import { getStats } from "../services/api";

function Dashboard() {
  const [stats, setStats] = useState({
    patients: 0,
    documents: 0,
    events: 0,
    conflicts: 0,
  });

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await getStats();
      setStats(data);
    } catch (error) {
      console.error("Could not load statistics:", error);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h2>Medical Intelligence Dashboard</h2>

        <p>
          Transform medical documents into a chronological, evidence-backed
          patient timeline.
        </p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">PATIENTS</div>
          <div className="stat-value">{stats.patients}</div>
          <div className="stat-note">Current records</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">DOCUMENTS</div>
          <div className="stat-value">{stats.documents}</div>
          <div className="stat-note">Uploaded documents</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">TIMELINE EVENTS</div>
          <div className="stat-value">{stats.events}</div>
          <div className="stat-note">Recorded events</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">NEEDS REVIEW</div>
          <div className="stat-value">{stats.conflicts}</div>
          <div className="stat-note">Current conflicts</div>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="card">
          <h3>Upload Medical Document</h3>

          <p className="card-subtitle">
            Add a discharge summary, clinical note, lab report or medical
            document.
          </p>

          <div className="upload-box">
            <div className="upload-icon">📄</div>

            <h4>Upload from Documents</h4>

            <p>
              Upload a document to ChronoMed for processing.
            </p>
          </div>
        </div>

        <div className="card">
          <h3>System Status</h3>

          <p className="card-subtitle">
            Current ChronoMed system information
          </p>

          <div className="activity">
            <div className="activity-item">
              <div className="activity-icon">✓</div>

              <div>
                <strong>Backend API</strong>
                <span>Connected</span>
              </div>
            </div>

            <div className="activity-item">
              <div className="activity-icon">AI</div>

              <div>
                <strong>AI/ML Processing</strong>
                <span>Not connected yet</span>
              </div>
            </div>

            <div className="activity-item">
              <div className="activity-icon">DB</div>

              <div>
                <strong>Database</strong>
                <span>Prototype in-memory storage</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;