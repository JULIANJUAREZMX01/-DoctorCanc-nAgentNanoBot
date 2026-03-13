#!/bin/bash
echo "🩺 Setting up DoctorCancúnAgentNanoBot..."
cp .env.example .env
pip install poetry
poetry install
mkdir -p data
echo "✅ Setup complete. Edit .env with your API keys, then run: poetry run uvicorn app.main:app --reload"
