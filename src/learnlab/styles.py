"""learnlab.styles — inject all custom CSS into Streamlit."""
from __future__ import annotations
import streamlit as st

# ── Luxury Dark Palette ──────────────────────────────────────
# bg-base:      #080810   deep midnight
# bg-surface:   #0e0e1c   card / surface
# bg-raised:    #13132a   elevated element
# border:       #22223a   visible border
# border-faint: #16162e   subtle border
#
# text-bright:  #f0f0ff   headings / primary
# text-body:    #b0b0d8   body — readable on dark
# text-muted:   #7070a8   secondary / labels — visible
# text-dim:     #484878   tertiary — decorative only
#
# violet:       #8b5cf6   primary accent
# violet-light: #a78bfa   highlight
# violet-glow:  rgba(139,92,246,0.22)
# cyan:         #22d3ee   secondary accent
# emerald:      #10b981   success
# rose:         #f43f5e   danger
# amber:        #f59e0b   warning
# ─────────────────────────────────────────────────────────────

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@700;800&family=Inter:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #080810; color: #b0b0d8; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.8rem 2.2rem 3rem !important; max-width: 100% !important; }

/* ── Logo ── */
.logo-bar {
  padding-bottom: 1.2rem;
  border-bottom: 1px solid #16162e;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.9rem;
}
.logo-mark {
  width: 32px; height: 32px;
  background: linear-gradient(135deg, #7c3aed, #a78bfa);
  border-radius: 9px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
  box-shadow: 0 0 20px rgba(139,92,246,0.5), 0 2px 8px rgba(0,0,0,0.4);
}
.logo-text {
  font-family: 'Syne', sans-serif;
  font-size: 1.45rem;
  font-weight: 800;
  background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 65%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.025em;
}
.tagline {
  font-size: 0.7rem;
  color: #484878;
  font-family: 'Space Mono', monospace;
  letter-spacing: 0.07em;
  margin-left: auto;
}

/* ── Cards ── */
.card {
  background: linear-gradient(160deg, #0e0e1c 0%, #0c0c18 100%);
  border: 1px solid #1e1e34;
  border-radius: 16px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 4px 32px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.04);
}
.card-accent {
  background: linear-gradient(160deg, #100d20 0%, #0d0a1c 100%);
  border-color: #221840;
  box-shadow: 0 4px 32px rgba(124,58,237,0.12), inset 0 1px 0 rgba(167,139,250,0.06);
}
.card-green {
  background: linear-gradient(160deg, #09140e 0%, #070f0a 100%);
  border-color: #122a18;
  box-shadow: 0 4px 32px rgba(16,185,129,0.08), inset 0 1px 0 rgba(52,211,153,0.05);
}
.card-purple {
  background: linear-gradient(160deg, #100c20 0%, #0d0918 100%);
  border-color: #1e1238;
  box-shadow: 0 4px 32px rgba(139,92,246,0.1), inset 0 1px 0 rgba(196,181,253,0.05);
}
.card-label {
  font-family: 'Space Mono', monospace;
  font-size: 0.62rem;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: #484878;
  margin-bottom: 0.7rem;
}

.concept-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.7rem;
  font-weight: 800;
  background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.15;
  margin-bottom: 0.35rem;
  letter-spacing: -0.025em;
}
.concept-tag {
  font-size: 0.72rem;
  color: #8b5cf6;
  font-family: 'Space Mono', monospace;
  margin-bottom: 0.7rem;
  letter-spacing: 0.1em;
}
.concept-desc {
  font-size: 0.88rem;
  color: #8888b8;
  line-height: 1.8;
}

/* ── Key points ── */
.points-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.point {
  background: #0b0b18;
  border-radius: 10px;
  padding: 12px 14px;
  border: 1px solid #1a1a30;
}
.point-label {
  font-size: 0.62rem;
  font-family: 'Space Mono', monospace;
  color: #484878;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 5px;
}
.point-value { font-size: 0.85rem; color: #d0d0f0; font-weight: 500; }
.p1 { border-left: 2px solid #8b5cf6; }
.p2 { border-left: 2px solid #22d3ee; }
.p3 { border-left: 2px solid #f43f5e; }
.p4 { border-left: 2px solid #f59e0b; }

/* ── Diagram ── */
.diagram-wrap {
  background: #050508;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #14142a;
  box-shadow: inset 0 2px 16px rgba(0,0,0,0.7);
}

/* ── Analogy ── */
.analogy-box { display: flex; gap: 14px; align-items: flex-start; }
.analogy-emoji { font-size: 1.6rem; flex-shrink: 0; }
.analogy-text { font-size: 0.87rem; color: #8888b8; line-height: 1.78; }
.analogy-text strong { color: #34d399; font-weight: 600; }

/* ── Section label ── */
.section-label {
  font-family: 'Space Mono', monospace;
  font-size: 0.6rem;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: #484878;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 0.6rem;
}
.section-label::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, #1e1e34, transparent);
}

/* ── Empty state ── */
.empty-state { text-align: center; padding: 80px 20px; }
.empty-icon { font-size: 2.8rem; margin-bottom: 18px; opacity: 0.4; }
.empty-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.1rem;
  font-weight: 800;
  color: #484878;
  margin-bottom: 10px;
  letter-spacing: -0.01em;
}
.empty-sub {
  font-size: 0.8rem;
  color: #383868;
  max-width: 260px;
  margin: 0 auto;
  line-height: 1.7;
}

/* ── Chat ── */
.msg-user {
  background: #0e0e1c;
  border: 1px solid #1e1e34;
  border-radius: 12px 12px 4px 12px;
  padding: 10px 14px;
  margin: 8px 0;
  font-size: 0.87rem;
  color: #b0b0d8;
  margin-left: 20%;
}
.msg-ai {
  background: linear-gradient(135deg, #0e0b20, #0c091c);
  border: 1px solid #201640;
  border-radius: 12px 12px 12px 4px;
  padding: 10px 14px;
  margin: 8px 0;
  font-size: 0.87rem;
  color: #b0b0d8;
  line-height: 1.72;
  margin-right: 8%;
}
.msg-role {
  font-size: 0.6rem;
  font-family: 'Space Mono', monospace;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 5px;
  color: #484878;
}

/* ── Console ── */
.console {
  background: #040408;
  border: 1px solid #14142a;
  border-radius: 10px;
  padding: 14px 16px;
  font-family: 'Space Mono', monospace;
  font-size: 0.76rem;
  line-height: 1.82;
  color: #8888b8;
  min-height: 90px;
  max-height: 240px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-word;
  box-shadow: inset 0 2px 16px rgba(0,0,0,0.8);
}

/* ── Widget overrides ── */
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
  background: #0e0e1c !important;
  border: 1px solid #22223a !important;
  border-radius: 10px !important;
  color: #f0f0ff !important;
  font-family: 'Inter', sans-serif !important;
}
.stTextInput>div>div>input::placeholder { color: #484878 !important; }
.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
  border-color: #8b5cf6 !important;
  box-shadow: 0 0 0 3px rgba(139,92,246,0.15) !important;
}
.stSelectbox>div>div {
  background: #0e0e1c !important;
  border: 1px solid #22223a !important;
  border-radius: 10px !important;
  color: #b0b0d8 !important;
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
  box-shadow: 0 2px 16px rgba(124,58,237,0.4) !important;
  transition: all 0.18s ease !important;
}
.stButton>button:hover {
  background: linear-gradient(135deg, #6d28d9 0%, #7c3aed 100%) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 24px rgba(124,58,237,0.5) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: #0e0e1c;
  border-radius: 10px;
  padding: 4px;
  border: 1px solid #1e1e34;
}
.stTabs [data-baseweb="tab"] {
  color: #7070a8;
  border-radius: 7px;
  font-family: 'Inter', sans-serif;
  font-size: 0.84rem;
  font-weight: 500;
}
.stTabs [aria-selected="true"] {
  background: #1a1a30 !important;
  color: #e0e0f8 !important;
}

/* ── Sidebar (after general button rules) ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0b0b18 0%, #08080f 100%) !important;
  border-right: 1px solid #1a1a30 !important;
}
[data-testid="stSidebar"] > div {
  padding: 1.4rem 0 2rem !important;
}
.sidebar-header {
  padding: 0 1.1rem 0.8rem;
  margin-bottom: 0.2rem;
}
.sidebar-title {
  font-family: 'Space Mono', monospace;
  font-size: 0.62rem;
  font-weight: 700;
  color: #484878;
  letter-spacing: 0.2em;
  text-transform: uppercase;
}
.sidebar-divider {
  height: 1px;
  background: linear-gradient(90deg, #1e1e34 0%, transparent 85%);
  margin: 0 0 0.6rem;
}

/* Kill Streamlit button wrapper spacing in sidebar */
[data-testid="stSidebar"] .stButton {
  margin: 0 !important;
  padding: 0 !important;
}
[data-testid="stSidebar"] .stButton>button {
  background: transparent !important;
  color: #7878b0 !important;
  border: none !important;
  border-radius: 0 !important;
  border-left: 2px solid transparent !important;
  font-size: 0.84rem !important;
  font-weight: 400 !important;
  text-align: left !important;
  justify-content: flex-start !important;
  padding: 0.52rem 1.1rem !important;
  margin: 0 !important;
  width: 100% !important;
  box-shadow: none !important;
  transition: color 0.12s, background 0.12s, border-color 0.12s !important;
  font-family: 'Inter', sans-serif !important;
  letter-spacing: 0 !important;
}
[data-testid="stSidebar"] .stButton>button p {
  text-align: left !important;
  margin: 0 !important;
  color: inherit !important;
}
[data-testid="stSidebar"] .stButton>button:hover {
  background: rgba(139,92,246,0.08) !important;
  color: #d8d8f8 !important;
  border-left-color: #8b5cf6 !important;
  transform: none !important;
  box-shadow: none !important;
}
</style>
"""


def inject() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
