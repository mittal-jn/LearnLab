"""learnlab.styles — inject all custom CSS into Streamlit."""
from __future__ import annotations
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@700;800&family=Inter:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #07070f; color: #f0f0f4; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.8rem 2.2rem 3rem !important; max-width: 100% !important; }

/* ── Logo ── */
.logo-bar {
  padding-bottom: 1.2rem;
  border-bottom: 1px solid #111120;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.85rem;
}
.logo-mark {
  width: 30px; height: 30px;
  background: linear-gradient(135deg, #7c3aed, #a78bfa);
  border-radius: 8px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
  flex-shrink: 0;
  box-shadow: 0 0 18px rgba(124,58,237,0.45);
}
.logo-text {
  font-family: 'Syne', sans-serif;
  font-size: 1.4rem;
  font-weight: 800;
  background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 70%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.025em;
}
.tagline {
  font-size: 0.7rem;
  color: #2e2e42;
  font-family: 'Space Mono', monospace;
  letter-spacing: 0.06em;
  margin-left: auto;
}

/* ── Cards ── */
.card {
  background: linear-gradient(160deg, #0e0e1c 0%, #0c0c18 100%);
  border: 1px solid #17172a;
  border-radius: 16px;
  padding: 1.2rem 1.4rem;
  margin-bottom: 0.9rem;
  box-shadow: 0 4px 28px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.03);
}
.card-accent {
  background: linear-gradient(160deg, #0f0c1e 0%, #0c0918 100%);
  border-color: #1e1638;
  box-shadow: 0 4px 32px rgba(124,58,237,0.1), inset 0 1px 0 rgba(167,139,250,0.05);
}
.card-green {
  background: linear-gradient(160deg, #09140e 0%, #070f0a 100%);
  border-color: #122418;
  box-shadow: 0 4px 32px rgba(16,185,129,0.07), inset 0 1px 0 rgba(52,211,153,0.04);
}
.card-purple {
  background: linear-gradient(160deg, #0f0b1e 0%, #0c0816 100%);
  border-color: #1c1132;
  box-shadow: 0 4px 32px rgba(139,92,246,0.09), inset 0 1px 0 rgba(196,181,253,0.04);
}
.card-label {
  font-family: 'Space Mono', monospace;
  font-size: 0.61rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: #2e2e42;
  margin-bottom: 0.65rem;
}

.concept-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.65rem;
  font-weight: 800;
  background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.15;
  margin-bottom: 0.35rem;
  letter-spacing: -0.025em;
}
.concept-tag {
  font-size: 0.7rem;
  color: #8b5cf6;
  font-family: 'Space Mono', monospace;
  margin-bottom: 0.65rem;
  letter-spacing: 0.1em;
}
.concept-desc {
  font-size: 0.87rem;
  color: #8888a0;
  line-height: 1.78;
  font-weight: 400;
}

/* ── Key points ── */
.points-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.point {
  background: #0b0b17;
  border-radius: 10px;
  padding: 12px 14px;
  border: 1px solid #17172a;
}
.point-label {
  font-size: 0.6rem;
  font-family: 'Space Mono', monospace;
  color: #2e2e42;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 5px;
}
.point-value { font-size: 0.84rem; color: #e0e0ee; font-weight: 500; }
.p1 { border-left: 2px solid #8b5cf6; }
.p2 { border-left: 2px solid #06b6d4; }
.p3 { border-left: 2px solid #f43f5e; }
.p4 { border-left: 2px solid #f59e0b; }

/* ── Diagram ── */
.diagram-wrap {
  background: #040408;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #111120;
  box-shadow: inset 0 2px 14px rgba(0,0,0,0.7);
}

/* ── Analogy ── */
.analogy-box { display: flex; gap: 14px; align-items: flex-start; }
.analogy-emoji { font-size: 1.6rem; flex-shrink: 0; }
.analogy-text { font-size: 0.86rem; color: #8888a0; line-height: 1.75; }
.analogy-text strong { color: #34d399; font-style: normal; font-weight: 600; }

/* ── Section label ── */
.section-label {
  font-family: 'Space Mono', monospace;
  font-size: 0.6rem;
  text-transform: uppercase;
  letter-spacing: 0.17em;
  color: #252538;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 0.55rem;
}
.section-label::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, #17172a 0%, transparent 100%);
}

/* ── Empty state ── */
.empty-state { text-align: center; padding: 80px 20px; }
.empty-icon { font-size: 2.6rem; margin-bottom: 16px; opacity: 0.35; }
.empty-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.05rem;
  font-weight: 800;
  color: #232335;
  margin-bottom: 10px;
  letter-spacing: -0.01em;
}
.empty-sub {
  font-size: 0.78rem;
  color: #1e1e30;
  max-width: 250px;
  margin: 0 auto;
  line-height: 1.7;
}

/* ── Chat ── */
.msg-user {
  background: #0e0e1c;
  border: 1px solid #17172a;
  border-radius: 12px 12px 4px 12px;
  padding: 10px 14px;
  margin: 8px 0;
  font-size: 0.86rem;
  margin-left: 20%;
}
.msg-ai {
  background: linear-gradient(135deg, #0d0a1e, #0b081a);
  border: 1px solid #1c1438;
  border-radius: 12px 12px 12px 4px;
  padding: 10px 14px;
  margin: 8px 0;
  font-size: 0.86rem;
  line-height: 1.7;
  margin-right: 8%;
}
.msg-role {
  font-size: 0.58rem;
  font-family: 'Space Mono', monospace;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 5px;
  color: #2e2e42;
}

/* ── Console ── */
.console {
  background: #030306;
  border: 1px solid #111120;
  border-radius: 10px;
  padding: 14px 16px;
  font-family: 'Space Mono', monospace;
  font-size: 0.75rem;
  line-height: 1.82;
  min-height: 90px;
  max-height: 240px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-word;
  box-shadow: inset 0 2px 14px rgba(0,0,0,0.8);
}

/* ── Widget overrides ── */
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
  background: #0e0e1c !important;
  border: 1px solid #1c1c2e !important;
  border-radius: 10px !important;
  color: #f0f0f4 !important;
  font-family: 'Inter', sans-serif !important;
}
.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
  border-color: #8b5cf6 !important;
  box-shadow: 0 0 0 3px rgba(139,92,246,0.14) !important;
}
.stSelectbox>div>div {
  background: #0e0e1c !important;
  border: 1px solid #1c1c2e !important;
  border-radius: 10px !important;
}

/* Main action buttons */
.stButton>button {
  background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 500 !important;
  font-family: 'Inter', sans-serif !important;
  letter-spacing: 0.01em !important;
  box-shadow: 0 2px 14px rgba(124,58,237,0.38) !important;
  transition: all 0.2s ease !important;
}
.stButton>button:hover {
  background: linear-gradient(135deg, #6d28d9 0%, #7c3aed 100%) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 22px rgba(124,58,237,0.48) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: #0e0e1c;
  border-radius: 10px;
  padding: 4px;
  border: 1px solid #17172a;
}
.stTabs [data-baseweb="tab"] {
  color: #2e2e42;
  border-radius: 7px;
  font-family: 'Inter', sans-serif;
  font-size: 0.84rem;
  font-weight: 500;
}
.stTabs [aria-selected="true"] {
  background: #17172a !important;
  color: #e0e0ee !important;
}

/* ── Sidebar (after general button rules to override) ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0c0c1a 0%, #09090f 100%) !important;
  border-right: 1px solid #1a1a2e !important;
}
[data-testid="stSidebar"] > div {
  padding: 1.2rem 0 2rem !important;
}
.sidebar-header {
  padding: 0 1rem 0.75rem;
  margin-bottom: 0.25rem;
}
.sidebar-title {
  font-family: 'Space Mono', monospace;
  font-size: 0.65rem;
  font-weight: 700;
  color: #3a3a58;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}
.sidebar-divider {
  height: 1px;
  background: linear-gradient(90deg, #1c1c30 0%, transparent 85%);
  margin: 0 0 0.5rem;
}
/* Kill Streamlit's default button wrapper spacing */
[data-testid="stSidebar"] .stButton {
  margin: 0 !important;
  padding: 0 !important;
}
[data-testid="stSidebar"] .stButton>button {
  background: transparent !important;
  color: #5a5a82 !important;
  border: none !important;
  border-radius: 0 !important;
  border-left: 2px solid transparent !important;
  font-size: 0.83rem !important;
  font-weight: 400 !important;
  text-align: left !important;
  justify-content: flex-start !important;
  padding: 0.5rem 1rem !important;
  margin: 0 !important;
  width: 100% !important;
  box-shadow: none !important;
  transition: color 0.12s ease, background 0.12s ease, border-color 0.12s ease !important;
  font-family: 'Inter', sans-serif !important;
  letter-spacing: 0 !important;
}
[data-testid="stSidebar"] .stButton>button p {
  text-align: left !important;
  margin: 0 !important;
}
[data-testid="stSidebar"] .stButton>button:hover {
  background: rgba(139,92,246,0.07) !important;
  color: #c0c0e8 !important;
  border-left-color: #8b5cf6 !important;
  transform: none !important;
  box-shadow: none !important;
}
</style>
"""


def inject() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
