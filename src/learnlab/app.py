"""
LearnLab — app.py
─────────────────
Streamlit entry point. All AI logic lives in learnlab.agent,
rendering helpers in learnlab.components, styles in learnlab.styles.

Run locally:
    uv run streamlit run src/learnlab/app.py
Or via the CLI script:
    uv run learnlab
"""

from __future__ import annotations

import streamlit as st

# When executing `src/learnlab/app.py` directly, `src/` might not be on
# `sys.path` yet. This keeps imports reliable in both installed and dev modes.
try:
    from learnlab import agent, components as comp, styles
except ModuleNotFoundError:  # pragma: no cover
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from learnlab import agent, components as comp, styles


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LearnLab ⚡",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

styles.inject(st)

# ── API key ───────────────────────────────────────────────────────────────────
try:
    API_KEY: str = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
    st.error("⚠️ Add `ANTHROPIC_API_KEY` to `.streamlit/secrets.toml`")
    st.stop()

# ── Session state ─────────────────────────────────────────────────────────────
DEFAULTS: dict = {
    "topic": "",
    "lang": "Python",
    "concept_data": None,
    "chat_history": [],
    "code": "",
    "output": "",
    "output_type": "info",
    "quiz_answered": False,
    "quiz_correct": None,
}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)

# ── Constants ─────────────────────────────────────────────────────────────────
LANGUAGES = ["Python", "JavaScript", "TypeScript", "Java", "Go", "Rust"]
QUICK_TOPICS = [
    "Binary Search",
    "Recursion",
    "Hash Maps",
    "Async/Await",
    "Big O Notation",
    "Linked Lists",
    "REST APIs",
    "Closures",
    "Graphs",
    "Sorting Algorithms",
]


# ── Helpers ───────────────────────────────────────────────────────────────────


def load_topic(topic: str, lang: str) -> None:
    """Fetch concept data and update session state."""
    with st.spinner(f"⚡ Building dashboard for '{topic}'…"):
        try:
            data = agent.fetch_concept(topic, lang, API_KEY)
            st.session_state.update(
                topic=topic,
                lang=lang,
                concept_data=data,
                code=data.get("codeExample", ""),
                output=f"// Dashboard loaded: {topic}",
                output_type="info",
                quiz_answered=False,
                quiz_correct=None,
                chat_history=[],
            )
        except Exception as exc:  # noqa: BLE001
            st.error(f"Failed to load concept: {exc}")


def render_quiz(quiz: dict) -> None:
    st.markdown(comp.section_label("🎯", "Quick Check"), unsafe_allow_html=True)
    st.markdown(
        f'<div style="color:#e8eaf0;font-size:0.9rem;margin-bottom:0.7rem;line-height:1.5">'
        f'{quiz["question"]}</div>',
        unsafe_allow_html=True,
    )
    if not st.session_state.quiz_answered:
        cols = st.columns(2)
        for i, opt in enumerate(quiz["options"]):
            with cols[i % 2]:
                if st.button(opt, key=f"quiz_{i}", use_container_width=True):
                    st.session_state.quiz_answered = True
                    st.session_state.quiz_correct = i == quiz["correctIndex"]
                    st.rerun()
    else:
        for i, opt in enumerate(quiz["options"]):
            if i == quiz["correctIndex"]:
                st.success(f"✓ {opt}")
        if not st.session_state.quiz_correct:
            st.error(f"✗ Correct answer: {quiz['options'][quiz['correctIndex']]}")
        st.info(f"💡 {quiz['explanation']}")
        if st.button("Try again →", key="quiz_reset"):
            st.session_state.quiz_answered = False
            st.session_state.quiz_correct = None
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# ── Layout ────────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

# Logo
st.markdown(
    '<div class="logo-bar">'
    '<div><div class="logo-text">⚡ LearnLab</div>'
    '<div class="tagline">// interactive concept explorer · powered by Claude AI</div></div>'
    "</div>",
    unsafe_allow_html=True,
)

# ── Search bar ───────────────────────────────────────────────────────────────
inp_col, lang_col, btn_col = st.columns([5, 1.2, 1])

with inp_col:
    topic_input = st.text_input(
        "topic",
        value=st.session_state.topic,
        placeholder="Search any concept… e.g. 'Binary Search Trees', 'Async/Await', 'Big O'",
        label_visibility="collapsed",
        key="topic_field",
    )

with lang_col:
    lang = st.selectbox(
        "lang",
        LANGUAGES,
        index=LANGUAGES.index(st.session_state.lang),
        label_visibility="collapsed",
        key="lang_field",
    )

with btn_col:
    explore_clicked = st.button("Explore →", use_container_width=True)

if explore_clicked and topic_input.strip():
    load_topic(topic_input.strip(), lang)
    st.rerun()

# ── Quick chips ───────────────────────────────────────────────────────────────
chip_cols = st.columns(len(QUICK_TOPICS))
for i, t in enumerate(QUICK_TOPICS):
    with chip_cols[i]:
        if st.button(t, key=f"chip_{i}", use_container_width=False):
            load_topic(t, lang)
            st.rerun()

st.markdown(
    '<hr style="border:none;border-top:1px solid #252736;margin:0.5rem 0 1rem"/>',
    unsafe_allow_html=True,
)

# ── Two-column layout ─────────────────────────────────────────────────────────
left, right = st.columns([1.08, 1], gap="medium")

# ════════════════════════════════════════════════════════════════════════
# LEFT — Visual Dashboard
# ════════════════════════════════════════════════════════════════════════
with left:
    data = st.session_state.concept_data

    if not data:
        st.markdown(
            """
            <div style="text-align:center;padding:60px 20px;color:#6b7094;">
              <div style="font-size:3rem;opacity:0.3">🧠</div>
              <div style="font-family:Syne,sans-serif;font-size:1.1rem;color:#9da3c8;
                          margin:12px 0 8px;font-weight:700">Pick a concept to explore</div>
              <div style="font-size:0.85rem;max-width:300px;margin:0 auto;line-height:1.6">
                Type any programming or CS topic above and click
                <strong style="color:#7b61ff">Explore →</strong> to generate a visual dashboard
                with diagrams, key points, analogies, and an AI tutor.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Hero
        st.markdown(
            comp.hero_card(data["title"], data.get("tagline", ""), data["description"]),
            unsafe_allow_html=True,
        )

        # Diagram
        st.markdown(comp.section_label("📊", "Visual Diagram"), unsafe_allow_html=True)
        svg = comp.diagram_svg(data.get("diagram", {}))
        st.markdown(
            f'<div class="card" style="background:#1b1d27;padding:16px">{svg}</div>',
            unsafe_allow_html=True,
        )

        # Key points
        st.markdown(comp.section_label("⚡", "Key Points"), unsafe_allow_html=True)
        st.markdown(comp.key_points_card(data.get("keyPoints", [])), unsafe_allow_html=True)

        # Analogy
        analogy = data.get("analogy", {})
        st.markdown(
            comp.analogy_card(analogy.get("emoji", "💡"), analogy.get("text", "")),
            unsafe_allow_html=True,
        )

        # Quiz
        st.markdown('<div class="card card-purple">', unsafe_allow_html=True)
        render_quiz(data.get("quiz", {}))
        st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# RIGHT — Code Editor + AI Agent
# ════════════════════════════════════════════════════════════════════════
with right:
    tab_code, tab_chat = st.tabs(["💻 Code Editor", "🤖 AI Agent"])

    # ── Code Editor ──────────────────────────────────────────────────────
    with tab_code:
        st.markdown(comp.section_label("📝", "Code Editor"), unsafe_allow_html=True)

        code_val = st.text_area(
            "code",
            value=st.session_state.code,
            height=280,
            placeholder=(
                f"# Write or paste {st.session_state.lang} code here\n"
                "# Click 'Get Example' to load a concept example\n"
                "# Click 'Run' to execute via AI simulation"
            ),
            label_visibility="collapsed",
            key="code_editor",
        )
        st.session_state.code = code_val

        c1, c2, c3 = st.columns([1, 1, 1])

        with c1:
            if st.button(
                "⚡ Get Example",
                use_container_width=True,
                key="get_ex",
                disabled=not bool(data),
            ):
                st.session_state.code = (data or {}).get("codeExample", "")
                st.session_state.output = f"// Example loaded: {st.session_state.topic}"
                st.session_state.output_type = "info"
                st.rerun()

        with c2:
            st.markdown('<div class="run-btn">', unsafe_allow_html=True)
            run_clicked = st.button(
                "▶ Run",
                use_container_width=True,
                key="run_btn",
                disabled=not bool(code_val.strip()),
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with c3:
            if st.button("✕ Clear", use_container_width=True, key="clear_btn"):
                st.session_state.code = ""
                st.session_state.output = ""
                st.rerun()

        if run_clicked and code_val.strip():
            with st.spinner("Running…"):
                try:
                    out, otype = agent.simulate_run(code_val, lang, API_KEY)
                    st.session_state.output = out
                    st.session_state.output_type = otype
                except Exception as exc:  # noqa: BLE001
                    st.session_state.output = f"ERROR: {exc}"
                    st.session_state.output_type = "error"
            st.rerun()

        # Console
        st.markdown(comp.section_label("🖥", "Console Output"), unsafe_allow_html=True)
        raw_out = st.session_state.output or "// Console ready. Run code to see output."
        st.markdown(
            comp.console_output(raw_out, st.session_state.output_type),
            unsafe_allow_html=True,
        )

    # ── AI Agent ─────────────────────────────────────────────────────────
    with tab_chat:
        st.markdown(comp.section_label("🤖", "AI Tutor Agent"), unsafe_allow_html=True)

        topic_ctx = st.session_state.topic or "general programming"
        n_turns = len(st.session_state.chat_history) // 2
        st.markdown(
            f'<div style="background:#1a1538;border:1px solid #2a2550;border-radius:8px;'
            f'padding:8px 12px;margin-bottom:0.8rem;font-size:0.78rem;color:#9da3c8;'
            f'font-family:Space Mono,monospace;">'
            f"🧠 Context: <strong style='color:#7b61ff'>{topic_ctx}</strong> · "
            f"{lang} · {n_turns} turns"
            f"</div>",
            unsafe_allow_html=True,
        )

        # Chat history
        if not st.session_state.chat_history:
            st.markdown(
                '<div style="text-align:center;padding:30px 10px;color:#6b7094;font-size:0.83rem">'
                "Ask anything about the concept!<br/>"
                '<span style="color:#3a3c54">e.g. "When should I use this?", '
                '"Give me a harder example", "Explain the diagram"</span>'
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            for msg in st.session_state.chat_history:
                st.markdown(
                    comp.chat_bubble(msg["role"], msg["content"]),
                    unsafe_allow_html=True,
                )

        # Input
        q_col, send_col = st.columns([5, 1])
        with q_col:
            user_q = st.text_input(
                "Ask",
                placeholder="Ask a follow-up question…",
                label_visibility="collapsed",
                key="chat_q",
            )
        with send_col:
            ask_clicked = st.button("↑ Ask", use_container_width=True, key="ask_btn")

        if ask_clicked and user_q.strip():
            history = list(st.session_state.chat_history)
            history.append({"role": "user", "content": user_q.strip()})
            with st.spinner("Thinking…"):
                try:
                    answer = agent.tutor_reply(
                        user_q.strip(),
                        st.session_state.topic,
                        lang,
                        history[:-1],
                        API_KEY,
                    )
                    history.append({"role": "assistant", "content": answer})
                except Exception as exc:  # noqa: BLE001
                    history.append({"role": "assistant", "content": f"Error: {exc}"})
            st.session_state.chat_history = history
            st.rerun()

        # Suggested questions
        if data and not st.session_state.chat_history:
            t = st.session_state.topic
            suggestions = [
                f"When should I use {t}?",
                f"Common mistakes with {t}?",
                f"Give me a harder {t} example",
                "Explain the diagram step by step",
            ]
            st.markdown(
                '<div style="margin-top:0.6rem;font-size:0.72rem;color:#6b7094;'
                'font-family:Space Mono,monospace;margin-bottom:0.3rem">SUGGESTED</div>',
                unsafe_allow_html=True,
            )
            sg_cols = st.columns(2)
            for i, s in enumerate(suggestions):
                with sg_cols[i % 2]:
                    if st.button(s, key=f"sg_{i}", use_container_width=True):
                        history = [{"role": "user", "content": s}]
                        with st.spinner("Thinking…"):
                            try:
                                ans = agent.tutor_reply(s, t, lang, [], API_KEY)
                                history.append({"role": "assistant", "content": ans})
                            except Exception as exc:  # noqa: BLE001
                                history.append({"role": "assistant", "content": f"Error: {exc}"})
                        st.session_state.chat_history = history
                        st.rerun()

        if st.session_state.chat_history:
            if st.button("🗑 Clear chat", key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()

