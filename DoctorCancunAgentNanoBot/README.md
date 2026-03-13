# 🩺 DoctorCancúnAgentNanoBot

**Chatbot inteligente, asistente personal y agente de mensajería instantánea para iDoctor Cancún.**

Un agente conversacional propio, local y replicable — construido sobre [nanobot](https://github.com/HKUDS/nanobot), potenciado con módulos de [KYNYKOS_AI_Agent](https://github.com/JULIANJUAREZMX01/KYNYKOS_AI_Agent) y [SAC](https://github.com/sistemascancunjefe-ai/SAC).

[![Python](https://img.shields.io/badge/python-≥3.11-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/status-development-orange)]()

## 🎯 Propósito

Reducir la carga laboral de **iDoctor Cancún** (taller de reparación de dispositivos electrónicos) automatizando:

- ✅ Respuestas a preguntas frecuentes (precios, horarios, ubicación)
- ✅ Cotizaciones automáticas por modelo de dispositivo
- ✅ Clasificación y seguimiento de leads (CRM ligero)
- ✅ Agendamiento de citas
- ✅ Follow-ups automáticos post-reparación
- ✅ Escalación inteligente a humano
- ✅ Soporte bilingüe ES/EN (turistas)

## 🏗️ Arquitectura

```
[WhatsApp / Telegram / Web Widget]
            │
            ▼
   ┌────────────────┐
   │  Gateway Layer  │  ← nanobot channels + bridge
   └───────┬────────┘
           │
           ▼
   ┌────────────────┐
   │  Intent Router  │  ← keyword matching + LLM fallback
   └───────┬────────┘
           │
    ┌──────┼──────┬──────────┐
    ▼      ▼      ▼          ▼
 ┌─────┐┌─────┐┌──────┐┌─────────┐
 │ FAQ ││Lead ││Citas ││Escalate │
 │ Bot ││ CRM ││Sched ││ Human   │
 └─────┘└─────┘└──────┘└─────────┘
    │      │      │          │
    └──────┼──────┘──────────┘
           ▼
   ┌────────────────┐
   │  LLM Router    │  ← Ollama → Anthropic → Groq → OpenAI
   └───────┬────────┘
           ▼
   ┌────────────────┐
   │  Persistence   │  ← SQLite + MEMORY.md
   └────────────────┘
```

## 📁 Estructura del Proyecto

```
DoctorCancunAgentNanoBot/
├── app/
│   ├── main.py                 # FastAPI entry point
│   ├── core/
│   │   ├── agent_loop.py       # Agent conversation loop
│   │   ├── context.py          # Prompt builder + SOUL injection
│   │   ├── intent_router.py    # Intent detection engine
│   │   ├── state_machine.py    # Conversation state management
│   │   └── memory.py           # Persistent memory
│   ├── services/
│   │   ├── llm_router.py       # Multi-provider LLM router ⭐
│   │   ├── token_tracker.py    # Per-provider usage tracking
│   │   ├── lead_manager.py     # Lead classification + CRM
│   │   ├── price_engine.py     # Price lookup by device model
│   │   ├── appointment.py      # Appointment scheduling
│   │   └── notifications.py    # Push notifications (owner)
│   ├── channels/
│   │   ├── whatsapp.py         # WhatsApp bridge (Baileys)
│   │   ├── telegram.py         # Telegram bot
│   │   └── web_widget.py       # Embedded web chat
│   ├── cloud/
│   │   ├── dashboard.py        # Web dashboard for leads
│   │   ├── mcp_server.py       # MCP integration
│   │   └── backup.py           # S3 backups
│   ├── config/
│   │   ├── settings.py         # Global settings + .env loader
│   │   ├── llm_config.yaml     # LLM provider configuration
│   │   └── schema.py           # Pydantic schemas
│   └── utils/
│       ├── logger.py           # Structured logging
│       ├── i18n.py             # Internationalization ES/EN
│       └── text_normalize.py   # WhatsApp text normalization
├── workspace/
│   ├── SOUL.md                 # Bot personality + rules
│   ├── USER.md                 # Default user profile
│   ├── AGENTS.md               # Operating instructions
│   ├── MEMORY.md               # Persistent memory store
│   └── skills/                 # Custom agent skills
├── data/
│   ├── business_rules.yaml     # Prices, hours, services
│   ├── intents.yaml            # Intent patterns
│   ├── responses.yaml          # Response templates
│   └── leads.db                # SQLite lead database
├── web/
│   ├── static/                 # Dashboard assets
│   └── templates/              # Jinja2 templates
├── infrastructure/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── render.yaml
├── scripts/
│   ├── setup.sh                # First-time setup
│   ├── seed_data.py            # Seed business rules
│   └── migrate_db.py           # Database migrations
├── tests/
│   ├── test_intents.py
│   ├── test_price_engine.py
│   └── test_state_machine.py
├── docs/
│   ├── RESEARCH.md
│   ├── COMPETITIVE_INTEL.md
│   └── DEPLOYMENT.md
├── .github/workflows/
│   ├── deploy.yml
│   ├── test.yml
│   └── backup.yml
├── .env.example
├── .gitignore
├── CLAUDE.md
├── LICENSE
├── pyproject.toml
└── README.md
```

## 🚀 Quick Start

### 1. Clonar

```bash
git clone https://github.com/JULIANJUAREZMX01/-DoctorCanc-nAgentNanoBot.git
cd DoctorCancunAgentNanoBot
```

### 2. Configurar

```bash
cp .env.example .env
# Editar .env con tus API keys y tokens
```

### 3. Instalar

```bash
pip install poetry
poetry install
```

### 4. Iniciar

```bash
# Desarrollo local
poetry run uvicorn app.main:app --reload --port 8000

# Con Docker
docker-compose up -d
```

### 5. Conectar canales

```bash
# Telegram
# → Configurar TELEGRAM_TOKEN en .env

# WhatsApp
# → Configurar número y escanear QR
```

## ⚙️ Variables de Entorno

```env
# App
ENVIRONMENT=development
LOG_LEVEL=INFO
APP_PORT=8000

# LLM Providers
ANTHROPIC_API_KEY=sk-ant-...
GROQ_API_KEY=gsk-...
OPENAI_API_KEY=sk-...
OLLAMA_URL=http://localhost:11434

# Channels
TELEGRAM_TOKEN=123456:ABC...
TELEGRAM_OWNER_ID=123456789
WHATSAPP_ENABLED=false
WHATSAPP_NUMBER=+529982134708

# Business
BUSINESS_NAME=iDoctor Cancún
BUSINESS_PHONE=9982134708

# Database
DATABASE_URL=sqlite:///data/leads.db

# Notifications
OWNER_NOTIFICATION_CHANNEL=telegram
```

## 📊 Dashboard

Accede al panel de leads en `http://localhost:8000/dashboard`

## 🤝 Créditos

- **Base:** [nanobot](https://github.com/HKUDS/nanobot) by HKUDS (MIT)
- **LLM Router + Cloud:** [KYNYKOS_AI_Agent](https://github.com/JULIANJUAREZMX01/KYNYKOS_AI_Agent) by Julian Juarez
- **Notifications + Patterns:** [SAC](https://github.com/sistemascancunjefe-ai/SAC) by sistemascancunjefe-ai
- **Architecture:** [KynicOS](https://github.com/JULIANJUAREZMX01) v2.2

## 📄 License

MIT — See [LICENSE](LICENSE)

## 👤 Author

**Julián Alexander Juárez Alvarado** (jaja.dev)
Jefe de Sistemas — CEDIS Cancún 427
UNT Team / Project Catalyst

---

*iDoctor... ¡recupera tu vida!* 📱✨
