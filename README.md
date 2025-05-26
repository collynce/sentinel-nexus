# Sentinel Nexus

**Sentinel Nexus** is a global, AI-powered threat intelligence platform that autonomously aggregates, analyzes, and responds to security threats in real-time using multi-source web data and advanced LLM-driven analysis.

---

## Project Structure

```
sentinel/
├── backend/    # FastAPI, Python, agent orchestration, services
│   └── app/
│       └── ...
├── frontend/   # Nuxt 3, Vue, Tailwind, Pinia, Shadcn-vue
│   └── ...
├── .gitignore
├── README.md
└── ...
```

---

## Features
- **Autonomous threat monitoring**: No user prompt required; runs on a schedule with strategic objectives.
- **Data collection pipeline**: Modular agents leverage Bright Data MCP tools for web discovery, access, extraction, and interaction.
- **Threat analysis pipeline**: LLM-driven agents extract IOCs, enrich, assess risk, and recommend actions.
- **Multi-source ingestion**: News, social media, dark web, and more.
- **SOC-ready**: Designed for real-time analyst workflows and automation.

---

## Getting Started

### Backend (FastAPI)
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (Nuxt 3)
```bash
cd frontend
npm install
npm run dev
```

---

## Configuration
- Copy `.env.example` to `.env` in both `backend/` and `frontend/` as needed, and fill in required values (e.g., API keys, MCP credentials).
- Backend expects Bright Data and LLM settings in its `.env` file.

---

## Autonomous Operation
- The platform runs scheduled threat intelligence objectives (configurable in backend service code).
- Results are stored in the database and can be surfaced in the frontend SOC dashboard.

---

## Tech Stack
- **Frontend**: Nuxt 3, Vue, Tailwind CSS, Shadcn-vue, Lucid-vue-icons, Pinia
- **Backend**: Python, FastAPI, Google ADK, LiteLLM, OpenRouter, Bright Data MCP
- **Orchestration**: Modular agents, workflow agents, async pipelines

---

## Contributing
- Please see code comments and follow the modular agent/service structure.
- PRs should keep new files under 300 lines and avoid code duplication.
- Do not commit `.env` or sensitive files.

---

## License
MIT License

---

## Acknowledgements
- Bright Data Real-Time AI Agents Challenge
- Google ADK Team
- Nuxt, Tailwind, Shadcn-vue, OpenRouter, and the open-source community
