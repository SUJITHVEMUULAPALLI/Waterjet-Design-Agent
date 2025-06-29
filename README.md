# 💧 Waterjet Design Agent (Marble & Granite Focus)

A modular AI-based system for generating and managing waterjet-cut designs with full automation — from prompt or image input to DXF generation, validation, and quotation.

---

## 🚀 Key Functionalities

| Module | Function |
|--------|----------|
| `app.py` | One-prompt design generator (prompt → DXF → quote) |
| `prompt_browser.py` | Edit, tag, and store prompt templates |
| `batch_generator.py` | Select multiple prompts to generate designs in one run |
| `design_browser.py` | Browse, filter, and download design outputs |
| `png_upload_ui.py` | Upload PNG → Convert to DXF → Validate → Quotation |
| `agent_ui.py` | Unified AI job runner with agent orchestration |
| `waterjet_agents/` | Core logic modules (PromptAgent, DXFAgent, etc.) |

---

## 📁 Directory Structure

```
waterjet_design_agent/
├── *.py                    # Streamlit apps
├── waterjet_agents/       # All AI agents and pipeline controller
├── data/outputs/          # Organized by project/job_id
├── logs/                  # Auto-logged design session results
├── .env                   # API key configuration
├── .gitignore
├── README.md
```

---

## 🧰 Requirements

- Python 3.8+
- [Inkscape](https://inkscape.org/) installed and in your PATH
- OpenAI API key (`.env` file)

---

## ✅ Setup

```bash
cd waterjet_design_agent
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create your `.env` file:
```
OPENAI_API_KEY=your-api-key-here
```

---

## ▶️ One-Click Launchers

These `.bat` files let you run apps easily (Windows):

- [launch_app.bat](launch_app.bat) → main DXF generator
- [launch_prompt_browser.bat](launch_prompt_browser.bat)
- [launch_batch_generator.bat](launch_batch_generator.bat)
- [launch_design_browser.bat](launch_design_browser.bat)
- [launch_png_upload.bat](launch_png_upload.bat)
- [launch_agent_ui.bat](launch_agent_ui.bat)

---

## 🔄 Auto Versioning with GitHub

- Project includes GitHub Actions to auto-commit any new outputs or prompt edits.
- Just push your repo and GitHub tracks everything!

---

## 🧠 Smart Agent-Based Architecture

| Agent | Description |
|-------|-------------|
| PromptAgent | Validates text input |
| ImageAgent | Calls DALL·E |
| DXFAgent | Converts image to DXF |
| ValidationAgent | Checks geometry |
| QuoteAgent | Creates PDF |
| LogAgent | Writes logs to `/logs/` |

---

## 📞 Contact

Created for professionals in stone & tile CNC fabrication  
Built with automation, accuracy, and efficiency in mind 🛠

MIT License © 2025
