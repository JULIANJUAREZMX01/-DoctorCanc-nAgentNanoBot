"""Intent Router — Keyword-based intent detection with YAML-driven patterns.

Design: Fast keyword matching first, LLM only as fallback.
Patterns loaded from data/intents.yaml at startup.
"""

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from app.utils.logger import setup_logger

logger = setup_logger(__name__)

INTENTS_PATH = Path("data/intents.yaml")


@dataclass
class IntentResult:
    """Result of intent detection."""

    intent_name: str = "unknown"
    confidence: float = 0.0
    matched_patterns: list[str] = field(default_factory=list)
    extracted_entities: dict = field(default_factory=dict)


class IntentRouter:
    """Detect user intent from normalized text using keyword patterns."""

    def __init__(self, intents_path: Path = INTENTS_PATH):
        self.intents: dict = {}
        self._load_intents(intents_path)

    def _load_intents(self, path: Path) -> None:
        """Load intent patterns from YAML file."""
        if not path.exists():
            logger.warning(f"Intents file not found: {path}, using defaults")
            self._load_defaults()
            return

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self.intents = data.get("intents", {})
        total_patterns = sum(len(v.get("patterns", [])) for v in self.intents.values())
        logger.info(f"Loaded {len(self.intents)} intents with {total_patterns} patterns")

    def _load_defaults(self) -> None:
        """Fallback default intents if YAML not found."""
        self.intents = {
            "greeting": {"patterns": ["hola", "buenas", "buen dia", "buenos dias", "hey"]},
            "location": {"patterns": ["donde", "ubicacion", "direccion", "como llego"]},
            "hours": {"patterns": ["horario", "hora", "abren", "cierran", "abiertos"]},
        }

    def detect(self, text: str) -> IntentResult:
        """Detect intent from normalized text.

        Uses a scoring system:
        - Each matched pattern adds weight
        - Longer pattern matches score higher
        - Multiple matches in same intent boost confidence

        Returns:
            IntentResult with best matching intent
        """
        text_lower = text.lower().strip()
        best = IntentResult()

        for intent_name, intent_data in self.intents.items():
            patterns = intent_data.get("patterns", [])
            matched = []
            score = 0.0

            for pattern in patterns:
                pattern_lower = pattern.lower()
                if pattern_lower in text_lower:
                    matched.append(pattern)
                    # Longer patterns = more specific = higher weight
                    weight = len(pattern_lower.split()) * 0.25
                    score += 0.5 + weight

            if score > best.confidence:
                best = IntentResult(
                    intent_name=intent_name,
                    confidence=min(score, 1.0),
                    matched_patterns=matched,
                )

        if best.confidence > 0:
            logger.debug(
                f"Intent: {best.intent_name} ({best.confidence:.2f}) "
                f"matched: {best.matched_patterns}"
            )

        return best
