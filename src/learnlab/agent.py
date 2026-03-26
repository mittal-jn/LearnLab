"""
learnlab.agent
──────────────
All AI interactions.
Currently supports Groq only.

secrets.toml example:
    PROVIDER      = "groq"
    GROQ_API_KEY  = "gsk_..."       # from console.groq.com (free)
"""

from __future__ import annotations

import json
import re

# ── Provider setup ────────────────────────────────────────────────────────────

def _get_provider(secrets: dict) -> str:
    return secrets.get("PROVIDER", "groq").lower()


def _groq_client(api_key: str):
    try:
        from groq import Groq
    except ModuleNotFoundError as exc:  # pragma: no cover
        raise ModuleNotFoundError(
            "Provider is set to 'groq', but the 'groq' package is not installed. "
            "Install it (`uv add groq`)."
        ) from exc
    return Groq(api_key=api_key)


def _chat(messages: list[dict], system: str, secrets: dict, max_tokens: int = 1800) -> str:
    """Chat call (Groq-only)."""
    provider = _get_provider(secrets)

    if provider == "groq":
        client = _groq_client(secrets["GROQ_API_KEY"])
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # free, fast, smart
            max_tokens=max_tokens,
            messages=[{"role": "system", "content": system}] + messages,
        )
        return resp.choices[0].message.content.strip()

    raise ValueError(f"Unsupported PROVIDER={provider!r}. Only 'groq' is supported.")


# ── Concept dashboard ─────────────────────────────────────────────────────────

CONCEPT_SYSTEM = """You are an expert CS educator. Return ONLY valid JSON (no markdown, no backticks) with this exact structure:
{
  "title": "concept name",
  "tagline": "punchy one-liner",
  "description": "3-4 sentence clear explanation for intermediate developers",
  "keyPoints": [
    {"label": "Time Complexity", "value": "O(log n)"},
    {"label": "Space Complexity", "value": "O(1)"},
    {"label": "Best Use", "value": "Sorted arrays"},
    {"label": "Avoid When", "value": "Unsorted data"}
  ],
  "diagram": {
    "type": "flowchart",
    "nodes": [
      {"id":"n1","label":"Start","color":"#7b61ff"},
      {"id":"n2","label":"Check mid","color":"#00e5c0"},
      {"id":"n3","label":"Found","color":"#3ddc84"},
      {"id":"n4","label":"Narrow","color":"#ffd166"}
    ],
    "edges": [
      {"from":"n1","to":"n2"},
      {"from":"n2","to":"n3","label":"match"},
      {"from":"n2","to":"n4","label":"no match"},
      {"from":"n4","to":"n2"}
    ]
  },
  "analogy": {
    "emoji": "📖",
    "text": "Think of it like... [analogy with <strong>bold keyword</strong>]"
  },
  "quiz": {
    "question": "Question about the concept?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correctIndex": 1,
    "explanation": "Because..."
  },
  "codeExample": "# Commented example in the requested language\n# Max 40 lines\n"
}
Rules: exactly 4 keyPoints, exactly 4 quiz options, codeExample must be valid runnable code."""


def fetch_concept(topic: str, lang: str, secrets: dict) -> dict:
    """Fetch a full concept dashboard JSON."""
    raw = _chat(
        messages=[{"role": "user", "content": f'Topic: "{topic}" — Language: {lang}. Write codeExample in {lang}.'}],
        system=CONCEPT_SYSTEM,
        secrets=secrets,
        max_tokens=1800,
    )
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    # Groq sometimes wraps in ```
    raw = re.sub(r"^```\s*", "", raw)
    return json.loads(raw)


# ── Code runner ───────────────────────────────────────────────────────────────

def simulate_run(code: str, lang: str, secrets: dict) -> tuple[str, str]:
    """Simulate executing code. Returns (output, 'success'|'error')."""
    out = _chat(
        messages=[{"role": "user", "content": f"Run this {lang} code:\n\n{code}"}],
        system=(
            f"You are a {lang} interpreter. Return ONLY what stdout/stderr would show. "
            "Prefix output lines with '> ', errors with 'ERROR: '. No explanation, no markdown."
        ),
        secrets=secrets,
        max_tokens=500,
    )
    return out, "error" if "ERROR:" in out else "success"


# ── AI tutor agent ────────────────────────────────────────────────────────────

def tutor_reply(
    question: str,
    topic: str,
    lang: str,
    history: list[dict],
    secrets: dict,
) -> str:
    """Context-aware AI tutor with conversation memory."""
    system = (
        f'You are LearnLab\'s AI tutor. The student is studying "{topic}" in {lang}.\n'
        f"Answer in 2-5 sentences. For code requests, use a fenced {lang} code block (≤15 lines).\n"
        "Be encouraging and build on previous answers."
    )
    messages = [{"role": m["role"], "content": m["content"]} for m in history[-8:]]
    messages.append({"role": "user", "content": question})

    return _chat(messages=messages, system=system, secrets=secrets, max_tokens=700)
