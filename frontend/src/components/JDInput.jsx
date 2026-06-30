import { useState } from "react";
import api from "../api/api";

const PLACEHOLDER =
  `Software Engineer – Full Stack
We are looking for a skilled engineer with experience in:

• Python, FastAPI or Django
• React, TypeScript, Node.js
• PostgreSQL, Redis
• Docker, Kubernetes, AWS or GCP
• Strong knowledge of REST APIs and CI/CD pipelines`;

export default function JDInput({ onMatchResult, onAnalyzing, isResumeUploaded }) {
  const [jdText, setJdText] = useState("");
  const [status, setStatus] = useState("idle"); // idle | analyzing | success | error
  const [errorMsg, setErrorMsg] = useState("");
  const [charCount, setCharCount] = useState(0);

  const MIN_CHARS = 80;

  const handleTextChange = (e) => {
    setJdText(e.target.value);
    setCharCount(e.target.value.length);
    if (status === "error") {
      setStatus("idle");
      setErrorMsg("");
    }
  };

  const handleAnalyze = async () => {
    if (!isResumeUploaded) {
      setStatus("error");
      setErrorMsg("Please upload your resume first before analyzing.");
      return;
    }
    if (jdText.trim().length < MIN_CHARS) {
      setStatus("error");
      setErrorMsg(`Please paste a complete job description (at least ${MIN_CHARS} characters).`);
      return;
    }

    setStatus("analyzing");
    setErrorMsg("");
    if (onAnalyzing) onAnalyzing();

    try {
      const res = await api.post("/match-jd", { jd_text: jdText.trim() });
      setStatus("success");
      onMatchResult(res.data);
    } catch (err) {
      setStatus("error");
      setErrorMsg(
        err?.response?.data?.detail || "Analysis failed. Please try again."
      );
      setStatus("error");
    }
  };

  const handleClear = () => {
    setJdText("");
    setCharCount(0);
    setStatus("idle");
    setErrorMsg("");
    onMatchResult(null);
  };

  const handlePaste = async () => {
    try {
      const text = await navigator.clipboard.readText();
      setJdText(text);
      setCharCount(text.length);
    } catch {
      setErrorMsg("Clipboard access denied. Please paste manually.");
    }
  };

  const isValid = jdText.trim().length >= MIN_CHARS;

  return (
    <div className="card">
      <div className="card-header">
        <span className="step-badge">02</span>
        <h2 className="card-title">Job Description</h2>
        <p className="card-subtitle">Paste the full JD from LinkedIn, Naukri, Indeed, etc.</p>
      </div>

      <div className="textarea-wrapper">
        <textarea
          className={`jd-textarea ${status === "error" ? "jd-textarea--error" : ""}`}
          value={jdText}
          onChange={handleTextChange}
          placeholder={PLACEHOLDER}
          rows={10}
          disabled={status === "analyzing"}
          id="jd-text-input"
          aria-label="Job description text"
        />
        <div className="textarea-footer">
          <span className={`char-count ${isValid ? "char-count--valid" : ""}`}>
            {charCount} chars {isValid ? "✓" : `(min ${MIN_CHARS})`}
          </span>
          <button
            className="btn btn--ghost btn--sm"
            onClick={handlePaste}
            title="Paste from clipboard"
            type="button"
          >
            Paste
          </button>
        </div>
      </div>

      {status === "error" && errorMsg && (
        <p className="field-error" role="alert">{errorMsg}</p>
      )}

      <div className="card-actions">
        <button
          className="btn btn--ghost"
          onClick={handleClear}
          disabled={!jdText && status === "idle"}
          type="button"
        >
          Clear
        </button>
        <button
          className="btn btn--primary"
          onClick={handleAnalyze}
          disabled={!isValid || status === "analyzing"}
          id="analyze-jd-btn"
          type="button"
        >
          {status === "analyzing" ? (
            <span className="btn__loading">
              <span className="spinner spinner--sm" /> Analyzing…
            </span>
          ) : (
            "Analyze Match"
          )}
        </button>
      </div>
    </div>
  );
}
