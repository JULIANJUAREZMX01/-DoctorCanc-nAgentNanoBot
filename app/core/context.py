"""Context Builder — Loads SOUL.md and response templates, builds LLM prompts."""

from pathlib import Path

import yaml

from app.config.settings import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

SOUL_PATH = Path("workspace/SOUL.md")
RESPONSES_PATH = Path("data/responses.yaml")

_soul_content: str | None = None
_responses: dict | None = None


def _load_soul() -> str:
    """Load SOUL.md personality file."""
    global _soul_content
    if _soul_content is None:
        if SOUL_PATH.exists():
            _soul_content = SOUL_PATH.read_text(encoding="utf-8")
        else:
            _soul_content = (
                "Eres el asistente virtual de iDoctor Cancún. "
                "Responde de forma amigable, profesional y directa. "
                "Siempre intenta llevar la conversación hacia una visita al taller."
            )
            logger.warning("SOUL.md not found, using default personality")
    return _soul_content


def _load_responses() -> dict:
    """Load response templates from YAML."""
    global _responses
    if _responses is None:
        if RESPONSES_PATH.exists():
            with open(RESPONSES_PATH, "r", encoding="utf-8") as f:
                _responses = yaml.safe_load(f) or {}
        else:
            _responses = {}
            logger.warning("responses.yaml not found, using empty templates")
    return _responses


def load_response(key: str, lang: str = "es") -> str:
    """Load a specific response template by key and language."""
    responses = _load_responses()
    templates = responses.get("responses", {})
    template = templates.get(key, {})

    if isinstance(template, str):
        return template
    if isinstance(template, dict):
        return template.get(lang, template.get("es", f"[Missing response: {key}]"))
    return f"[Missing response: {key}]"


class ContextBuilder:
    """Build system prompts for LLM calls."""

    def build_system_prompt(self, state=None, lang: str = "es") -> str:
        """Build full system prompt with SOUL + business context."""
        soul = _load_soul()
        business_context = self._business_context()
        lang_instruction = (
            "Respond in English." if lang == "en"
            else "Responde en español mexicano coloquial."
        )

        prompt = f"""{soul}

## Contexto del negocio
{business_context}

## Instrucciones de esta conversación
- {lang_instruction}
- Sé breve y directo (máximo 3-4 oraciones por respuesta).
- Si no sabes el precio exacto, sugiere traer el equipo para diagnóstico gratuito.
- Siempre intenta cerrar con un call-to-action (visita, cita, llamada).
- No inventes precios ni tiempos que no tengas confirmados.
"""
        if state and state.context_history:
            prompt += "\n## Historial reciente de esta conversación:\n"
            for msg in state.context_history[-5:]:
                role = "Cliente" if msg["role"] == "user" else "DocBot"
                prompt += f"- {role}: {msg['content']}\n"

        return prompt

    def _business_context(self) -> str:
        return f"""- Negocio: {settings.business_name}
- Dirección: {settings.business_address}
- Teléfono: {settings.business_phone}
- Facebook: {settings.business_facebook}
- Experiencia: +10 años
- Diagnóstico: GRATUITO
- Garantía: Por escrito en todas las reparaciones
- Slogan: "{settings.business_slogan}"
- Rating: 4.9★ en Google (31 reseñas)
- Diferenciador: Honestidad, transparencia, explicamos opciones al cliente"""
