const SECTION_CONFIG = {
  pros: {
    title: "Strengths",
    icon: "✦",
    variant: "pros",
    emptyMsg: "No strengths identified.",
  },
  cons: {
    title: "Weaknesses",
    icon: "▲",
    variant: "cons",
    emptyMsg: "No weaknesses identified.",
  },
  suggestions: {
    title: "Suggestions",
    icon: "→",
    variant: "suggestions",
    emptyMsg: "No suggestions available.",
  },
};

function FeedbackSkeleton() {
  return (
    <div className="ai-feedback-grid">
      {[1, 2, 3].map((i) => (
        <div key={i} className="card ai-feedback-card ai-feedback-card--skeleton">
          <div className="skeleton skeleton--title" />
          <div className="skeleton skeleton--line" />
          <div className="skeleton skeleton--line skeleton--line-short" />
          <div className="skeleton skeleton--line" />
          <div className="skeleton skeleton--line skeleton--line-short" />
        </div>
      ))}
    </div>
  );
}

function FeedbackSection({ sectionKey, items }) {
  const config = SECTION_CONFIG[sectionKey];
  if (!config) return null;

  const list = Array.isArray(items) ? items : [];

  return (
    <div className={`card ai-feedback-card ai-feedback-card--${config.variant}`}>
      <h3 className="ai-feedback-card__title">
        <span className={`ai-feedback-card__icon ai-feedback-card__icon--${config.variant}`}>
          {config.icon}
        </span>
        {config.title}
        <span className="ai-feedback-card__count">{list.length}</span>
      </h3>

      {list.length === 0 ? (
        <p className="ai-feedback-empty">{config.emptyMsg}</p>
      ) : (
        <ul className="ai-feedback-list">
          {list.map((item, idx) => (
            <li key={idx} className={`ai-feedback-item ai-feedback-item--${config.variant}`}>
              <span className="ai-feedback-item__bullet" />
              <span>{item}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default function AIFeedback({ status, feedback, error }) {
  // status: 'idle' | 'loading' | 'done' | 'error'

  if (status === "idle") return null;

  return (
    <div className="ai-feedback-section fade-in" id="ai-feedback" aria-live="polite">
      {/* Section header */}
      <div className="ai-feedback-header">
        <div className="ai-feedback-label">
          <span className="ai-badge">
            <span className="ai-badge__dot" />
            AI Analysis
          </span>
        </div>
        <h2 className="ai-feedback-title">Resume Feedback</h2>
        <p className="ai-feedback-subtitle">
          Powered by AI — tailored strengths, weaknesses, and improvement tips
        </p>
      </div>

      {/* Loading skeletons */}
      {status === "loading" && <FeedbackSkeleton />}

      {/* Error / AI unavailable */}
      {status === "error" && (
        <div className="ai-unavailable-card card">
          <span className="ai-unavailable-icon">⚠</span>
          <p className="ai-unavailable-title">AI feedback unavailable</p>
          <p className="ai-unavailable-hint">
            {error || "Check that OPENROUTER_API_KEY is set in backend/.env"}
          </p>
        </div>
      )}

      {/* Done — render feedback */}
      {status === "done" && feedback && (
        <>
          {!feedback.ai_available && (
            <div className="ai-fallback-banner">
              <span>⚠</span>
              AI model unavailable — showing default suggestions. Add your{" "}
              <code>OPENROUTER_API_KEY</code> to <code>backend/.env</code>.
            </div>
          )}
          <div className="ai-feedback-grid">
            <FeedbackSection sectionKey="pros"        items={feedback.feedback?.pros} />
            <FeedbackSection sectionKey="cons"        items={feedback.feedback?.cons} />
            <FeedbackSection sectionKey="suggestions" items={feedback.feedback?.suggestions} />
          </div>
        </>
      )}
    </div>
  );
}
