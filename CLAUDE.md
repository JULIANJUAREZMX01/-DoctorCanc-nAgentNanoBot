# CLAUDE.md — DoctorCancúnAgentNanoBot

## Project Overview
AI-powered chatbot for iDoctor Cancún, a phone/tablet/laptop repair shop in Cancún, Mexico.
Built on nanobot + KYNYKOS_AI_Agent + SAC patterns. Created by Julián Juárez (jaja.dev / KynicOS).

## Tech Stack
- **Runtime:** Python 3.11+
- **Framework:** FastAPI + Uvicorn
- **LLM:** Multi-provider router (Ollama → Anthropic → Groq → OpenAI)
- **Database:** SQLite (data/leads.db)
- **Channels:** Telegram (polling), Web widget, WhatsApp (TODO)
- **Deploy:** Docker + Render
- **CI/CD:** GitHub Actions

## Key Commands
```bash
poetry install                              # Install deps
poetry run uvicorn app.main:app --reload    # Dev server on :8000
poetry run pytest tests/ -v                 # Run tests
```

## Architecture (what's where)
```
app/main.py              → FastAPI routes: / (landing), /dashboard, /api/chat, /api/leads, /api/status
app/core/agent_loop.py   → Message flow: normalize → intent → route → respond → log
app/core/intent_router.py→ Keyword scoring engine, loads data/intents.yaml
app/core/state_machine.py→ 7 lead states: NEW→CITADO/INTERESADO/URGENTE/ESCALADO/etc
app/core/context.py      → SOUL.md injection + response template loader
app/core/onboarding.py   → 45-question self-config: owner writes /onboard, bot asks everything
app/services/llm_router.py → Multi-provider: Ollama(1)→Anthropic(2)→Groq(3)→OpenAI(4)
app/services/price_engine.py → 25+ regex model patterns + YAML price lookup
app/services/lead_manager.py → SQLite CRM (interactions + leads tables)
app/channels/telegram.py → Full bot: owner mode (/onboard /leads /status) + customer mode
data/business_rules.yaml → Prices, hours, services (auto-updated by onboarding)
data/intents.yaml        → 17 intents, ~100 trigger patterns
data/responses.yaml      → 20 bilingual response templates ES/EN
workspace/SOUL.md        → Bot personality injected into every LLM call
web/templates/landing.html→ Public landing page with embedded chat widget
web/templates/dashboard.html→ Owner lead monitoring dashboard
```

## Design Rules
1. Business data ONLY in data/business_rules.yaml — never hardcode
2. Response templates ONLY in data/responses.yaml — never hardcode
3. Keyword matching FIRST (fast), LLM ONLY as fallback (expensive)
4. Every interaction logged to SQLite — no data loss
5. Owner gets Telegram push on LEAD_URGENTE and GARANTIA_ESCALADO

## Current Status (v0.2)
DONE: FastAPI, agent loop, intent router, state machine, LLM router, price engine,
      lead manager, onboarding (45 questions), Telegram bot, landing page, dashboard, tests
TODO: WhatsApp Baileys bridge, cron follow-ups, S3 backups, appointment scheduling

## Business Context
- iDoctor Cancún — C. 71 SM 91, Tumben Cuxtal, 77516 Cancún — Tel: 998 213 4708
- 4.9★ Google (31 reviews) — 10+ years — Free diagnosis — Written warranty
- Slogan: "iDoctor... ¡recupera tu vida!"
