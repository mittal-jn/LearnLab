"""
LearnLab — app.py
─────────────────
Run:  uv run streamlit run src/learnlab/app.py
      uv run learnlab
"""

from __future__ import annotations

import streamlit as st

from learnlab import agent
from learnlab import components as comp
from learnlab import styles

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
    SECRETS: dict = dict(st.secrets)
except Exception:
    st.error("⚠️ Add `GROQ_API_KEY` to `.streamlit/secrets.toml`")
    st.stop()

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "topic": "",
    "lang": "Python",
    "concept_data": None,
    "chat_history": [],
    "code": "",
    "output": "",
    "output_type": "info",
    "quiz_answered": False,
    "quiz_correct": None,
    "pending_topic": None,
}.items():
    st.session_state.setdefault(k, v)

LANGUAGES   = ["Python", "JavaScript", "TypeScript", "Java", "Go", "Rust"]
QUICK_TOPICS = [
    "Binary Search", "Recursion", "Hash Maps", "Async/Await",
    "Big O Notation", "Linked Lists", "REST APIs", "Closures",
    "Graphs", "Sorting Algorithms",
]

# ── Process any pending topic load (runs at top before render) ────────────────
if st.session_state.pending_topic:
    topic, lang_req = st.session_state.pending_topic
    st.session_state.pending_topic = None
    with st.spinner(f"⚡ Building dashboard for '{topic}'…"):
        try:
            data = agent.fetch_concept(topic, lang_req, SECRETS)
            st.session_state.update(
                topic=topic,
                lang=lang_req,
                concept_data=data,
                code=data.get("codeExample", ""),
                output=f"// Dashboard loaded: {topic}",
                output_type="info",
                quiz_answered=False,
                quiz_correct=None,
                chat_history=[],
            )
        except Exception as exc:
            st.error(f"Failed to load: {exc}")


# ── Quiz renderer ─────────────────────────────────────────────────────────────
def render_quiz(quiz: dict) -> None:
    st.markdown(comp.section_label("🎯", "Quick Check"), unsafe_allow_html=True)
    st.markdown(
        f'<div style="color:#e8eaf0;font-size:0.9rem;margin-bottom:0.7rem;line-height:1.5">'
        f'{quiz.get("question","")}</div>',
        unsafe_allow_html=True,
    )
    options = quiz.get("options", [])
    correct = quiz.get("correctIndex", 0)

    if not st.session_state.quiz_answered:
        cols = st.columns(2)
        for i, opt in enumerate(options):
            with cols[i % 2]:
                if st.button(opt, key=f"quiz_{i}", use_container_width=True):
                    st.session_state.quiz_answered = True
                    st.session_state.quiz_correct  = (i == correct)
                    st.rerun()
    else:
        for i, opt in enumerate(options):
            if i == correct:
                st.success(f"✓ {opt}")
        if not st.session_state.quiz_correct:
            st.error(f"✗ Correct: {options[correct] if options else ''}")
        st.info(f"💡 {quiz.get('explanation','')}")
        if st.button("Try again →", key="quiz_reset"):
            st.session_state.quiz_answered = False
            st.session_state.quiz_correct  = None
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

st.markdown(
    '<div class="logo-bar">'
    '<div><div class="logo-text">⚡ LearnLab</div>'
    '<div class="tagline">// interactive concept explorer · powered by Groq AI</div>'
    '</div></div>',
    unsafe_allow_html=True,
)

# ── Search row ────────────────────────────────────────────────────────────────
inp_col, lang_col, btn_col = st.columns([5, 1.2, 1])

with inp_col:
    topic_input = st.text_input(
        "topic",
        placeholder="Search any concept… e.g. 'Binary Search Trees', 'Async/Await', 'Big O'",
        label_visibility="collapsed",
        key="topic_field",
    )

with lang_col:
    lang = st.selectbox(
        "lang", LANGUAGES,
        index=LANGUAGES.index(st.session_state.lang),
        label_visibility="collapsed",
        key="lang_field",
    )

with btn_col:
    if st.button("Explore →", use_container_width=True, key="explore_btn"):
        if topic_input.strip():
            st.session_state.pending_topic = (topic_input.strip(), lang)
            st.rerun()

# ── Quick-topic chips ─────────────────────────────────────────────────────────
chip_cols = st.columns(len(QUICK_TOPICS))
for i, t in enumerate(QUICK_TOPICS):
    with chip_cols[i]:
        if st.button(t, key=f"chip_{i}"):
            st.session_state.pending_topic = (t, lang)
            st.rerun()

st.markdown(
    '<hr style="border:none;border-top:1px solid #252736;margin:0.5rem 0 1rem"/>',
    unsafe_allow_html=True,
)

# ── Two-column main layout ────────────────────────────────────────────────────
left, right = st.columns([1.08, 1], gap="medium")
concept_data = st.session_state.concept_data

# ════════════════════════════════════════════════════════════════════════
# LEFT — Visual Dashboard
# ════════════════════════════════════════════════════════════════════════
with left:
    if not concept_data:
        st.markdown(
            '<div style="text-align:center;padding:60px 20px;color:#6b7094;">'
            '<div style="font-size:3rem;opacity:0.3">🧠</div>'
            '<div style="font-family:Syne,sans-serif;font-size:1.1rem;color:#9da3c8;'
            'margin:12px 0 8px;font-weight:700">Pick a concept to explore</div>'
            '<div style="font-size:0.85rem;max-width:300px;margin:0 auto;line-height:1.6">'
            'Type any topic above and click <strong style="color:#7b61ff">Explore →</strong> '
            'or pick a quick chip below.</div></div>',
            unsafe_allow_html=True,
        )
    else:
        # Hero card
        st.markdown(
            comp.hero_card(
                concept_data["title"],
                concept_data.get("tagline", ""),
                concept_data["description"],
            ),
            unsafe_allow_html=True,
        )

        # Diagram
        st.markdown(comp.section_label("📊", "Visual Diagram"), unsafe_allow_html=True)
        svg = comp.diagram_svg(concept_data.get("diagram", {}))
        st.markdown(
            f'<div class="card" style="background:#1b1d27;padding:16px">{svg}</div>',
            unsafe_allow_html=True,
        )

        # Key points
        st.markdown(comp.section_label("⚡", "Key Points"), unsafe_allow_html=True)
        st.markdown(
            comp.key_points_card(concept_data.get("keyPoints", [])),
            unsafe_allow_html=True,
        )

        # Analogy
        analogy = concept_data.get("analogy", {})
        st.markdown(
            comp.analogy_card(analogy.get("emoji", "💡"), analogy.get("text", "")),
            unsafe_allow_html=True,
        )

        # Quiz
        st.markdown('<div class="card card-purple">', unsafe_allow_html=True)
        render_quiz(concept_data.get("quiz", {}))
        st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════
# RIGHT — Code Editor + AI Agent
# ════════════════════════════════════════════════════════════════════════
with right:
    tab_code, tab_chat = st.tabs(["💻 Code Editor", "🤖 AI Agent"])

    # ── Code tab ─────────────────────────────────────────────────────────
    with tab_code:
        st.markdown(comp.section_label("📝", "Code Editor"), unsafe_allow_html=True)

        code_val = st.text_area(
            "code",
            value=st.session_state.code,
            height=280,
            placeholder=(
                f"# Write or paste {lang} code here\n"
                "# Click 'Get Example' to auto-load\n"
                "# Click 'Run' to execute via AI simulation"
            ),
            label_visibility="collapsed",
            key="code_editor",
        )
        # sync back immediately so other widgets see latest value
        st.session_state.code = code_val

        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button("⚡ Get Example", use_container_width=True, key="get_ex",
                         disabled=not bool(concept_data)):
                st.session_state.code   = (concept_data or {}).get("codeExample", "")
                st.session_state.output = f"// Example loaded: {st.session_state.topic}"
                st.session_state.output_type = "info"
                st.rerun()

        with c2:
            run_clicked = st.button(
                "▶ Run", use_container_width=True, key="run_btn",
                disabled=not bool(code_val.strip()),
            )

        with c3:
            if st.button("✕ Clear", use_container_width=True, key="clear_btn"):
                st.session_state.code   = ""
                st.session_state.output = ""
                st.rerun()

        if run_clicked and code_val.strip():
            with st.spinner("Running…"):
                try:
                    out, otype = agent.simulate_run(code_val, lang, SECRETS)
                    st.session_state.output      = out
                    st.session_state.output_type = otype
                except Exception as exc:
                    st.session_state.output      = f"ERROR: {exc}"
                    st.session_state.output_type = "error"
            st.rerun()

        st.markdown(comp.section_label("🖥", "Console Output"), unsafe_allow_html=True)
        st.markdown(
            comp.console_output(
                st.session_state.output or "// Console ready. Run code to see output.",
                st.session_state.output_type,
            ),
            unsafe_allow_html=True,
        )

    # ── AI Agent tab ──────────────────────────────────────────────────────
    with tab_chat:
        st.markdown(comp.section_label("🤖", "AI Tutor Agent"), unsafe_allow_html=True)

        topic_ctx = st.session_state.topic or "general programming"
        n_turns   = len(st.session_state.chat_history) // 2
        st.markdown(
            f'<div style="background:#1a1538;border:1px solid #2a2550;border-radius:8px;'
            f'padding:8px 12px;margin-bottom:0.8rem;font-size:0.78rem;color:#9da3c8;'
            f'font-family:Space Mono,monospace;">'
            f'🧠 <strong style="color:#7b61ff">{topic_ctx}</strong> · {lang} · {n_turns} turns'
            f'</div>',
            unsafe_allow_html=True,
        )

        # History
        if not st.session_state.chat_history:
            st.markdown(
                '<div style="text-align:center;padding:30px 10px;color:#6b7094;font-size:0.83rem">'
                'Ask anything about the concept!<br/>'
                '<span style="color:#3a3c54">"When should I use this?", '
                '"Give me a harder example", "Explain the diagram"</span>'
                '</div>',
                unsafe_allow_html=True,
            )
        else:
            for msg in st.session_state.chat_history:
                st.markdown(
                    comp.chat_bubble(msg["role"], msg["content"]),
                    unsafe_allow_html=True,
                )

        # Input row
        q_col, send_col = st.columns([5, 1])
        with q_col:
            user_q = st.text_input(
                "Ask", placeholder="Ask a follow-up question…",
                label_visibility="collapsed", key="chat_q",
            )
        with send_col:
            ask_clicked = st.button("↑ Ask", use_container_width=True, key="ask_btn")

        if ask_clicked and user_q.strip():
            history = list(st.session_state.chat_history)
            history.append({"role": "user", "content": user_q.strip()})
            with st.spinner("Thinking…"):
                try:
                    answer = agent.tutor_reply(
                        user_q.strip(), topic_ctx, lang, history[:-1], SECRETS
                    )
                    history.append({"role": "assistant", "content": answer})
                except Exception as exc:
                    history.append({"role": "assistant", "content": f"Error: {exc}"})
            st.session_state.chat_history = history
            st.rerun()

        # Suggested questions (only when topic loaded + no chat yet)
        if concept_data and not st.session_state.chat_history:
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
                                ans = agent.tutor_reply(s, t, lang, [], SECRETS)
                                history.append({"role": "assistant", "content": ans})
                            except Exception as exc:
                                history.append({"role": "assistant", "content": f"Error: {exc}"})
                        st.session_state.chat_history = history
                        st.rerun()

        if st.session_state.chat_history:
            if st.button("🗑 Clear chat", key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()
