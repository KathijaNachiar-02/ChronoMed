import { useState } from "react";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function QA() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) {
      return;
    }

    setLoading(true);
    setAnswer("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to ask question");
      }

      const data = await response.json();

      setAnswer(data.answer || "No answer available.");
    } catch (error) {
      console.error(error);
      setAnswer("Could not connect to the Q&A service.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h2>Q&A</h2>

        <p>
          Ask questions about the patient's medical records.
        </p>
      </div>

      <div className="card">
        <h3>Ask ChronoMed</h3>

        <p className="card-subtitle">
          Ask a question and retrieve information from processed
          medical documents.
        </p>

        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Example: What medications were prescribed?"
          rows={5}
          style={{
            width: "100%",
            marginTop: "20px",
            padding: "12px",
            borderRadius: "8px",
            border: "1px solid #d1d5db",
            resize: "vertical",
            fontFamily: "inherit",
          }}
        />

        <button
          className="primary-button"
          onClick={askQuestion}
          disabled={loading}
          style={{ marginTop: "12px" }}
        >
          {loading ? "Asking..." : "Ask Question"}
        </button>

        {answer && (
          <div
            style={{
              marginTop: "20px",
              padding: "18px",
              background: "#f8fafc",
              borderRadius: "10px",
              border: "1px solid #e5e7eb",
            }}
          >
            <h3>Answer</h3>

            <p style={{ marginTop: "10px" }}>
              {answer}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default QA;