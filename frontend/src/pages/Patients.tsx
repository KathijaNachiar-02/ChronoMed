import { useEffect, useState } from "react";
import { getPatients } from "../services/api";

function Patients() {
  const [patients, setPatients] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPatients();
  }, []);

  const loadPatients = async () => {
    try {
      const data = await getPatients();
      setPatients(data);
    } catch (error) {
      console.error("Could not load patients:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h2>Patients</h2>
        <p>View patients registered in the ChronoMed system.</p>
      </div>

      <div className="card">
        <h3>Patient Records</h3>

        <p className="card-subtitle">
          Patients currently available in ChronoMed.
        </p>

        {loading ? (
          <p>Loading patients...</p>
        ) : patients.length === 0 ? (
          <p>No patients found.</p>
        ) : (
          <div>
            {patients.map((patient) => (
              <div
                key={patient.id}
                style={{
                  padding: "15px 0",
                  borderBottom: "1px solid #e5e7eb",
                }}
              >
                <strong>{patient.name}</strong>

                <div style={{ marginTop: "5px" }}>
                  Patient ID: {patient.id}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Patients;