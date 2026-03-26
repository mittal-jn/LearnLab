"""
learnlab.components
────────────────────
Pure functions that return HTML strings for Streamlit's st.markdown().
No Streamlit imports here — keeps rendering logic testable and portable.
"""

from __future__ import annotations


# ── Diagram ───────────────────────────────────────────────────────────────────


def diagram_svg(diagram: dict, width: int = 580, height: int = 165) -> str:
    """Build an SVG diagram from diagram spec dict."""
    nodes = diagram.get("nodes", [])
    edges = diagram.get("edges", [])
    dtype = diagram.get("type", "flowchart")
    n = len(nodes)

    if not n:
        return "<p style='color:#6b7094;font-size:0.82rem'>No diagram available.</p>"

    positions: dict[str, tuple[float, float]] = {}

    for i, node in enumerate(nodes):
        nid = node.get("id", str(i))
        if dtype == "tree" and n >= 3:
            level = (i).bit_length() - 1 if i > 0 else 0
            pos_in_level = i - (2**level - 1)
            total_in_level = 2**level
            x = ((pos_in_level + 0.5) / total_in_level) * width
            y = 20 + (level / max(2, n.bit_length())) * (height - 40)
        elif dtype == "layers":
            x = width / 2
            y = 20 + (i / max(n - 1, 1)) * (height - 40)
        else:
            x = 50 + (i / max(n - 1, 1)) * (width - 100)
            y = height // 2 + (12 if i % 2 else -12)
        positions[nid] = (x, y)

    parts: list[str] = [
        f'<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" '
        f'xmlns="http://www.w3.org/2000/svg">',
        '<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        '<path d="M0,0 L0,6 L8,3 z" fill="#2a2c40"/></marker></defs>',
    ]

    for edge in edges:
        f = positions.get(edge.get("from", ""))
        t = positions.get(edge.get("to", ""))
        if not (f and t):
            continue
        parts.append(
            f'<line x1="{f[0]:.1f}" y1="{f[1]:.1f}" '
            f'x2="{t[0]:.1f}" y2="{t[1]:.1f}" '
            f'stroke="#2a2c40" stroke-width="1.5" marker-end="url(#arr)"/>'
        )
        if label := edge.get("label"):
            mx, my = (f[0] + t[0]) / 2, (f[1] + t[1]) / 2 - 5
            parts.append(
                f'<text x="{mx:.1f}" y="{my:.1f}" fill="#6b7094" font-size="9" '
                f'text-anchor="middle" font-family="Space Mono,monospace">{_esc(label)}</text>'
            )

    for node in nodes:
        nid = node.get("id", "")
        pos = positions.get(nid)
        if not pos:
            continue
        col = node.get("color", "#7b61ff")
        label = node.get("label", "")[:22]
        bw = max(len(label) * 6.8 + 24, 84)
        parts.append(
            f'<g transform="translate({pos[0]:.1f},{pos[1]:.1f})">'
            f'<rect x="{-bw/2:.1f}" y="-14" width="{bw:.1f}" height="28" rx="8" '
            f'fill="{col}22" stroke="{col}" stroke-width="1.2"/>'
            f'<text y="5" fill="{col}" font-size="10" text-anchor="middle" '
            f'font-family="Space Mono,monospace">{_esc(label)}</text>'
            f"</g>"
        )

    parts.append("</svg>")
    return "".join(parts)


# ── Cards ─────────────────────────────────────────────────────────────────────


def hero_card(title: str, tagline: str, description: str) -> str:
    return f"""
<div class="card card-accent">
  <div class="card-title">🧠 Core Concept</div>
  <div class="concept-title">{_esc(title)}</div>
  <div style="font-size:0.78rem;color:#7b61ff;font-family:Space Mono,monospace;margin-bottom:8px">
    {_esc(tagline)}
  </div>
  <div class="concept-desc">{_esc(description)}</div>
</div>
"""


def key_points_card(points: list[dict]) -> str:
    classes = ["p1", "p2", "p3", "p4"]
    items = "".join(
        f'<div class="point-item {classes[i % 4]}">'
        f'<div class="point-label">{_esc(p["label"])}</div>'
        f'<div class="point-value">{_esc(p["value"])}</div>'
        f"</div>"
        for i, p in enumerate(points[:4])
    )
    return f'<div class="card"><div class="points-grid">{items}</div></div>'


def analogy_card(emoji: str, text: str) -> str:
    return f"""
<div class="card card-green">
  <div class="card-title">💡 Real-World Analogy</div>
  <div class="analogy-box">
    <div class="analogy-emoji">{emoji}</div>
    <div class="analogy-text">{text}</div>
  </div>
</div>
"""


def chat_bubble(role: str, content: str) -> str:
    if role == "user":
        return (
            f'<div class="msg-user">'
            f'<div class="msg-label user">You</div>'
            f"{_esc(content)}"
            f"</div>"
        )
    safe = content.replace("\n", "<br>")
    return (
        f'<div class="msg-ai">'
        f'<div class="msg-label ai">⚡ LearnLab AI</div>'
        f"{safe}"
        f"</div>"
    )


def console_output(text: str, otype: str) -> str:
    color_map = {
        "success": "#3ddc84",
        "error": "#ff6b6b",
        "info": "#00e5c0",
        "normal": "#c9d1d9",
    }
    color = color_map.get(otype, "#9da3c8")
    safe = _esc(text)
    return f'<div class="console-out"><span style="color:{color}">{safe}</span></div>'


def section_label(icon: str, text: str) -> str:
    return f'<div class="section-label">{icon} {_esc(text)}</div>'


# ── Helpers ───────────────────────────────────────────────────────────────────


def _esc(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )

