import os
import json
import requests

# ─────────────────────────────────────────
# Config — ordered fallback list
# All confirmed free + non-reasoning instruct models from OpenRouter live API
# ─────────────────────────────────────────
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

FREE_MODELS = [
    # ── Confirmed working right now ──────────────────────────
    "google/gemma-4-26b-a4b-it:free",                        # 26B MoE — clean JSON ✅
    "liquid/lfm-2.5-1.2b-instruct:free",                     # 1.2B — JSON in code fences ✅
    # ── Fallback pool (rotate when above are rate-limited) ───
    "google/gemma-4-31b-it:free",                             # 31B, reasoning off by default
    "nousresearch/hermes-3-llama-3.1-405b:free",              # 405B instruct
    "meta-llama/llama-3.3-70b-instruct:free",                 # 70B instruct
    "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",  # 24B instruct
    "qwen/qwen3-next-80b-a3b-instruct:free",                  # 80B, reasoning optional
    "meta-llama/llama-3.2-3b-instruct:free",                  # 3B last resort
]

# Max chars of resume text sent to AI (stay within token limits)
MAX_RESUME_CHARS = 3000
MAX_JD_CHARS     = 1500

# Graceful fallback when AI is unavailable
FALLBACK_FEEDBACK = {
    "pros": [
        "Resume was parsed and analyzed successfully.",
        "Skills were extracted and matched against the job description."
    ],
    "cons": [
        "AI-powered feedback is currently unavailable.",
        "Please check your OPENROUTER_API_KEY in the .env file."
    ],
    "suggestions": [
        "Add the missing skills listed above to strengthen your resume.",
        "Tailor your resume summary to match the job description keywords.",
        "Quantify achievements where possible (e.g. 'Reduced load time by 40%')."
    ]
}


def _build_prompt(
    resume_text: str,
    jd_text: str,
    ats_score: int,
    matched_skills: list,
    missing_skills: list
) -> str:
    """Build the structured prompt sent to the AI model."""

    resume_snippet = resume_text[:MAX_RESUME_CHARS].strip()
    jd_snippet     = jd_text[:MAX_JD_CHARS].strip()

    matched_str = ", ".join(matched_skills) if matched_skills else "None"
    missing_str = ", ".join(missing_skills) if missing_skills else "None"

    return f"""You are an expert ATS analyst and career advisor. Analyze the resume below against the job description and provide honest, actionable feedback.

RESUME (excerpt):
{resume_snippet}

JOB DESCRIPTION (excerpt):
{jd_snippet}

ATS MATCH SCORE: {ats_score}/100
MATCHED SKILLS: {matched_str}
MISSING SKILLS: {missing_str}

Respond ONLY with a valid JSON object in this exact format (no markdown, no extra text):
{{
  "pros": [
    "Specific strength 1",
    "Specific strength 2",
    "Specific strength 3"
  ],
  "cons": [
    "Specific weakness 1",
    "Specific weakness 2",
    "Specific weakness 3"
  ],
  "suggestions": [
    "Actionable suggestion 1",
    "Actionable suggestion 2",
    "Actionable suggestion 3",
    "Actionable suggestion 4"
  ]
}}

Rules:
- pros: 3-5 genuine strengths based on matched skills and resume content
- cons: 3-5 honest weaknesses based on missing skills and gaps
- suggestions: 3-5 specific, actionable improvement tips tailored to this JD
- Be concise, specific, and professional
- Return ONLY the JSON object, nothing else"""


def _parse_ai_response(raw_content: str) -> dict:
    """
    Safely parse JSON from the AI response.
    Handles cases where the model wraps JSON in markdown code fences.
    """
    content = raw_content.strip()

    # Strip markdown code fences if present
    if content.startswith("```"):
        lines = content.split("\n")
        # Remove first and last fence lines
        lines = [l for l in lines if not l.strip().startswith("```")]
        content = "\n".join(lines).strip()

    parsed = json.loads(content)

    # Validate and normalise structure
    return {
        "pros":        list(parsed.get("pros", [])),
        "cons":        list(parsed.get("cons", [])),
        "suggestions": list(parsed.get("suggestions", []))
    }


def generate_resume_feedback(
    resume_text: str,
    jd_text: str,
    ats_score: int,
    matched_skills: list,
    missing_skills: list
) -> dict:
    """
    Call OpenRouter to generate AI-powered resume feedback.

    Returns:
        {
            "success": bool,
            "ai_available": bool,
            "feedback": { "pros": [...], "cons": [...], "suggestions": [...] }
        }
    """
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()

    if not api_key:
        return {
            "success": False,
            "ai_available": False,
            "feedback": FALLBACK_FEEDBACK,
            "error": "OPENROUTER_API_KEY not set in environment."
        }

    prompt = _build_prompt(
        resume_text   = resume_text,
        jd_text       = jd_text,
        ats_score     = ats_score,
        matched_skills = matched_skills,
        missing_skills = missing_skills
    )



    headers = {
        "Authorization":  f"Bearer {api_key}",
        "Content-Type":   "application/json",
        "HTTP-Referer":   "http://localhost:5173",
        "X-Title":        "AI Resume Analyzer"
    }

    last_error = "All models failed."

    for model in FREE_MODELS:
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4,
            "max_tokens": 800,
        }

        try:
            response = requests.post(
                OPENROUTER_API_URL,
                headers = headers,
                json    = payload,
                timeout = 30
            )

            # Rate limited or model unavailable — try next
            if response.status_code in (429, 404):
                last_error = f"{model} returned {response.status_code}. Trying next model."
                continue

            response.raise_for_status()

            data    = response.json()
            message = data["choices"][0]["message"]

            raw_content = (
                message.get("content") or
                message.get("reasoning") or
                message.get("reasoning_content") or
                ""
            )

            if not raw_content.strip():
                last_error = f"{model} returned empty content."
                continue

            feedback = _parse_ai_response(raw_content)

            return {
                "success":      True,
                "ai_available": True,
                "model_used":   model,
                "feedback":     feedback
            }

        except requests.exceptions.Timeout:
            last_error = f"{model} timed out."
            continue
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            last_error = f"{model} parse error: {str(e)}"
            continue
        except requests.exceptions.HTTPError as e:
            last_error = f"{model} HTTP error: {e.response.status_code}"
            continue

    # All models exhausted
    return {
        "success":      False,
        "ai_available": False,
        "feedback":     FALLBACK_FEEDBACK,
        "error":        last_error
    }
