# RelocateMind — Global Mobility & Residency Discovery Engine

RelocateMind is a high-tech global mobility discovery engine that matches digital nomads, freelancers, and remote workers with residency visas using a 2-stage hybrid AI approach.

## Tech Stack

* **Backend**: Python 3.10+, FastAPI (ASGI)
* **Database & Auth**: Supabase PostgreSQL & Auth Engine
* **Frontend**: Jinja2 Templates, Tailwind CSS, JetBrains Mono & Inter Fonts
* **AI Engine**: Gemini API (`google-genai` SDK)

## Quickstart

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Agent context

Future coding agents should begin with [`AGENTS.md`](AGENTS.md) and [`PROMPT.md`](PROMPT.md), then read the current project state and relevant documents under [`docs/agent-context/`](docs/agent-context/). The context files distinguish verified implementation from planned architecture and must not contain secrets or private production data.

The root [`PROMPT.txt`](PROMPT.txt) is retained as historical context and is not the canonical handoff.