# ⚡ LearnLab

Interactive AI Learning Platform — search any CS/programming concept and get a live visual dashboard, code runner, and AI tutor agent, all powered by Claude.

## Project Structure

```
learnlab/
├── src/
│   └── learnlab/
│       ├── __init__.py      # Package metadata
│       ├── app.py           # Streamlit UI entry point
│       ├── agent.py         # All Claude AI calls (concept, runner, tutor)
│       ├── components.py    # HTML/SVG renderers (no Streamlit dependency)
│       ├── styles.py        # Custom CSS injected into Streamlit
│       └── cli.py           # `uv run learnlab` entry point
├── .streamlit/
│   ├── config.toml          # Dark theme + server settings
│   └── secrets.toml.example # API key template
├── pyproject.toml           # uv project config + dependencies
├── uv.lock                  # Locked dependency graph
└── README.md
```

## Prerequisites

Install [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Local Development

```bash
# 1. Clone
git clone https://github.com/your-username/learnlab.git
cd learnlab

# 2. Install deps (uv creates .venv automatically)
uv sync

# 3. Add your Anthropic API key
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml and set:
# ANTHROPIC_API_KEY = "sk-ant-..."

# 4. Run via CLI script
uv run learnlab

# — OR — run Streamlit directly
uv run streamlit run src/learnlab/app.py
```

App opens at **http://localhost:8501**

## Dependency Management

```bash
uv add <package>        # add a dependency
uv remove <package>     # remove a dependency
uv sync --upgrade       # update all packages
uv tree                 # show dependency tree
```

## Deploy Publicly — Streamlit Community Cloud (Free)

### Step 1 — Push to GitHub

```bash
git add .
git commit -m "Initial LearnLab commit"
git remote add origin https://github.com/YOUR_USERNAME/learnlab.git
git push -u origin main
```

> Tip: commit uv.lock for reproducible deploys.

### Step 2 — Get an Anthropic API Key

1. Visit https://console.anthropic.com
2. Go to API Keys → Create Key
3. Copy the key (starts with sk-ant-)

### Step 3 — Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io and sign in with GitHub
2. Click New app
3. Set:
   - Repository: your-username/learnlab
   - Branch: main
   - Main file path: src/learnlab/app.py
4. Click Advanced settings → Secrets and paste:
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
5. Click Deploy!

Your public URL will be:
  https://your-username-learnlab-app-XXXXX.streamlit.app

Streamlit Cloud reads pyproject.toml and installs deps automatically.
No requirements.txt needed.

## Features

- Dynamic topic search — live dashboard on any CS concept
- 10 quick-topic chips (Binary Search, Recursion, Hash Maps…)
- Auto-generated SVG diagrams scoped to each concept
- Key points grid: complexity, best use, trade-offs
- Real-world analogy card
- Interactive quiz with AI explanation
- Code editor with 6-language support
- AI-simulated code runner with colour-coded console
- AI tutor agent with full conversation memory
- 4 smart suggested questions per topic

## Architecture

  app.py → agent.py      (Claude API — concept, runner, tutor)
         → components.py (HTML/SVG builders, pure functions)
         → styles.py     (CSS injection)

agent.py has zero Streamlit imports — independently testable.
components.py returns plain strings — no framework coupling.
