# CLAUDE.md — DoctorCancúnAgentNanoBot

## Project Overview
AI-powered chatbot for iDoctor Cancún, a phone/tablet/laptop repair shop in Cancún, Mexico.
Built on nanobot + KYNYKOS_AI_Agent + SAC patterns.

## Tech Stack
- **Runtime:** Python 3.11+
- **Framework:** FastAPI + Uvicorn
- **LLM:** Multi-provider router (Ollama → Anthropic → Groq → OpenAI)
- **Database:** SQLite (leads.db)
- **Channels:** WhatsApp (Baileys bridge), Telegram, Web widget
- **Deploy:** Docker + Render
- **CI/CD:** GitHub Actions

## Key Commands
```bash
poetry install                          # Install deps
poetry run uvicorn app.main:app --reload # Dev server
poetry run pytest tests/ -v             # Run tests
docker-compose up -d                    # Docker dev
```

## Architecture Rules
1. All business data lives in `data/business_rules.yaml` — never hardcode prices
2. All response templates in `data/responses.yaml` — never hardcode messages
3. Intent patterns in `data/intents.yaml` — modular, not in code
4. SOUL.md defines bot personality — injected into every LLM prompt
5. State machine handles conversation flow — not ad-hoc if/else
6. LLM is fallback, not primary — keyword matching first, LLM for ambiguity
7. Every lead interaction logged to SQLite — no data loss
8. Owner notifications via Telegram for urgencies and escalations

## File Conventions
- Python: snake_case, type hints, docstrings
- YAML: 2-space indent, comments for sections
- Tests: pytest, mirror app/ structure

## Business Context
- **Business:** iDoctor Cancún — phone repair shop
- **Location:** C. 71 SM 91 Mza 88 Lt 17, Tumben Cuxtal, 77516 Cancún
- **Rating:** 4.9★ Google (31 reviews)
- **Experience:** 10+ years
- **Key differentiator:** Honesty, free diagnosis, written warranty
- **Slogan:** "iDoctor... ¡recupera tu vida!"
