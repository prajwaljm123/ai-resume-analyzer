import { useState } from "react";
import api from "./api/api";
import ResumeUpload from "./components/ResumeUpload";
import JDInput from "./components/JDInput";
import ResultsPanel from "./components/ResultsPanel";
import AIFeedback from "./components/AIFeedback";
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
  const [resumeUploaded, setResumeUploaded]     = useState(false);
  const [resumeName, setResumeName]             = useState("");
  const [matchData, setMatchData]               = useState(null);
  const [isAnalyzing, setIsAnalyzing]           = useState(false);

  // AI feedback state
  const [aiFeedback, setAiFeedback]             = useState(null);
  const [aiFeedbackStatus, setAiFeedbackStatus] = useState("idle"); // idle | loading | done | error
  const [aiFeedbackError, setAiFeedbackError]   = useState("");

  // Store last resume text so we can pass it to /generate-feedback
  const [resumeText, setResumeText]             = useState("");
  const [lastJdText, setLastJdText]             = useState("");

  const handleUploadSuccess = (filename) => {
    setResumeUploaded(true);
    setResumeName(filename);
    setMatchData(null);
    setAiFeedback(null);
    setAiFeedbackStatus("idle");

    // Fetch extracted text right after upload so it's ready for AI
    api.get("/extract-text")
      .then((res) => setResumeText(res.data?.text ?? ""))
      .catch(() => setResumeText(""));
  };

  const handleMatchResult = (data, jdText) => {
    setIsAnalyzing(false);
    setMatchData(data);
    if (jdText) setLastJdText(jdText);

    if (data) {
      // Scroll to results
      setTimeout(() => {
        document.getElementById("results-section")?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }, 100);

      // Fire AI feedback call non-blocking
      fireAiFeedback(data, jdText ?? lastJdText);
    }
  };

  const fireAiFeedback = async (matchData, jdText) => {
    setAiFeedbackStatus("loading");
    setAiFeedback(null);
    setAiFeedbackError("");

    const matchResult = matchData?.match_result ?? {};
    const matched = Array.isArray(matchResult.matched_skills)
      ? matchResult.matched_skills
      : (matchResult.matched_skills?.all ?? []);
    const missing = Array.isArray(matchResult.missing_skills)
      ? matchResult.missing_skills
      : (matchResult.missing_skills?.all ?? []);
    const atsScore = matchResult.ats_score ?? matchResult.match_percentage ?? 0;

    try {
      const res = await api.post("/generate-feedback", {
        resume_text:    resumeText,
        jd_text:        jdText,
        ats_score:      Math.round(atsScore),
        matched_skills: matched,
        missing_skills: missing,
      });

      setAiFeedback(res.data);
      setAiFeedbackStatus("done");

      // Scroll to AI section after it loads
      setTimeout(() => {
        document.getElementById("ai-feedback")?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }, 200);
    } catch (err) {
      setAiFeedbackStatus("error");
      setAiFeedbackError(
        err?.response?.data?.detail || "Could not reach AI service."
      );
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
            ATS Score · Skill Gap Analysis · AI Feedback
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="hero-section">
        <h1 className="hero-title">
          Get Your Resume <span className="gradient-text">ATS-Ready</span>
        </h1>
        <p className="hero-subtitle">
          Upload your resume, paste a job description, and get an instant ATS
          score with AI-powered improvement tips.
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

        {/* ATS Results */}
        {matchData && <ResultsPanel data={matchData} />}

        {/* AI Feedback — loads non-blocking after ATS results */}
        <AIFeedback
          status={aiFeedbackStatus}
          feedback={aiFeedback}
          error={aiFeedbackError}
        />
      </main>

      {/* Loading overlay */}
      {isAnalyzing && <LoadingOverlay />}

      {/* Footer */}
      <footer className="app-footer">
        <p>AI Resume Analyzer · FastAPI + React + OpenRouter</p>
      </footer>
    </div>
  );
}