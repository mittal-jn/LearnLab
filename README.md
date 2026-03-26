# ⚡ LearnLab

Interactive AI Learning Platform — search any CS concept and get a live visual dashboard, code runner, and AI tutor, powered by **Groq** (free & fast).

## Project Structure

```
learnlab/
├── src/learnlab/
│   ├── __init__.py     # package
│   ├── app.py          # Streamlit UI
│   ├── agent.py        # all Groq AI calls
│   ├── components.py   # HTML/SVG renderers (no Streamlit dep)
│   ├── styles.py       # custom CSS
│   └── cli.py          # uv run learnlab
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── pyproject.toml      # uv project + deps
├── requirements.txt    # for Streamlit Cloud
└── uv.lock
```

## Local Setup

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone & install
git clone https://github.com/YOUR_USERNAME/learnlab.git
cd learnlab
uv sync

# Add your free Groq key (console.groq.com)
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml: GROQ_API_KEY = "gsk_..."

# Run
uv run learnlab
```

## Deploy on Streamlit Cloud (Free)

1. Push repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Set main file: `src/learnlab/app.py`
4. Advanced settings → Secrets:
   ```toml
   GROQ_API_KEY = "gsk_your-key-here"
   ```
5. Deploy → get public URL

## Add a dependency

```bash
uv add <package>
echo "<package>" >> requirements.txt   # keep Streamlit Cloud in sync
git add pyproject.toml uv.lock requirements.txt
git commit -m "chore: add <package>"
```
