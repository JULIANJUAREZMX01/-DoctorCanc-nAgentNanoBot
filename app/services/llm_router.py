"""LLM Router — Multi-provider with priority fallback.

Adapted from KYNYKOS_AI_Agent llm_router.py pattern.
Priority: Ollama (local) → Anthropic → Groq → OpenAI
"""

import httpx

from app.config.settings import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class LLMRouter:
    """Route LLM requests through multiple providers with fallback."""

    def __init__(self):
        self.providers = self._init_providers()
        logger.info(f"LLM Router initialized with providers: {list(self.providers.keys())}")

    def _init_providers(self) -> dict:
        """Initialize available providers based on configuration."""
        providers = {}

        if settings.ollama_url:
            providers["ollama"] = {
                "priority": 1,
                "url": settings.ollama_url,
                "model": settings.ollama_model,
                "type": "ollama",
            }
        if settings.anthropic_api_key:
            providers["anthropic"] = {
                "priority": 2,
                "api_key": settings.anthropic_api_key,
                "model": settings.anthropic_model,
                "type": "anthropic",
            }
        if settings.groq_api_key:
            providers["groq"] = {
                "priority": 3,
                "api_key": settings.groq_api_key,
                "model": settings.groq_model,
                "type": "groq",
            }
        if settings.openai_api_key:
            providers["openai"] = {
                "priority": 4,
                "api_key": settings.openai_api_key,
                "model": settings.openai_model,
                "type": "openai",
            }

        # Sort by priority
        return dict(sorted(providers.items(), key=lambda x: x[1]["priority"]))

    def available_providers(self) -> list[str]:
        """List available provider names."""
        return list(self.providers.keys())

    async def chat(self, system: str, message: str, max_tokens: int = 300) -> str:
        """Send a chat request through the provider chain.

        Tries each provider in priority order until one succeeds.
        """
        for name, provider in self.providers.items():
            try:
                result = await self._call_provider(name, provider, system, message, max_tokens)
                if result:
                    logger.debug(f"LLM response from {name} ({len(result)} chars)")
                    return result
            except Exception as e:
                logger.warning(f"Provider {name} failed: {e}")
                continue

        logger.error("All LLM providers failed")
        raise RuntimeError("No LLM provider available")

    async def _call_provider(
        self, name: str, provider: dict, system: str, message: str, max_tokens: int
    ) -> str | None:
        """Call a specific provider."""
        provider_type = provider["type"]

        if provider_type == "ollama":
            return await self._call_ollama(provider, system, message, max_tokens)
        elif provider_type == "anthropic":
            return await self._call_anthropic(provider, system, message, max_tokens)
        elif provider_type == "groq":
            return await self._call_groq(provider, system, message, max_tokens)
        elif provider_type == "openai":
            return await self._call_openai(provider, system, message, max_tokens)

        return None

    async def _call_ollama(self, provider: dict, system: str, message: str, max_tokens: int) -> str:
        """Call Ollama local API."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{provider['url']}/api/chat",
                json={
                    "model": provider["model"],
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": message},
                    ],
                    "stream": False,
                    "options": {"num_predict": max_tokens},
                },
            )
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "")

    async def _call_anthropic(
        self, provider: dict, system: str, message: str, max_tokens: int
    ) -> str:
        """Call Anthropic API."""
        from anthropic import AsyncAnthropic

        client = AsyncAnthropic(api_key=provider["api_key"])
        response = await client.messages.create(
            model=provider["model"],
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": message}],
        )
        return response.content[0].text if response.content else ""

    async def _call_groq(self, provider: dict, system: str, message: str, max_tokens: int) -> str:
        """Call Groq API (OpenAI-compatible)."""
        from groq import AsyncGroq

        client = AsyncGroq(api_key=provider["api_key"])
        response = await client.chat.completions.create(
            model=provider["model"],
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": message},
            ],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    async def _call_openai(
        self, provider: dict, system: str, message: str, max_tokens: int
    ) -> str:
        """Call OpenAI API."""
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=provider["api_key"])
        response = await client.chat.completions.create(
            model=provider["model"],
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": message},
            ],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""
