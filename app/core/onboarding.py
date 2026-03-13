"""Owner Onboarding — The bot interviews the business owner to self-configure.

When the owner sends '/onboard' or is detected as the configured owner,
the bot walks through a structured questionnaire and saves all answers
directly to data/business_rules.yaml and data/responses.yaml.

This makes the bot self-configurable: no manual YAML editing needed.
"""

from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime

import yaml

from app.utils.logger import setup_logger

logger = setup_logger(__name__)

RULES_PATH = Path("data/business_rules.yaml")
ONBOARD_LOG_PATH = Path("data/onboarding_log.yaml")


@dataclass
class OnboardingQuestion:
    """A single question in the onboarding flow."""
    id: str
    section: str
    question: str
    key_path: str  # dot-notation path in business_rules.yaml
    question_type: str = "text"  # text, number, list, yes_no, price_table
    follow_up: str | None = None
    example: str | None = None
    required: bool = True


# ============================================================
# THE 45 QUESTIONS — Structured for bot delivery
# ============================================================

ONBOARDING_QUESTIONS = [
    # --- SECTION 1: BUSINESS BASICS ---
    OnboardingQuestion(
        id="biz_name",
        section="📋 DATOS DEL NEGOCIO",
        question="¿Cuál es el nombre EXACTO como quieres que el bot se presente?\n\n_Ejemplo: \"iDoctor Cancún\", \"Somos iDoctor\"_",
        key_path="business.display_name",
        example="iDoctor Cancún",
    ),
    OnboardingQuestion(
        id="hours_weekday",
        section="📋 DATOS DEL NEGOCIO",
        question="¿Cuál es tu horario de LUNES A VIERNES?\n\n_Ejemplo: 11:00 AM a 8:00 PM_",
        key_path="business.hours.weekdays",
        example="11:00 AM a 8:00 PM",
    ),
    OnboardingQuestion(
        id="hours_saturday",
        section="📋 DATOS DEL NEGOCIO",
        question="¿Horario de SÁBADO?",
        key_path="business.hours.saturday",
        example="11:00 AM a 5:00 PM",
    ),
    OnboardingQuestion(
        id="hours_sunday",
        section="📋 DATOS DEL NEGOCIO",
        question="¿Horario de DOMINGO? _(o 'Cerrado')_",
        key_path="business.hours.sunday",
        example="Cerrado",
    ),
    OnboardingQuestion(
        id="num_technicians",
        section="📋 DATOS DEL NEGOCIO",
        question="¿Cuántos técnicos trabajan en el taller? ¿Cuántos equipos atienden al mismo tiempo?",
        key_path="business.technicians",
    ),
    OnboardingQuestion(
        id="reference",
        section="📋 DATOS DEL NEGOCIO",
        question="¿Alguna referencia para llegar? _(Ejemplo: \"frente a la tienda X\", \"la casa color azul\")_",
        key_path="business.location_reference",
    ),
    OnboardingQuestion(
        id="escalation",
        section="📋 DATOS DEL NEGOCIO",
        question="Cuando el bot NO pueda resolver algo, ¿cómo te aviso?\n\n1️⃣ Te mando mensaje a tu WhatsApp personal\n2️⃣ Te mando Telegram\n3️⃣ Le digo al cliente que llame\n\n_Responde con el número_",
        key_path="business.escalation_method",
    ),

    # --- SECTION 2: SCREEN REPAIR PRICES ---
    OnboardingQuestion(
        id="price_screen_intro",
        section="💰 PRECIOS — PANTALLAS",
        question="Vamos con los precios de CAMBIO DE PANTALLA. Te voy a preguntar modelo por modelo.\n\n¿Cuánto cobras por cambio de pantalla de **iPhone SE/6/7/8**?\n\n_Responde con el precio o rango. Ej: \"800\" o \"800-1200\" o \"No manejo\"_",
        key_path="services.screen_repair.prices.iphone_old",
    ),
    OnboardingQuestion(
        id="price_screen_iphonex",
        section="💰 PRECIOS — PANTALLAS",
        question="¿Cambio de pantalla **iPhone X/XS**?",
        key_path="services.screen_repair.prices.iphone_x",
    ),
    OnboardingQuestion(
        id="price_screen_iphonexr",
        section="💰 PRECIOS — PANTALLAS",
        question="¿Cambio de pantalla **iPhone XR**?",
        key_path="services.screen_repair.prices.iphone_xr",
    ),
    OnboardingQuestion(
        id="price_screen_iphone11",
        section="💰 PRECIOS — PANTALLAS",
        question="¿Cambio de pantalla **iPhone 11**?",
        key_path="services.screen_repair.prices.iphone_11",
    ),
    OnboardingQuestion(
        id="price_screen_iphone12",
        section="💰 PRECIOS — PANTALLAS",
        question="¿Cambio de pantalla **iPhone 12**?",
        key_path="services.screen_repair.prices.iphone_12",
    ),
    OnboardingQuestion(
        id="price_screen_iphone13",
        section="💰 PRECIOS — PANTALLAS",
        question="¿Cambio de pantalla **iPhone 13**?",
        key_path="services.screen_repair.prices.iphone_13",
    ),
    OnboardingQuestion(
        id="price_screen_iphone14",
        section="💰 PRECIOS — PANTALLAS",
        question="¿Cambio de pantalla **iPhone 14**?",
        key_path="services.screen_repair.prices.iphone_14",
    ),
    OnboardingQuestion(
        id="price_screen_iphone15",
        section="💰 PRECIOS — PANTALLAS",
        question="¿Cambio de pantalla **iPhone 15**?",
        key_path="services.screen_repair.prices.iphone_15",
    ),
    OnboardingQuestion(
        id="price_screen_samsung_low",
        section="💰 PRECIOS — PANTALLAS",
        question="¿Cambio de pantalla **Samsung A14/A15** (gama baja)?",
        key_path="services.screen_repair.prices.samsung_a14",
    ),
    OnboardingQuestion(
        id="price_screen_samsung_mid",
        section="💰 PRECIOS — PANTALLAS",
        question="¿Cambio de pantalla **Samsung A54/A55** (gama media)?",
        key_path="services.screen_repair.prices.samsung_a54",
    ),
    OnboardingQuestion(
        id="price_screen_samsung_high",
        section="💰 PRECIOS — PANTALLAS",
        question="¿Cambio de pantalla **Samsung S23/S24** (gama alta)?",
        key_path="services.screen_repair.prices.samsung_s23",
    ),
    OnboardingQuestion(
        id="price_screen_huawei",
        section="💰 PRECIOS — PANTALLAS",
        question="¿Cambio de pantalla **Huawei** (modelo más común que te llega)?",
        key_path="services.screen_repair.prices.huawei_generic",
    ),
    OnboardingQuestion(
        id="price_screen_xiaomi",
        section="💰 PRECIOS — PANTALLAS",
        question="¿Cambio de pantalla **Xiaomi/Redmi**?",
        key_path="services.screen_repair.prices.xiaomi_generic",
    ),
    OnboardingQuestion(
        id="price_screen_motorola",
        section="💰 PRECIOS — PANTALLAS",
        question="¿Cambio de pantalla **Motorola**?",
        key_path="services.screen_repair.prices.motorola_generic",
    ),
    OnboardingQuestion(
        id="screen_warranty",
        section="💰 PRECIOS — PANTALLAS",
        question="¿Cuántos meses de garantía das en cambio de pantalla?",
        key_path="services.screen_repair.warranty",
    ),

    # --- SECTION 3: OTHER SERVICES ---
    OnboardingQuestion(
        id="price_battery",
        section="🔋 OTROS SERVICIOS",
        question="¿Cuánto cobras por **cambio de batería**? _(rango general o por modelo)_",
        key_path="services.battery_replacement.prices.general",
    ),
    OnboardingQuestion(
        id="price_charging",
        section="🔋 OTROS SERVICIOS",
        question="¿Cuánto cobras por **reparación de puerto de carga**?",
        key_path="services.charging_port.prices.general",
    ),
    OnboardingQuestion(
        id="price_water",
        section="🔋 OTROS SERVICIOS",
        question="¿Cuánto cobras por **reparación de daño por agua**? ¿Cobras el diagnóstico en este caso?",
        key_path="services.water_damage.prices.general",
    ),
    OnboardingQuestion(
        id="price_unlock",
        section="🔋 OTROS SERVICIOS",
        question="¿Cuánto cobras por **desbloqueos**? (compañía, FRP/Google, iCloud, patrón)",
        key_path="services.unlock.prices.general",
    ),
    OnboardingQuestion(
        id="other_services",
        section="🔋 OTROS SERVICIOS",
        question="¿Qué OTROS servicios ofreces? _(cámara, micrófono, bocina, back glass, Face ID, consolas, etc.)_ Enlista con precios aproximados:",
        key_path="services.other",
    ),
    OnboardingQuestion(
        id="not_offered",
        section="🔋 OTROS SERVICIOS",
        question="¿Hay algún servicio que NO hagas y que te pregunten seguido?",
        key_path="services.not_offered",
    ),

    # --- SECTION 4: TABLETS & LAPTOPS ---
    OnboardingQuestion(
        id="price_ipad",
        section="📱 TABLETS Y LAPTOPS",
        question="¿Qué servicios ofreces para **iPad/tablets** y a qué precio?",
        key_path="services.tablet.details",
    ),
    OnboardingQuestion(
        id="price_laptop",
        section="📱 TABLETS Y LAPTOPS",
        question="¿Qué servicios ofreces para **laptops/computadoras** y a qué precio?\n_(mantenimiento, formateo, cambio de disco, RAM, pantalla, etc.)_",
        key_path="services.laptop.details",
    ),

    # --- SECTION 5: POLICIES ---
    OnboardingQuestion(
        id="warranty_detail",
        section="🛡️ GARANTÍAS Y POLÍTICAS",
        question="Describe tu política de garantía: ¿Qué cubre? ¿Qué NO cubre?",
        key_path="business.warranty_policy",
    ),
    OnboardingQuestion(
        id="parts_type",
        section="🛡️ GARANTÍAS Y POLÍTICAS",
        question="¿Qué tipo de piezas usas? ¿Originales, genéricas de calidad, ambas? ¿Cómo le explicas la diferencia al cliente?",
        key_path="business.parts_policy",
    ),
    OnboardingQuestion(
        id="payment_methods",
        section="🛡️ GARANTÍAS Y POLÍTICAS",
        question="¿Qué formas de pago aceptas?\n_(efectivo, tarjeta débito, crédito, transferencia, OXXO, Mercado Pago, meses sin intereses, etc.)_",
        key_path="business.payment_methods_detail",
    ),

    # --- SECTION 6: FAQ REAL ---
    OnboardingQuestion(
        id="top_questions",
        section="❓ PREGUNTAS FRECUENTES",
        question="¿Cuáles son las 5 preguntas que MÁS te hacen por WhatsApp? Escríbelas tal cual te las mandan:",
        key_path="faq.top_questions",
    ),
    OnboardingQuestion(
        id="annoying_question",
        section="❓ PREGUNTAS FRECUENTES",
        question="¿Cuál es la pregunta más repetitiva que un bot te quitaría de encima?",
        key_path="faq.most_repetitive",
    ),
    OnboardingQuestion(
        id="english_clients",
        section="❓ PREGUNTAS FRECUENTES",
        question="¿Recibes mensajes en INGLÉS de turistas? ¿Con qué frecuencia?",
        key_path="faq.english_frequency",
    ),
    OnboardingQuestion(
        id="daily_messages",
        section="❓ PREGUNTAS FRECUENTES",
        question="¿Cuántos mensajes/conversaciones recibes por DÍA aproximadamente?",
        key_path="business.daily_messages",
    ),
    OnboardingQuestion(
        id="peak_hours",
        section="❓ PREGUNTAS FRECUENTES",
        question="¿En qué horarios recibes MÁS mensajes? ¿Recibes fuera de horario?",
        key_path="business.peak_hours",
    ),

    # --- SECTION 7: SALES & CONVERSION ---
    OnboardingQuestion(
        id="domicilio",
        section="💼 VENTAS",
        question="¿Ofreces servicio a DOMICILIO? ¿Zonas? ¿Costo extra?",
        key_path="business.domicilio",
    ),
    OnboardingQuestion(
        id="promotions",
        section="💼 VENTAS",
        question="¿Tienes PROMOCIONES actuales o recurrentes?\n_(Ejemplo: \"2x1 en micas\", \"descuento estudiantes\")_",
        key_path="business.promotions",
    ),
    OnboardingQuestion(
        id="accessories",
        section="💼 VENTAS",
        question="¿Vendes accesorios? (micas, fundas, cargadores, audífonos) ¿Rango de precios?",
        key_path="business.accessories",
    ),
    OnboardingQuestion(
        id="sell_used",
        section="💼 VENTAS",
        question="¿Vendes equipos seminuevos/reacondicionados?",
        key_path="business.sells_used_devices",
    ),

    # --- SECTION 8: TONE & IDENTITY ---
    OnboardingQuestion(
        id="tone",
        section="🎭 TONO Y PERSONALIDAD",
        question="¿Cómo habla tu negocio por WhatsApp?\n\n1️⃣ Formal: \"Estimado cliente, con gusto le atendemos\"\n2️⃣ Profesional cercano: \"¡Hola! Claro que lo reparamos\"\n3️⃣ Informal: \"¡Qué onda! Sí, jálate y lo checamos\"\n\n_Responde con el número o describe tu estilo_",
        key_path="business.tone",
    ),
    OnboardingQuestion(
        id="phrases",
        section="🎭 TONO Y PERSONALIDAD",
        question="¿Hay alguna frase o expresión que uses mucho al atender?\n_(Ejemplo: tu forma de saludar, despedirte, agradecer)_",
        key_path="business.signature_phrases",
    ),
    OnboardingQuestion(
        id="never_say",
        section="🎭 TONO Y PERSONALIDAD",
        question="¿Qué NUNCA debe decir el bot?\n_(Ejemplo: \"no hablar mal de competencia\", \"no prometer tiempo exacto sin ver equipo\")_",
        key_path="business.never_say",
    ),
    OnboardingQuestion(
        id="differentiator",
        section="🎭 TONO Y PERSONALIDAD",
        question="¿Qué te DIFERENCIA de la competencia? ¿Por qué un cliente debería elegirte?",
        key_path="business.differentiator",
    ),
    OnboardingQuestion(
        id="fun_fact",
        section="🎭 TONO Y PERSONALIDAD",
        question="¿Algún dato impresionante del negocio?\n_(Ejemplo: \"más de 5,000 equipos reparados\", alguna historia memorable)_",
        key_path="business.fun_fact",
    ),
    OnboardingQuestion(
        id="final",
        section="✅ FINALIZACIÓN",
        question="¡Última pregunta! ¿Algo MÁS que quieras que el bot sepa y que no hayamos preguntado?",
        key_path="business.additional_notes",
        required=False,
    ),
]


class OnboardingEngine:
    """Manages the owner onboarding conversation flow."""

    def __init__(self):
        self.questions = ONBOARDING_QUESTIONS
        self.sessions: dict[str, OnboardingSession] = {}

    def start_session(self, owner_id: str) -> str:
        """Start a new onboarding session. Returns first question."""
        session = OnboardingSession(owner_id=owner_id)
        self.sessions[owner_id] = session

        total = len(self.questions)
        intro = (
            "🩺 *¡Bienvenido al setup de DocBot!*\n\n"
            f"Te haré {total} preguntas para configurar tu chatbot inteligente. "
            "Responde cada una y yo guardo todo automáticamente.\n\n"
            "Puedes escribir `/skip` para saltar una pregunta "
            "y `/done` para terminar en cualquier momento.\n\n"
            "¡Empecemos! 🚀\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
        )
        first_q = self._format_question(session)
        return intro + first_q

    def process_answer(self, owner_id: str, answer: str) -> str:
        """Process an answer and return the next question or completion message."""
        session = self.sessions.get(owner_id)
        if not session:
            return "No hay sesión de onboarding activa. Escribe /onboard para comenzar."

        # Handle commands
        if answer.strip().lower() == "/skip":
            session.skip_current()
        elif answer.strip().lower() == "/done":
            return self._finish_session(session)
        else:
            # Save the answer
            current_q = self.questions[session.current_index]
            session.answers[current_q.id] = answer
            session.current_index += 1

        # Check if done
        if session.current_index >= len(self.questions):
            return self._finish_session(session)

        # Format next question
        return self._format_question(session)

    def is_onboarding(self, user_id: str) -> bool:
        """Check if user is in an active onboarding session."""
        return user_id in self.sessions

    def _format_question(self, session: "OnboardingSession") -> str:
        """Format the current question for display."""
        q = self.questions[session.current_index]
        progress = session.current_index + 1
        total = len(self.questions)
        pct = int((progress / total) * 100)

        # Progress bar
        filled = int(pct / 5)
        bar = "█" * filled + "░" * (20 - filled)

        # Section header (show on first question of each section)
        section_header = ""
        if session.current_index == 0 or q.section != self.questions[session.current_index - 1].section:
            section_header = f"\n*{q.section}*\n━━━━━━━━━━━━━━━━━━━━━\n"

        return (
            f"{section_header}"
            f"📊 [{bar}] {progress}/{total} ({pct}%)\n\n"
            f"{q.question}"
        )

    def _finish_session(self, session: "OnboardingSession") -> str:
        """Save all answers and generate completion message."""
        answered = len(session.answers)
        skipped = session.skipped

        # Save to YAML
        self._save_answers(session)

        # Remove session
        self.sessions.pop(session.owner_id, None)

        return (
            f"🎉 *¡Onboarding completado!*\n\n"
            f"✅ {answered} preguntas respondidas\n"
            f"⏭️ {skipped} preguntas saltadas\n\n"
            f"Tu chatbot ya tiene toda la información para atender clientes. "
            f"Los datos se guardaron en `business_rules.yaml`.\n\n"
            f"El bot ya está listo para recibir mensajes de clientes. 🚀\n\n"
            f"_Si necesitas actualizar algo después, escribe /onboard de nuevo._"
        )

    def _save_answers(self, session: "OnboardingSession") -> None:
        """Save onboarding answers to business_rules.yaml."""
        # Load existing rules
        if RULES_PATH.exists():
            with open(RULES_PATH, "r", encoding="utf-8") as f:
                rules = yaml.safe_load(f) or {}
        else:
            rules = {}

        # Create onboarding section
        if "onboarding" not in rules:
            rules["onboarding"] = {}

        rules["onboarding"]["completed_at"] = datetime.now().isoformat()
        rules["onboarding"]["answers"] = {}

        for q in self.questions:
            if q.id in session.answers:
                answer = session.answers[q.id]
                rules["onboarding"]["answers"][q.id] = answer

                # Also try to update the key_path in the rules
                self._set_nested(rules, q.key_path, answer)

        # Save
        RULES_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(RULES_PATH, "w", encoding="utf-8") as f:
            yaml.dump(rules, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        # Also save raw log
        with open(ONBOARD_LOG_PATH, "w", encoding="utf-8") as f:
            yaml.dump(
                {"owner_id": session.owner_id, "timestamp": datetime.now().isoformat(), "answers": session.answers},
                f, default_flow_style=False, allow_unicode=True,
            )

        logger.info(f"Onboarding saved: {len(session.answers)} answers to {RULES_PATH}")

    def _set_nested(self, d: dict, path: str, value) -> None:
        """Set a nested dict value using dot notation. E.g., 'business.hours.weekdays'."""
        keys = path.split(".")
        for key in keys[:-1]:
            if key not in d or not isinstance(d[key], dict):
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value


@dataclass
class OnboardingSession:
    """State for an onboarding conversation."""
    owner_id: str
    current_index: int = 0
    answers: dict = field(default_factory=dict)
    skipped: int = 0
    started_at: datetime = field(default_factory=datetime.now)

    def skip_current(self):
        self.skipped += 1
        self.current_index += 1
