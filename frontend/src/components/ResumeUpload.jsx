import { useState, useRef, useCallback } from "react";
import api from "../api/api";

export default function ResumeUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | uploading | success | error
  const [errorMsg, setErrorMsg] = useState("");
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef(null);

  const validateFile = (f) => {
    if (!f) return "No file selected.";
    if (f.type !== "application/pdf") return "Only PDF files are accepted.";
    if (f.size > 10 * 1024 * 1024) return "File size must be under 10 MB.";
    return null;
  };

  const handleFile = (f) => {
    const err = validateFile(f);
    if (err) {
      setErrorMsg(err);
      setStatus("error");
      setFile(null);
      return;
    }
    setFile(f);
    setStatus("idle");
    setErrorMsg("");
  };

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    const dropped = e.dataTransfer.files[0];
    handleFile(dropped);
  }, []);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => setIsDragging(false);

  const handleInputChange = (e) => {
    handleFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    setStatus("uploading");
    setErrorMsg("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await api.post("/upload-resume", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setStatus("success");
      onUploadSuccess(file.name, res.data);
    } catch (err) {
      setStatus("error");
      setErrorMsg(
        err?.response?.data?.detail || "Upload failed. Please try again."
      );
    }
  };

  const handleReset = () => {
    setFile(null);
    setStatus("idle");
    setErrorMsg("");
    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <div className="card">
      <div className="card-header">
        <span className="step-badge">01</span>
        <h2 className="card-title">Upload Resume</h2>
        <p className="card-subtitle">PDF format only · Max 10 MB</p>
      </div>

      {/* Drop Zone */}
      <div
        className={`drop-zone ${isDragging ? "drop-zone--active" : ""} ${
          status === "success" ? "drop-zone--success" : ""
        } ${status === "error" ? "drop-zone--error" : ""}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => status !== "success" && inputRef.current?.click()}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === "Enter" && inputRef.current?.click()}
        aria-label="Resume upload drop zone"
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf"
          onChange={handleInputChange}
          style={{ display: "none" }}
          id="resume-file-input"
        />

        {status === "success" ? (
          <div className="drop-zone__content">
            <span className="drop-zone__icon success-icon">✓</span>
            <p className="drop-zone__text success-text">
              <strong>{file?.name}</strong>
            </p>
            <p className="drop-zone__hint">Resume uploaded successfully</p>
          </div>
        ) : (
          <div className="drop-zone__content">
            <span className="drop-zone__icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="12" y1="18" x2="12" y2="12"/>
                <line x1="9" y1="15" x2="15" y2="15"/>
              </svg>
            </span>
            {file ? (
              <>
                <p className="drop-zone__text">
                  <strong>{file.name}</strong>
                </p>
                <p className="drop-zone__hint">
                  {(file.size / 1024).toFixed(1)} KB · Click to change
                </p>
              </>
            ) : (
              <>
                <p className="drop-zone__text">
                  {isDragging ? "Drop your PDF here" : "Drag & drop your PDF here"}
                </p>
                <p className="drop-zone__hint">or click to browse files</p>
              </>
            )}
          </div>
        )}
      </div>

      {/* Error message */}
      {status === "error" && errorMsg && (
        <p className="field-error" role="alert">{errorMsg}</p>
      )}

      {/* Actions */}
      <div className="card-actions">
        {status === "success" ? (
          <button className="btn btn--ghost" onClick={handleReset}>
            Replace Resume
          </button>
        ) : (
          <button
            className="btn btn--primary"
            onClick={handleUpload}
            disabled={!file || status === "uploading"}
            id="upload-resume-btn"
          >
            {status === "uploading" ? (
              <span className="btn__loading">
                <span className="spinner spinner--sm" /> Uploading…
              </span>
            ) : (
              "Upload Resume"
            )}
          </button>
        )}
      </div>
    </div>
  );
}
