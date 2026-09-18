import { useEffect, useState } from "react";
import { uploadDocument, getDocuments } from "../services/api";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function Documents() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [processingId, setProcessingId] = useState("");
  const [message, setMessage] = useState("");
  const [documents, setDocuments] = useState<any[]>([]);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const data = await getDocuments();
      setDocuments(data);
    } catch (error) {
      console.error("Could not load documents:", error);
    }
  };

  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];

    if (file) {
      setSelectedFile(file);
      setMessage("");
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage("Please select a document first.");
      return;
    }

    setUploading(true);
    setMessage("");

    try {
      await uploadDocument(selectedFile);

      setMessage("Document uploaded successfully.");
      setSelectedFile(null);

      await loadDocuments();
    } catch (error) {
      setMessage(
        "Upload could not be completed. Backend may not be running."
      );
    } finally {
      setUploading(false);
    }
  };

  const handleProcess = async (documentId: string) => {
    setProcessingId(documentId);
    setMessage("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/documents/${documentId}/process`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error("Processing failed");
      }

      if (data.status === "processed") {
        setMessage("Document processed successfully.");
      } else {
        setMessage(`Document processing status: ${data.status}`);
      }

      await loadDocuments();
    } catch (error) {
      console.error(error);
      setMessage("Could not process the document.");
    } finally {
      setProcessingId("");
    }
  };

  return (
    <div>
      <div className="page-header">
        <h2>Medical Documents</h2>

        <p>
          Upload and manage medical documents processed by ChronoMed.
        </p>
      </div>

      <div className="card">
        <h3>Upload Medical Document</h3>

        <p className="card-subtitle">
          Upload a discharge summary, clinical note, lab report,
          or other medical document.
        </p>

        <div className="upload-box">
          <div className="upload-icon">📄</div>

          <h3>
            {selectedFile
              ? selectedFile.name
              : "Choose a medical document"}
          </h3>

          <p>
            Select a document from your computer to send it to ChronoMed.
          </p>

          <input
            type="file"
            id="document-upload"
            accept=".pdf,.txt,.doc,.docx"
            onChange={handleFileChange}
            style={{ display: "none" }}
          />

          <label
            htmlFor="document-upload"
            className="upload-button"
          >
            Choose Document
          </label>

          {selectedFile && (
            <button
              onClick={handleUpload}
              disabled={uploading}
              className="upload-button"
              style={{ marginLeft: "10px" }}
            >
              {uploading ? "Uploading..." : "Upload"}
            </button>
          )}

          {message && (
            <p style={{ marginTop: "15px" }}>
              {message}
            </p>
          )}
        </div>
      </div>

      <div className="card">
        <h3>Recent Documents</h3>

        <p className="card-subtitle">
          Documents uploaded to ChronoMed.
        </p>

        {documents.length === 0 ? (
          <p>No documents uploaded yet.</p>
        ) : (
          <div>
            {documents.map((document) => (
              <div
                key={document.id}
                className="document-item"
                style={{
                  padding: "15px 0",
                  borderBottom: "1px solid #e5e7eb",
                }}
              >
                <strong>{document.filename}</strong>

                <div style={{ marginTop: "5px" }}>
                  Status: {document.status}
                </div>

                {document.status === "uploaded" && (
                  <button
                    onClick={() => handleProcess(document.id)}
                    disabled={processingId === document.id}
                    className="primary-button"
                    style={{ marginTop: "10px" }}
                  >
                    {processingId === document.id
                      ? "Processing..."
                      : "Process Document"}
                  </button>
                )}

                {document.status === "processed" && (
                  <div style={{ marginTop: "10px" }}>
                    Text extracted successfully.
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Documents;