"""
learnlab.agent
──────────────
All AI calls via Groq (free). Three public functions:

    fetch_concept(topic, lang, api_key) -> dict
    simulate_run(code, lang, api_key)   -> (output_str, "success"|"error")
    tutor_reply(question, topic, lang, history, api_key) -> str
"""
from __future__ import annotations

import json
import re

from groq import Groq

MODEL = "llama-3.3-70b-versatile"


def _chat(
    system: str,
    user: str,
    api_key: str,
    history: list[dict] | None = None,
    max_tokens: int = 1800,
) -> str:
    messages = [{"role": "system", "content": system}]
    if history:
        messages += [{"role": m["role"], "content": m["content"]} for m in history]
    messages.append({"role": "user", "content": user})

    resp = Groq(api_key=api_key).chat.completions.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=messages,
    )
    return resp.choices[0].message.content.strip()


# ── Concept dashboard ─────────────────────────────────────────────────────────

_CONCEPT_SYSTEM = """You are an expert CS educator. Return ONLY raw JSON — no markdown fences, no explanation, nothing else.

Required structure:
{
  "title": "short concept name",
  "tagline": "one punchy line",
  "description": "3-4 sentences for intermediate developers",
  "keyPoints": [
    {"label": "Time Complexity",  "value": "O(log n)"},
    {"label": "Space Complexity", "value": "O(1)"},
    {"label": "Best Use",         "value": "Sorted arrays"},
    {"label": "Avoid When",       "value": "Unsorted data"}
  ],
  "diagram": {
    "type": "flowchart",
    "nodes": [
      {"id":"n1","label":"Start",     "color":"#7b61ff"},
      {"id":"n2","label":"Check mid", "color":"#00e5c0"},
      {"id":"n3","label":"Found",     "color":"#3ddc84"},
      {"id":"n4","label":"Narrow",    "color":"#ffd166"}
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
    "text": "Think of it like... [real analogy with <strong>key word</strong> bolded]"
  },
  "quiz": {
    "question": "A specific question testing understanding of this concept?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correctIndex": 1,
    "explanation": "Because..."
  },
  "codeExample": "# Runnable commented example\\n# Max 40 lines\\n"
}

Strict rules: exactly 4 keyPoints, exactly 4 quiz options, valid runnable codeExample."""


def fetch_concept(topic: str, lang: str, api_key: str) -> dict:
    """Fetch full concept dashboard data from Groq."""
    raw = _chat(
        system=_CONCEPT_SYSTEM,
        user=f'Topic: "{topic}". Write codeExample in {lang}.',
        api_key=api_key,
        max_tokens=1800,
    )
    # Strip accidental fences
    raw = re.sub(r"^```[a-z]*\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw.strip())
    return json.loads(raw)


# ── Code runner ───────────────────────────────────────────────────────────────

def simulate_run(code: str, lang: str, api_key: str) -> tuple[str, str]:
    """Simulate running code via Groq. Returns (output, 'success'|'error')."""
    out = _chat(
        system=(
            f"You are a {lang} interpreter. Output ONLY what stdout/stderr would show. "
            "Prefix each output line with '> '. Prefix errors with 'ERROR: '. "
            "No markdown, no explanation."
        ),
        user=f"Run this {lang} code:\n\n{code}",
        api_key=api_key,
        max_tokens=400,
    )
    return out, "error" if "ERROR:" in out else "success"


# ── AI tutor ──────────────────────────────────────────────────────────────────

def tutor_reply(
    question: str,
    topic: str,
    lang: str,
    history: list[dict],
    api_key: str,
) -> str:
    """Context-aware AI tutor with conversation memory."""
    return _chat(
        system=(
            f'You are LearnLab\'s AI tutor. The student is studying "{topic}" in {lang}. '
            f"Answer in 2-5 sentences. For code use a fenced {lang} block (max 15 lines). "
            "Be concise and encouraging. Build on previous answers."
        ),
        user=question,
        api_key=api_key,
        history=history[-8:],
        max_tokens=700,
    )
