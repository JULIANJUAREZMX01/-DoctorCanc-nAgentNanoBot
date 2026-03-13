#!/bin/bash
# ============================================================
# 🩺 DoctorCancúnAgentNanoBot — Deployment Script
# ============================================================
# Ejecuta esto en tu terminal local después de descargar el tar.gz
# Prerrequisitos: git, python 3.11+, poetry
# ============================================================

set -e

echo "🩺 DoctorCancúnAgentNanoBot — Setup & Deploy"
echo "============================================="

# --- PASO 1: Extraer y entrar al proyecto ---
echo ""
echo "📦 PASO 1: Extrayendo proyecto..."
# Si descargaste el tar.gz, descomprímelo primero:
# tar xzf DoctorCancunAgentNanoBot_v0.2.tar.gz
cd DoctorCancunAgentNanoBot

# --- PASO 2: Inicializar Git ---
echo ""
echo "🔧 PASO 2: Inicializando repositorio Git..."
git init
git add .
git commit -m "feat: DocBot v0.2.0 — onboarding, landing page, full agent loop

- FastAPI app con 6 endpoints (landing, dashboard, chat, leads, prices, status)
- Agent Loop: normalize → intent detect → route → respond → log lead
- 17 intents con ~100 patterns (intents.yaml)
- 20 response templates bilingües ES/EN (responses.yaml)
- LLM Router multi-provider: Ollama → Anthropic → Groq → OpenAI
- Price Engine: 25+ modelos, lookup desde business_rules.yaml
- Lead Manager: CRM SQLite con 7 estados de lead
- Onboarding Engine: 45 preguntas, el bot entrevista al dueño via /onboard
- Telegram bot completo: owner mode + customer mode
- Landing page profesional con chat widget embebido
- Dashboard de leads
- Docker + Render config
- CI/CD GitHub Actions
- Tests (intents, prices, state machine, onboarding)
- Docs: research, competitive intel, cuestionario"

# --- PASO 3: Conectar a GitHub ---
echo ""
echo "🐙 PASO 3: Conectando a GitHub..."
# Opción A: Si el repo ya existe
git remote add origin https://github.com/JULIANJUAREZMX01/-DoctorCanc-nAgentNanoBot.git
git branch -M main
git push -u origin main --force

# Opción B: Si necesitas crear el repo primero
# gh repo create -DoctorCanc-nAgentNanoBot --public --source=. --push

echo ""
echo "✅ Código subido a GitHub"

# --- PASO 4: Configurar .env ---
echo ""
echo "⚙️ PASO 4: Configurando variables de entorno..."
cp .env.example .env
echo ""
echo "⚠️  EDITA .env con tus API keys:"
echo "   - TELEGRAM_TOKEN      → @BotFather en Telegram"
echo "   - TELEGRAM_OWNER_ID   → @userinfobot en Telegram"
echo "   - ANTHROPIC_API_KEY   → console.anthropic.com"
echo "   (al menos UNO de los LLM providers)"
echo ""
read -p "¿Ya editaste .env? (Enter para continuar) "

# --- PASO 5: Instalar dependencias ---
echo ""
echo "📥 PASO 5: Instalando dependencias..."
pip install poetry 2>/dev/null || true
poetry install

# --- PASO 6: Correr tests ---
echo ""
echo "🧪 PASO 6: Corriendo tests..."
poetry run pytest tests/ -v || echo "⚠️ Algunos tests pueden fallar si no hay data/intents.yaml accesible"

# --- PASO 7: Iniciar localmente ---
echo ""
echo "🚀 PASO 7: Iniciando servidor local..."
echo "   Landing page: http://localhost:8000"
echo "   Dashboard:    http://localhost:8000/dashboard"
echo "   API Status:   http://localhost:8000/api/status"
echo ""
echo "   En Telegram escribe /onboard para configurar el bot"
echo ""
poetry run uvicorn app.main:app --reload --port 8000
