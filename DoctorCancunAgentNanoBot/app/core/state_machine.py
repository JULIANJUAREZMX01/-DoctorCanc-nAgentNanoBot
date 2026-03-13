"""State Machine — Conversation state management + lead classification."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class LeadStatus(str, Enum):
    NEW = "NEW"
    USUARIO_PREGUNTO = "USUARIO_PREGUNTO"
    LEAD_INTERESADO = "LEAD_INTERESADO"
    LEAD_CITADO = "LEAD_CITADO"
    LEAD_URGENTE = "LEAD_URGENTE"
    GARANTIA_ESCALADO = "GARANTIA_ESCALADO"
    CLIENTE_RECURRENTE = "CLIENTE_RECURRENTE"
    LEAD_PERDIDO = "LEAD_PERDIDO"


@dataclass
class ConversationState:
    """State of a single conversation session."""

    session_id: str
    lead_status: str = LeadStatus.NEW
    language: str = "es"
    awaiting_input: str | None = None  # e.g., "device_model", "name", "appointment_time"
    device_model: str | None = None
    device_problem: str | None = None
    sender_name: str | None = None
    interaction_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    context_history: list[dict] = field(default_factory=list)

    def touch(self):
        """Update last activity timestamp."""
        self.last_activity = datetime.now()
        self.interaction_count += 1

    def add_context(self, role: str, content: str):
        """Add message to context history (keep last 10)."""
        self.context_history.append({"role": role, "content": content[:500]})
        if len(self.context_history) > 10:
            self.context_history = self.context_history[-10:]


class StateManager:
    """Manage conversation states across sessions."""

    def __init__(self):
        self._states: dict[str, ConversationState] = {}

    def get_state(self, session_id: str) -> ConversationState:
        """Get or create conversation state."""
        if session_id not in self._states:
            self._states[session_id] = ConversationState(session_id=session_id)
        state = self._states[session_id]
        state.touch()
        return state

    def remove_state(self, session_id: str) -> None:
        """Remove a conversation state."""
        self._states.pop(session_id, None)

    def get_all_active(self, minutes: int = 60) -> list[ConversationState]:
        """Get all states active within the last N minutes."""
        cutoff = datetime.now()
        return [
            s for s in self._states.values()
            if (cutoff - s.last_activity).total_seconds() < minutes * 60
        ]
