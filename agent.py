"""
learnlab.agent
──────────────
All Claude AI interactions: concept fetching, code simulation, and tutor chat.
Each function is a pure call → response with no Streamlit dependency.
"""

from __future__ import annotations

import json
import re

import anthropic


def _client(api_key: str) -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=api_key)


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
  "codeExample": "# Commented example in the requested language\\n# Max 40 lines\\n"
}
Rules: exactly 4 keyPoints, exactly 4 quiz options, codeExample must be valid runnable code."""


def fetch_concept(topic: str, lang: str, api_key: str) -> dict:
    """Fetch a full concept dashboard JSON from Claude."""
    client = _client(api_key)
    resp = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1800,
        system=CONCEPT_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": f'Topic: "{topic}" — Language: {lang}. Write the codeExample in {lang}.',
            }
        ],
    )
    raw = resp.content[0].text.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


# ── Code runner ───────────────────────────────────────────────────────────────

def simulate_run(code: str, lang: str, api_key: str) -> tuple[str, str]:
    """
    Simulate executing code via Claude.
    Returns (output_text, status) where status is 'success' | 'error'.
    """
    client = _client(api_key)
    resp = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=(
            f"You are a {lang} interpreter. Return ONLY what stdout/stderr would show. "
            "Prefix output lines with '> ', errors with 'ERROR: '. No explanation, no markdown."
        ),
        messages=[{"role": "user", "content": f"Run this {lang} code:\n\n{code}"}],
    )
    output = resp.content[0].text.strip()
    status = "error" if "ERROR:" in output else "success"
    return output, status


# ── AI tutor agent ────────────────────────────────────────────────────────────

def tutor_reply(
    question: str,
    topic: str,
    lang: str,
    history: list[dict],
    api_key: str,
) -> str:
    """
    Context-aware AI tutor. Maintains conversation history across turns.
    history = [{"role": "user"|"assistant", "content": str}, ...]
    """
    client = _client(api_key)
    system = (
        f'You are LearnLab\'s AI tutor. The student is studying "{topic}" in {lang}.\n\n'
        "Your role:\n"
        f"- Answer follow-up questions clearly (2-5 sentences)\n"
        f"- If asked for code, provide a short {lang} snippet (≤15 lines) in a fenced code block\n"
        "- Be pedagogical and encouraging\n"
        "- Reference the current topic when relevant\n"
        "- Build on previous answers — you have full conversation memory"
    )

    # Keep last 8 messages for context window efficiency
    messages = [
        {"role": m["role"], "content": m["content"]}
        for m in history[-8:]
    ]
    messages.append({"role": "user", "content": question})

    resp = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=700,
        system=system,
        messages=messages,
    )
    return resp.content[0].text.strip()
