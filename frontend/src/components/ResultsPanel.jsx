import { useMemo } from "react";

function ScoreRing({ score }) {
  const radius = 52;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const color =
    score >= 75 ? "var(--score-great)" :
    score >= 50 ? "var(--score-good)" :
    score >= 30 ? "var(--score-fair)" : "var(--score-poor)";

  const label =
    score >= 75 ? "Great Match" :
    score >= 50 ? "Good Match" :
    score >= 30 ? "Needs Work" : "Low Match";

  return (
    <div className="score-ring-wrapper" aria-label={`ATS Score: ${score}%`}>
      <svg className="score-ring" width="140" height="140" viewBox="0 0 140 140">
        {/* Background track */}
        <circle
          cx="70" cy="70" r={radius}
          fill="none"
          stroke="var(--border)"
          strokeWidth="10"
        />
        {/* Progress arc */}
        <circle
          cx="70" cy="70" r={radius}
          fill="none"
          stroke={color}
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform="rotate(-90 70 70)"
          style={{ transition: "stroke-dashoffset 1s ease, stroke 0.5s" }}
        />
        <text x="70" y="65" textAnchor="middle" dominantBaseline="middle" className="score-number" fill={color}>
          {score}%
        </text>
        <text x="70" y="86" textAnchor="middle" dominantBaseline="middle" className="score-label-svg" fill="var(--text)">
          {label}
        </text>
      </svg>
    </div>
  );
}

function SkillPill({ skill, variant }) {
  return (
    <span className={`skill-pill skill-pill--${variant}`}>{skill}</span>
  );
}

function SkillSection({ title, skills, variant, icon }) {
  const list = Array.isArray(skills) ? skills : [];
  if (list.length === 0) return null;
  return (
    <div className="skill-section">
      <h3 className="skill-section__title">
        <span className="skill-section__icon">{icon}</span>
        {title}
        <span className="skill-section__count">{list.length}</span>
      </h3>
      <div className="skill-pills">
        {list.map((skill) => (
          <SkillPill key={skill} skill={skill} variant={variant} />
        ))}
      </div>
    </div>
  );
}

export default function ResultsPanel({ data }) {
  const matchResult = data?.match_result;
  // matched_skills / missing_skills are objects: { categorized, all, total_matched }
  const score = useMemo(() => Math.round(matchResult?.ats_score ?? matchResult?.match_percentage ?? 0), [matchResult]);
  const matched = Array.isArray(matchResult?.matched_skills)
    ? matchResult.matched_skills
    : (matchResult?.matched_skills?.all ?? []);
  const missing = Array.isArray(matchResult?.missing_skills)
    ? matchResult.missing_skills
    : (matchResult?.missing_skills?.all ?? []);

  const resumeSkills = Array.isArray(data?.resume_skills)
    ? data.resume_skills
    : (data?.resume_skills?.all ?? []);
  const jdSkills = Array.isArray(data?.jd_skills)
    ? data.jd_skills
    : (data?.jd_skills?.all ?? []);

  if (!data) return null;

  return (
    <div className="results-panel fade-in" id="results-section" aria-live="polite">
      <div className="results-header">
        <h2 className="results-title">Analysis Results</h2>
        <p className="results-meta">
          Resume: <strong>{data.resume_file}</strong> · JD Skills found: <strong>{jdSkills.length}</strong>
        </p>
      </div>

      {/* ATS Score */}
      <div className="results-grid">
        <div className="card score-card">
          <h3 className="card-title">ATS Match Score</h3>
          <ScoreRing score={score} />
          <div className="score-stats">
            <div className="score-stat">
              <span className="score-stat__value matched-color">{matched.length}</span>
              <span className="score-stat__label">Matched</span>
            </div>
            <div className="score-stat">
              <span className="score-stat__value missing-color">{missing.length}</span>
              <span className="score-stat__label">Missing</span>
            </div>
            <div className="score-stat">
              <span className="score-stat__value">{jdSkills.length}</span>
              <span className="score-stat__label">Required</span>
            </div>
          </div>
        </div>

        <div className="card skills-card">
          <SkillSection
            title="Matched Skills"
            skills={matched}
            variant="matched"
            icon="✓"
          />
          <SkillSection
            title="Missing Skills"
            skills={missing}
            variant="missing"
            icon="✗"
          />
          {matched.length === 0 && missing.length === 0 && (
            <p className="no-skills-msg">No skill comparison data available.</p>
          )}
        </div>
      </div>

      {/* Resume skills breakdown */}
      {resumeSkills.length > 0 && (
        <div className="card resume-skills-card">
          <SkillSection
            title="All Resume Skills"
            skills={resumeSkills}
            variant="neutral"
            icon="◈"
          />
        </div>
      )}
    </div>
  );
}
