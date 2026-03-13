"""Agent Loop — Core conversation processing engine.

Inspired by nanobot's agent/loop.py pattern.
Flow: Message → Normalize → Detect Intent → Route → Generate Response → Log Lead
"""

import time
from pathlib import Path

from app.core.intent_router import IntentRouter, IntentResult
from app.core.state_machine import ConversationState, StateManager
from app.core.context import ContextBuilder
from app.services.llm_router import LLMRouter
from app.services.lead_manager import LeadManager
from app.services.price_engine import PriceEngine
from app.utils.logger import setup_logger
from app.utils.text_normalize import normalize_whatsapp_text
from app.utils.i18n import detect_language

logger = setup_logger(__name__)


class AgentLoop:
    """Main agent processing loop."""

    def __init__(
        self,
        llm_router: LLMRouter,
        lead_manager: LeadManager,
        price_engine: PriceEngine,
    ):
        self.llm = llm_router
        self.leads = lead_manager
        self.prices = price_engine
        self.intents = IntentRouter()
        self.states = StateManager()
        self.context = ContextBuilder()

    async def process_message(
        self,
        message: str,
        session_id: str,
        channel: str = "whatsapp",
        sender_name: str | None = None,
    ) -> str:
        """Process an incoming message and return a response.

        Args:
            message: Raw text from user
            session_id: Unique conversation identifier
            channel: Origin channel (whatsapp, telegram, web)
            sender_name: Optional display name of sender

        Returns:
            Response text to send back
        """
        start_time = time.time()

        # Step 1: Normalize text (handle WhatsApp quirks, typos, abbreviations)
        normalized = normalize_whatsapp_text(message)
        lang = detect_language(normalized)

        logger.info(
            f"[{channel}:{session_id}] Message: {message[:80]}... | Lang: {lang}"
        )

        # Step 2: Get or create conversation state
        state = self.states.get_state(session_id)

        # Step 3: If mid-flow (e.g., waiting for model name), handle continuation
        if state.awaiting_input:
            response = await self._handle_continuation(state, normalized, lang)
            elapsed = time.time() - start_time
            logger.info(f"[{channel}:{session_id}] Response ({elapsed:.2f}s): {response[:80]}...")
            return response

        # Step 4: Detect intent via keyword matching
        intent_result = self.intents.detect(normalized)

        # Step 5: Route to handler
        if intent_result.confidence >= 0.7:
            response = await self._handle_intent(intent_result, state, normalized, lang, sender_name)
        else:
            # Fallback to LLM for ambiguous messages
            response = await self._handle_llm_fallback(normalized, state, lang)

        # Step 6: Log interaction for lead tracking
        await self.leads.log_interaction(
            session_id=session_id,
            channel=channel,
            sender_name=sender_name,
            message=message,
            intent=intent_result.intent_name if intent_result else "unknown",
            response=response,
            language=lang,
        )

        elapsed = time.time() - start_time
        logger.info(f"[{channel}:{session_id}] Response ({elapsed:.2f}s): {response[:80]}...")
        return response

    async def _handle_intent(
        self,
        intent: IntentResult,
        state: ConversationState,
        text: str,
        lang: str,
        sender_name: str | None,
    ) -> str:
        """Route a detected intent to the appropriate handler."""

        handlers = {
            "greeting": self._handle_greeting,
            "location": self._handle_location,
            "hours": self._handle_hours,
            "price_screen": self._handle_price_query,
            "price_battery": self._handle_price_query,
            "price_charging": self._handle_price_query,
            "water_damage": self._handle_water_damage,
            "unlock": self._handle_price_query,
            "diagnosis": self._handle_diagnosis,
            "repair_decision": self._handle_repair_decision,
            "warranty": self._handle_warranty,
            "payment": self._handle_payment,
            "tablet": self._handle_price_query,
            "laptop": self._handle_price_query,
            "accessories": self._handle_accessories,
            "appointment": self._handle_appointment,
            "domicilio": self._handle_domicilio,
            "english": self._handle_english_switch,
        }

        handler = handlers.get(intent.intent_name)
        if handler:
            return await handler(state, text, lang, sender_name)

        # Default: LLM fallback
        return await self._handle_llm_fallback(text, state, lang)

    async def _handle_greeting(self, state, text, lang, sender_name) -> str:
        """Welcome message."""
        from app.core.context import load_response
        name_part = f" {sender_name}" if sender_name else ""
        resp = load_response("welcome", lang)
        return f"¡Hola{name_part}! 👋 {resp}"

    async def _handle_location(self, state, text, lang, sender_name) -> str:
        from app.core.context import load_response
        return load_response("location", lang)

    async def _handle_hours(self, state, text, lang, sender_name) -> str:
        from app.core.context import load_response
        return load_response("hours", lang)

    async def _handle_water_damage(self, state, text, lang, sender_name) -> str:
        from app.core.context import load_response
        state.lead_status = "LEAD_URGENTE"
        return load_response("water_damage_advice", lang)

    async def _handle_diagnosis(self, state, text, lang, sender_name) -> str:
        from app.core.context import load_response
        state.lead_status = "LEAD_INTERESADO"
        return load_response("diagnosis_free", lang)

    async def _handle_repair_decision(self, state, text, lang, sender_name) -> str:
        from app.core.context import load_response
        return load_response("repair_vs_new", lang)

    async def _handle_warranty(self, state, text, lang, sender_name) -> str:
        from app.core.context import load_response
        return load_response("warranty_info", lang)

    async def _handle_payment(self, state, text, lang, sender_name) -> str:
        from app.core.context import load_response
        return load_response("payment_methods", lang)

    async def _handle_accessories(self, state, text, lang, sender_name) -> str:
        from app.core.context import load_response
        return load_response("accessories", lang)

    async def _handle_appointment(self, state, text, lang, sender_name) -> str:
        from app.core.context import load_response
        state.lead_status = "LEAD_CITADO"
        return load_response("appointment", lang)

    async def _handle_domicilio(self, state, text, lang, sender_name) -> str:
        from app.core.context import load_response
        return load_response("domicilio", lang)

    async def _handle_english_switch(self, state, text, lang, sender_name) -> str:
        from app.core.context import load_response
        state.language = "en"
        return load_response("english_detected", "en")

    async def _handle_price_query(self, state, text, lang, sender_name) -> str:
        """Handle price lookups. Extract device model from text or ask for it."""
        model = self.prices.extract_model(text)
        if model:
            result = self.prices.lookup(model)
            if result.get("found"):
                state.lead_status = "LEAD_INTERESADO"
                return self._format_price_response(result, lang)
            else:
                return self._format_price_unknown(model, lang)
        else:
            # Need more info — set state to awaiting model
            state.awaiting_input = "device_model"
            return (
                "¡Claro! ¿Me puedes decir el modelo exacto de tu equipo? "
                "Por ejemplo: iPhone 13, Samsung A54, Huawei P30, etc."
            )

    async def _handle_continuation(self, state, text, lang) -> str:
        """Handle continuation when we're awaiting user input."""
        if state.awaiting_input == "device_model":
            state.awaiting_input = None
            model = self.prices.extract_model(text) or text.strip()
            result = self.prices.lookup(model)
            if result.get("found"):
                state.lead_status = "LEAD_INTERESADO"
                return self._format_price_response(result, lang)
            else:
                return self._format_price_unknown(model, lang)
        return "¿En qué más te puedo ayudar?"

    async def _handle_llm_fallback(self, text: str, state: ConversationState, lang: str) -> str:
        """Use LLM for messages that don't match any intent."""
        soul = self.context.build_system_prompt(state, lang)
        try:
            response = await self.llm.chat(
                system=soul,
                message=text,
                max_tokens=300,
            )
            return response
        except Exception as e:
            logger.error(f"LLM fallback failed: {e}")
            return (
                "Disculpa, no entendí bien tu mensaje. "
                "¿Puedes decirme qué equipo tienes y cuál es el problema? "
                "O si prefieres, llámanos al 998 213 4708. 📞"
            )

    def _format_price_response(self, result: dict, lang: str) -> str:
        """Format a price lookup result into a friendly message."""
        model = result.get("model", "tu equipo")
        service = result.get("service", "reparación")
        price_min = result.get("price_min")
        price_max = result.get("price_max")
        time_est = result.get("time_estimate", "")
        warranty = result.get("warranty", "")

        msg = f"Para {model}, el {service} tiene un costo aproximado de "
        if price_min and price_max and price_min != price_max:
            msg += f"${price_min:,} a ${price_max:,} MXN"
        elif price_min:
            msg += f"${price_min:,} MXN"
        else:
            msg += "precio variable (necesitamos ver el equipo)"

        if time_est:
            msg += f"\n⏱️ Tiempo estimado: {time_est}"
        if warranty:
            msg += f"\n🛡️ Garantía: {warranty}"

        msg += "\n\n📍 Recuerda que el diagnóstico es GRATIS. ¿Te gustaría pasar para que te demos precio exacto?"
        return msg

    def _format_price_unknown(self, model: str, lang: str) -> str:
        """Response when we don't have price data for a model."""
        return (
            f"Para {model} necesitamos revisar el equipo directamente para darte un precio exacto. "
            "El diagnóstico es totalmente gratis y sin compromiso. "
            "¿Te gustaría traerlo? 😉"
        )
