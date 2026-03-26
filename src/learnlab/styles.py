"""learnlab.styles — inject all custom CSS into Streamlit."""
from __future__ import annotations
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0b0c10; color: #e8eaf0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 1.5rem 2rem !important; max-width: 100% !important; }

/* Logo */
.logo-bar { padding-bottom: 0.8rem; border-bottom: 1px solid #252736; margin-bottom: 1rem; }
.logo-text { font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 800;
  background: linear-gradient(135deg, #7b61ff, #00e5c0);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.tagline { font-size: 0.78rem; color: #6b7094; font-family: 'Space Mono', monospace; }

/* Cards */
.card { background: #13141a; border: 1px solid #252736; border-radius: 12px;
  padding: 1rem 1.2rem; margin-bottom: 0.8rem; }
.card-accent { background: linear-gradient(135deg,#1a1538,#121624,#0f1820); border-color: #2a2550; }
.card-green  { background: linear-gradient(135deg,#1a2818,#121a10); border-color: #2a3828; }
.card-purple { background: linear-gradient(135deg,#1a1028,#100d18); border-color: #28203a; }
.card-label  { font-family: 'Space Mono', monospace; font-size: 0.68rem;
  text-transform: uppercase; letter-spacing: 0.1em; color: #6b7094; margin-bottom: 0.5rem; }

.concept-title { font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 800;
  background: linear-gradient(135deg, #fff 40%, #7b61ff);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  line-height: 1.2; margin-bottom: 0.3rem; }
.concept-tag  { font-size: 0.78rem; color: #7b61ff; font-family: 'Space Mono', monospace; margin-bottom: 0.5rem; }
.concept-desc { font-size: 0.88rem; color: #9da3c8; line-height: 1.65; }

/* Key points */
.points-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.point { background: #1b1d27; border-radius: 8px; padding: 10px 12px; }
.point-label { font-size: 0.67rem; font-family: 'Space Mono', monospace; color: #6b7094;
  text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 3px; }
.point-value { font-size: 0.85rem; color: #e8eaf0; }
.p1 { border-left: 3px solid #7b61ff; }
.p2 { border-left: 3px solid #00e5c0; }
.p3 { border-left: 3px solid #ff6b6b; }
.p4 { border-left: 3px solid #ffd166; }

/* Diagram */
.diagram-wrap { background: #1b1d27; border-radius: 8px; padding: 12px; }

/* Analogy */
.analogy-box  { display: flex; gap: 12px; align-items: flex-start; }
.analogy-emoji{ font-size: 1.5rem; flex-shrink: 0; }
.analogy-text { font-size: 0.87rem; color: #9da3c8; line-height: 1.6; font-style: italic; }
.analogy-text strong { color: #3ddc84; font-style: normal; }

/* Section label */
.section-label { font-family: 'Space Mono', monospace; font-size: 0.68rem;
  text-transform: uppercase; letter-spacing: 0.1em; color: #6b7094;
  display: flex; align-items: center; gap: 6px; margin-bottom: 0.4rem; }
.section-label::after { content: ''; flex: 1; height: 1px; background: #252736; }

/* Chat */
.msg-user { background: #1b1d27; border: 1px solid #252736; border-radius: 10px 10px 4px 10px;
  padding: 10px 14px; margin: 6px 0; font-size: 0.87rem; margin-left: 15%; }
.msg-ai   { background: #1a1538; border: 1px solid #2a2550; border-radius: 10px 10px 10px 4px;
  padding: 10px 14px; margin: 6px 0; font-size: 0.87rem; line-height: 1.6; margin-right: 5%; }
.msg-role { font-size: 0.65rem; font-family: 'Space Mono', monospace;
  text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; }

/* Console */
.console { background: #070809; border: 1px solid #252736; border-radius: 8px;
  padding: 12px 14px; font-family: 'Space Mono', monospace; font-size: 0.78rem;
  line-height: 1.7; min-height: 80px; max-height: 240px; overflow-y: auto;
  white-space: pre-wrap; word-break: break-word; }

/* Widget overrides */
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
  background: #13141a !important; border: 1px solid #252736 !important;
  border-radius: 8px !important; color: #e8eaf0 !important; }
.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
  border-color: #7b61ff !important; box-shadow: 0 0 0 2px #7b61ff22 !important; }
.stSelectbox>div>div { background: #13141a !important; border: 1px solid #252736 !important;
  border-radius: 8px !important; }
.stButton>button { background: #7b61ff !important; color: #fff !important;
  border: none !important; border-radius: 8px !important; font-weight: 500 !important; }
.stButton>button:hover { background: #6b52e8 !important; transform: translateY(-1px); }
.stTabs [data-baseweb="tab-list"] { background: #13141a; border-radius: 8px; padding: 4px; }
.stTabs [data-baseweb="tab"]      { color: #6b7094; border-radius: 6px; }
.stTabs [aria-selected="true"]    { background: #1b1d27 !important; color: #e8eaf0 !important; }
</style>
"""


def inject() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
