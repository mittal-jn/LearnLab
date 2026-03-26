"""
learnlab.components
────────────────────
Pure functions → HTML strings for st.markdown(unsafe_allow_html=True).
Zero Streamlit imports — independently testable.
"""
from __future__ import annotations


def _e(s: str) -> str:
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")


def hero_card(title: str, tagline: str, description: str) -> str:
    return (
        '<div class="card card-accent">'
        '<div class="card-label">🧠 Core Concept</div>'
        f'<div class="concept-title">{_e(title)}</div>'
        f'<div class="concept-tag">{_e(tagline)}</div>'
        f'<div class="concept-desc">{_e(description)}</div>'
        '</div>'
    )


def key_points_card(points: list[dict]) -> str:
    colors = ["p1", "p2", "p3", "p4"]
    items = "".join(
        f'<div class="point {colors[i % 4]}">'
        f'<div class="point-label">{_e(p["label"])}</div>'
        f'<div class="point-value">{_e(p["value"])}</div>'
        '</div>'
        for i, p in enumerate(points[:4])
    )
    return (
        '<div class="card">'
        '<div class="card-label">⚡ Key Points</div>'
        f'<div class="points-grid">{items}</div>'
        '</div>'
    )


def analogy_card(emoji: str, text: str) -> str:
    return (
        '<div class="card card-green">'
        '<div class="card-label">💡 Real-World Analogy</div>'
        '<div class="analogy-box">'
        f'<span class="analogy-emoji">{emoji}</span>'
        f'<span class="analogy-text">{text}</span>'
        '</div></div>'
    )


def diagram_card(diagram: dict) -> str:
    return (
        '<div class="card">'
        '<div class="card-label">📊 Visual Diagram</div>'
        f'<div class="diagram-wrap">{build_svg(diagram)}</div>'
        '</div>'
    )


def chat_bubble(role: str, content: str) -> str:
    if role == "user":
        return (
            '<div class="msg-user">'
            '<div class="msg-role" style="color:#7b61ff">You</div>'
            f'{_e(content)}</div>'
        )
    return (
        '<div class="msg-ai">'
        '<div class="msg-role" style="color:#00e5c0">⚡ LearnLab AI</div>'
        f'{content.replace(chr(10), "<br>")}</div>'
    )


def console_out(text: str, otype: str) -> str:
    color = {"success": "#3ddc84", "error": "#ff6b6b", "info": "#00e5c0"}.get(otype, "#9da3c8")
    return f'<div class="console"><span style="color:{color}">{_e(text)}</span></div>'


def section_label(icon: str, text: str) -> str:
    return f'<div class="section-label">{icon} {_e(text)}</div>'


def build_svg(diagram: dict, W: int = 560, H: int = 160) -> str:
    nodes = diagram.get("nodes", [])
    edges = diagram.get("edges", [])
    dtype = diagram.get("type", "flowchart")
    n = len(nodes)
    if not n:
        return "<p style='color:#6b7094;font-size:0.82rem'>No diagram.</p>"

    pos: dict[str, tuple[float, float]] = {}
    for i, node in enumerate(nodes):
        nid = node.get("id", str(i))
        if dtype == "tree" and n >= 3:
            level = (i).bit_length() - 1 if i > 0 else 0
            p_in_l = i - (2 ** level - 1)
            t_in_l = 2 ** level
            pos[nid] = (((p_in_l + 0.5) / t_in_l) * W, 20 + (level / max(2, n.bit_length())) * (H - 40))
        elif dtype == "layers":
            pos[nid] = (W / 2, 20 + (i / max(n - 1, 1)) * (H - 40))
        else:
            pos[nid] = (50 + (i / max(n - 1, 1)) * (W - 100), H // 2 + (14 if i % 2 else -14))

    parts = [
        f'<svg width="100%" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
        '<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        '<path d="M0,0 L0,6 L8,3 z" fill="#2a2c40"/></marker></defs>',
    ]
    for e in edges:
        f, t = pos.get(e.get("from", "")), pos.get(e.get("to", ""))
        if not (f and t):
            continue
        parts.append(
            f'<line x1="{f[0]:.0f}" y1="{f[1]:.0f}" x2="{t[0]:.0f}" y2="{t[1]:.0f}" '
            f'stroke="#2a2c40" stroke-width="1.5" marker-end="url(#arr)"/>'
        )
        if lbl := e.get("label"):
            parts.append(
                f'<text x="{(f[0]+t[0])/2:.0f}" y="{(f[1]+t[1])/2-5:.0f}" '
                f'fill="#6b7094" font-size="9" text-anchor="middle" '
                f'font-family="Space Mono,monospace">{_e(lbl)}</text>'
            )
    for node in nodes:
        p = pos.get(node.get("id", ""))
        if not p:
            continue
        col = node.get("color", "#7b61ff")
        lbl = node.get("label", "")[:22]
        bw  = max(len(lbl) * 6.8 + 24, 80)
        parts.append(
            f'<g transform="translate({p[0]:.0f},{p[1]:.0f})">'
            f'<rect x="{-bw/2:.0f}" y="-14" width="{bw:.0f}" height="28" rx="8" '
            f'fill="{col}22" stroke="{col}" stroke-width="1.2"/>'
            f'<text y="5" fill="{col}" font-size="10" text-anchor="middle" '
            f'font-family="Space Mono,monospace">{_e(lbl)}</text>'
            '</g>'
        )
    parts.append("</svg>")
    return "".join(parts)
