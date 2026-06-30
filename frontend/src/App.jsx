import { useState } from "react";
import ResumeUpload from "./components/ResumeUpload";
import JDInput from "./components/JDInput";
import ResultsPanel from "./components/ResultsPanel";
import "./App.css";

function LoadingOverlay() {
  return (
    <div className="loading-overlay" aria-live="polite" aria-label="Analyzing">
      <div className="loading-card">
        <div className="spinner spinner--lg" />
        <p className="loading-text">Analyzing your resume…</p>
        <p className="loading-hint">Extracting and matching skills</p>
      </div>
    </div>
  );
}

export default function App() {
  const [resumeUploaded, setResumeUploaded] = useState(false);
  const [resumeName, setResumeName] = useState("");
  const [matchData, setMatchData] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleUploadSuccess = (filename) => {
    setResumeUploaded(true);
    setResumeName(filename);
    setMatchData(null);
  };

  const handleMatchResult = (data) => {
    setIsAnalyzing(false);
    setMatchData(data);
    if (data) {
      setTimeout(() => {
        document.getElementById("results-section")?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }, 100);
    }
  };

  const handleAnalyzing = () => setIsAnalyzing(true);

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">⚡</span>
            <span className="logo-text">ResumeAI</span>
          </div>
          <div className="header-tagline">
            ATS Score · Skill Gap Analysis · Job Match
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="hero-section">
        <h1 className="hero-title">
          Get Your Resume <span className="gradient-text">ATS-Ready</span>
        </h1>
        <p className="hero-subtitle">
          Upload your resume, paste a job description, and instantly see your
          match score with missing skills highlighted.
        </p>

        {resumeUploaded && (
          <div className="resume-badge" role="status">
            <span className="resume-badge__icon">✓</span>
            <span>{resumeName} is ready</span>
          </div>
        )}
      </section>

      {/* Main Input Area */}
      <main className="main-content">
        <div className="input-grid">
          <ResumeUpload onUploadSuccess={handleUploadSuccess} />
          <JDInput
            onMatchResult={handleMatchResult}
            onAnalyzing={handleAnalyzing}
            isResumeUploaded={resumeUploaded}
          />
        </div>

        {/* Results */}
        {matchData && <ResultsPanel data={matchData} />}
      </main>

      {/* Loading overlay */}
      {isAnalyzing && <LoadingOverlay />}

      {/* Footer */}
      <footer className="app-footer">
        <p>AI Resume Analyzer · Built with FastAPI + React</p>
      </footer>
    </div>
  );
}