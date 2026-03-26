"""
LearnLab — app.py
─────────────────
Streamlit UI. AI logic → agent.py, HTML → components.py, CSS → styles.py.

Run:  uv run learnlab
  or: uv run streamlit run src/learnlab/app.py
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
styles.inject()

# ── API key ───────────────────────────────────────────────────────────────────
try:
    API_KEY: str = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("⚠️ Add `GROQ_API_KEY` to `.streamlit/secrets.toml` — get a free key at console.groq.com")
    st.stop()

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "topic":        "",
    "lang":         "Python",
    "data":         None,
    "code":         "",
    "output":       "",
    "output_type":  "info",
    "chat":         [],
    "quiz_done":    False,
    "quiz_correct": None,
    "pending":      None,   # (topic, lang) waiting to be fetched
}.items():
    st.session_state.setdefault(k, v)

LANGUAGES    = ["Python", "JavaScript", "TypeScript", "Java", "Go", "Rust"]
QUICK_TOPICS = [
    "Binary Search", "Recursion", "Hash Maps", "Async/Await",
    "Big O Notation", "Linked Lists", "REST APIs", "Closures",
    "Graphs", "Sorting Algorithms",
]

# ── Fetch pending topic (top of script so spinner shows before render) ────────
if st.session_state.pending:
    topic, lang_req = st.session_state.pending
    st.session_state.pending = None
    with st.spinner(f"⚡ Building dashboard for '{topic}'…"):
        try:
            data = agent.fetch_concept(topic, lang_req, API_KEY)
            st.session_state.update(
                topic=topic, lang=lang_req, data=data,
                code=data.get("codeExample", ""),
                output=f"// Loaded: {topic}", output_type="info",
                chat=[], quiz_done=False, quiz_correct=None,
            )
        except Exception as exc:
            st.error(f"Failed to load '{topic}': {exc}")


# ── Quiz renderer ─────────────────────────────────────────────────────────────
def render_quiz(quiz: dict) -> None:
    st.markdown(comp.section_label("🎯", "Quick Check"), unsafe_allow_html=True)
    st.markdown(
        f'<div style="color:#e8eaf0;font-size:0.9rem;line-height:1.5;margin-bottom:0.7rem">'
        f'{quiz.get("question","")}</div>',
        unsafe_allow_html=True,
    )
    opts    = quiz.get("options", [])
    correct = quiz.get("correctIndex", 0)

    if not st.session_state.quiz_done:
        cols = st.columns(2)
        for i, opt in enumerate(opts):
            with cols[i % 2]:
                if st.button(opt, key=f"q{i}", use_container_width=True):
                    st.session_state.quiz_done    = True
                    st.session_state.quiz_correct = (i == correct)
                    st.rerun()
    else:
        for i, opt in enumerate(opts):
            if i == correct:
                st.success(f"✓ {opt}")
        if not st.session_state.quiz_correct:
            st.error(f"✗ Correct: {opts[correct] if opts else ''}")
        st.info(f"💡 {quiz.get('explanation','')}")
        if st.button("Try again →", key="quiz_retry"):
            st.session_state.quiz_done    = False
            st.session_state.quiz_correct = None
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

# Logo
st.markdown(
    '<div class="logo-bar">'
    '<div class="logo-text">⚡ LearnLab</div>'
    '<div class="tagline">// interactive concept explorer · powered by Groq AI</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ── Search row ────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns([5, 1.2, 1])
with c1:
    topic_input = st.text_input(
        "topic", placeholder="Search any concept… e.g. 'Binary Search', 'Async/Await', 'Big O'",
        label_visibility="collapsed", key="topic_field",
    )
with c2:
    lang = st.selectbox(
        "lang", LANGUAGES,
        index=LANGUAGES.index(st.session_state.lang),
        label_visibility="collapsed", key="lang_field",
    )
with c3:
    if st.button("Explore →", use_container_width=True) and topic_input.strip():
        st.session_state.pending = (topic_input.strip(), lang)
        st.rerun()

# ── Quick-topic chips ─────────────────────────────────────────────────────────
chip_cols = st.columns(len(QUICK_TOPICS))
for i, t in enumerate(QUICK_TOPICS):
    with chip_cols[i]:
        if st.button(t, key=f"chip_{i}"):
            st.session_state.pending = (t, lang)
            st.rerun()

st.markdown('<hr style="border:none;border-top:1px solid #252736;margin:0.4rem 0 1rem"/>', unsafe_allow_html=True)

# ── Two-column layout ─────────────────────────────────────────────────────────
left, right = st.columns([1.08, 1], gap="medium")
data = st.session_state.data

# ════════════════════════════════════════════════════════════════════════
# LEFT — Visual Dashboard
# ════════════════════════════════════════════════════════════════════════
with left:
    if not data:
        st.markdown(
            '<div style="text-align:center;padding:60px 20px;color:#6b7094">'
            '<div style="font-size:3rem;opacity:0.25">🧠</div>'
            '<div style="font-family:Syne,sans-serif;font-size:1.1rem;color:#9da3c8;'
            'margin:12px 0 8px;font-weight:700">Pick a concept to explore</div>'
            '<div style="font-size:0.85rem;max-width:280px;margin:0 auto;line-height:1.6">'
            'Type any CS topic and click <strong style="color:#7b61ff">Explore →</strong> '
            'or tap a quick chip above.</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(comp.hero_card(data["title"], data.get("tagline",""), data["description"]), unsafe_allow_html=True)
        st.markdown(comp.diagram_card(data.get("diagram", {})), unsafe_allow_html=True)
        st.markdown(comp.key_points_card(data.get("keyPoints", [])), unsafe_allow_html=True)
        analogy = data.get("analogy", {})
        st.markdown(comp.analogy_card(analogy.get("emoji","💡"), analogy.get("text","")), unsafe_allow_html=True)
        st.markdown('<div class="card card-purple">', unsafe_allow_html=True)
        render_quiz(data.get("quiz", {}))
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════
# RIGHT — Code Editor + AI Agent
# ════════════════════════════════════════════════════════════════════════
with right:
    tab_code, tab_chat = st.tabs(["💻 Code Editor", "🤖 AI Agent"])

    # ── Code tab ─────────────────────────────────────────────────────────
    with tab_code:
        st.markdown(comp.section_label("📝", "Editor"), unsafe_allow_html=True)

        code_val = st.text_area(
            "code", value=st.session_state.code, height=290,
            placeholder=f"# Write {lang} code here, or click ⚡ Get Example",
            label_visibility="collapsed", 
        )
        st.session_state.code = code_val

        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("⚡ Get Example", use_container_width=True, disabled=not data):
                st.session_state.code   = (data or {}).get("codeExample", "")
                st.session_state.output = f"// Example loaded: {st.session_state.topic}"
                st.session_state.output_type = "info"
                st.rerun()
        with b2:
            run = st.button("▶ Run", use_container_width=True, disabled=not code_val.strip())
        with b3:
            if st.button("✕ Clear", use_container_width=True):
                st.session_state.code = ""
                st.session_state.output = ""
                st.rerun()

        if run and code_val.strip():
            with st.spinner("Running…"):
                try:
                    out, otype = agent.simulate_run(code_val, lang, API_KEY)
                    st.session_state.output      = out
                    st.session_state.output_type = otype
                except Exception as exc:
                    st.session_state.output      = f"ERROR: {exc}"
                    st.session_state.output_type = "error"
            st.rerun()

        st.markdown(comp.section_label("🖥", "Console"), unsafe_allow_html=True)
        st.markdown(
            comp.console_out(st.session_state.output or "// Ready. Run code to see output.", st.session_state.output_type),
            unsafe_allow_html=True,
        )

    # ── AI Agent tab ──────────────────────────────────────────────────────
    with tab_chat:
        st.markdown(comp.section_label("🤖", "AI Tutor"), unsafe_allow_html=True)

        topic_ctx = st.session_state.topic or "general programming"
        st.markdown(
            f'<div style="background:#1a1538;border:1px solid #2a2550;border-radius:8px;'
            f'padding:7px 12px;margin-bottom:0.7rem;font-size:0.75rem;color:#9da3c8;'
            f'font-family:Space Mono,monospace">'
            f'🧠 <strong style="color:#7b61ff">{topic_ctx}</strong> · {lang} · '
            f'{len(st.session_state.chat)//2} turns</div>',
            unsafe_allow_html=True,
        )

        # History
        if not st.session_state.chat:
            st.markdown(
                '<div style="text-align:center;padding:24px 10px;color:#6b7094;font-size:0.83rem">'
                'Ask anything about the concept!<br>'
                '<span style="color:#3a3c54;font-size:0.78rem">'
                '"When should I use this?" · "Give me a harder example"</span></div>',
                unsafe_allow_html=True,
            )
        else:
            for msg in st.session_state.chat:
                st.markdown(comp.chat_bubble(msg["role"], msg["content"]), unsafe_allow_html=True)

        # Input
        qc, sc = st.columns([5, 1])
        with qc:
            user_q = st.text_input("q", placeholder="Ask a follow-up question…",
                                   label_visibility="collapsed", key="chat_input")
        with sc:
            ask = st.button("↑ Ask", use_container_width=True)

        if ask and user_q.strip():
            history = list(st.session_state.chat)
            history.append({"role": "user", "content": user_q.strip()})
            with st.spinner("Thinking…"):
                try:
                    ans = agent.tutor_reply(user_q.strip(), topic_ctx, lang, history[:-1], API_KEY)
                    history.append({"role": "assistant", "content": ans})
                except Exception as exc:
                    history.append({"role": "assistant", "content": f"Error: {exc}"})
            st.session_state.chat = history
            st.rerun()

        # Suggested prompts (shown only before first message)
        if data and not st.session_state.chat:
            t = st.session_state.topic
            prompts = [
                f"When should I use {t}?",
                f"Common mistakes with {t}?",
                f"Harder {t} example please",
                "Explain the diagram",
            ]
            st.markdown('<div style="margin-top:0.5rem;font-size:0.68rem;color:#6b7094;font-family:Space Mono,monospace;margin-bottom:0.3rem">SUGGESTED</div>', unsafe_allow_html=True)
            pc1, pc2 = st.columns(2)
            for i, p in enumerate(prompts):
                with (pc1 if i % 2 == 0 else pc2):
                    if st.button(p, key=f"p{i}", use_container_width=True):
                        h = [{"role": "user", "content": p}]
                        with st.spinner("Thinking…"):
                            try:
                                ans = agent.tutor_reply(p, t, lang, [], API_KEY)
                                h.append({"role": "assistant", "content": ans})
                            except Exception as exc:
                                h.append({"role": "assistant", "content": f"Error: {exc}"})
                        st.session_state.chat = h
                        st.rerun()

        if st.session_state.chat:
            if st.button("🗑 Clear chat", key="clear_chat"):
                st.session_state.chat = []
                st.rerun()
