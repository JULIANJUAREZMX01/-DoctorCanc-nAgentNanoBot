"""Telegram Bot Channel — Full implementation with onboarding + customer modes.

Two modes:
- OWNER mode: /onboard triggers self-configuration questionnaire
- CUSTOMER mode: Regular chatbot for clients
"""

import asyncio
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from app.config.settings import settings
from app.core.onboarding import OnboardingEngine
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
_agent_loop = None
_onboarding = OnboardingEngine()


async def start_telegram_bot(agent_loop) -> None:
    global _agent_loop
    _agent_loop = agent_loop
    if not settings.telegram_token:
        logger.warning("TELEGRAM_TOKEN not set")
        return

    app = Application.builder().token(settings.telegram_token).build()
    await app.bot.set_my_commands([
        BotCommand("start", "Iniciar conversación"),
        BotCommand("onboard", "Configurar bot (dueño)"),
        BotCommand("status", "Estado del bot"),
        BotCommand("leads", "Ver leads (dueño)"),
        BotCommand("help", "Ayuda"),
    ])

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("onboard", cmd_onboard))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("leads", cmd_leads))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Telegram bot starting polling...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)


def _is_owner(user_id: int) -> bool:
    return str(user_id) == str(settings.telegram_owner_id)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if _is_owner(user.id):
        await update.message.reply_text(
            f"🩺 *¡Hola, jefe!*\n\nSoy DocBot, tu asistente para iDoctor Cancún.\n\n"
            f"*Comandos de dueño:*\n/onboard — Configurar bot\n/leads — Ver leads\n/status — Estado\n\n"
            f"_Escribe /onboard para comenzar la configuración_",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            f"¡Hola {user.first_name}! 👋\n\nBienvenido a *iDoctor Cancún*.\n"
            f"Reparación de celulares, iPads y laptops. +10 años de experiencia.\n\n"
            f"📍 C. 71 SM 91, Tumben Cuxtal, Cancún\n📱 998 213 4708\n\n¿En qué te ayudo?",
            parse_mode="Markdown",
        )


async def cmd_onboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not _is_owner(user.id):
        await update.message.reply_text("⚠️ Solo para el dueño del negocio.")
        return
    first_msg = _onboarding.start_session(str(user.id))
    await update.message.reply_text(first_msg, parse_mode="Markdown")


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_owner(update.effective_user.id):
        await update.message.reply_text("DocBot activo. ¿En qué te ayudo?")
        return
    providers = _agent_loop.llm.available_providers() if _agent_loop else []
    stats = await _agent_loop.leads.get_stats() if _agent_loop else {}
    await update.message.reply_text(
        f"🩺 *DocBot Status*\n\n✅ Activo\n🤖 LLM: {', '.join(providers) or 'N/A'}\n"
        f"📊 Leads: {stats.get('total_leads', 0)}\n💬 24h: {stats.get('interactions_24h', 0)}",
        parse_mode="Markdown",
    )


async def cmd_leads(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_owner(update.effective_user.id):
        await update.message.reply_text("⚠️ Solo para el dueño.")
        return
    if not _agent_loop:
        return
    leads = await _agent_loop.leads.get_leads(limit=10)
    if not leads:
        await update.message.reply_text("📭 Sin leads aún.")
        return
    msg = "📋 *Últimos 10 leads:*\n\n"
    for l in leads:
        name = l.get("sender_name") or "Anónimo"
        st = l.get("status", "?")
        ch = l.get("channel", "?")
        cnt = l.get("interaction_count", 0)
        e = {"LEAD_CITADO":"🟢","LEAD_INTERESADO":"🟡","LEAD_URGENTE":"🔴","GARANTIA_ESCALADO":"⚠️"}.get(st, "⚪")
        msg += f"{e} *{name}* ({ch}) — {st} [{cnt}]\n"
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🩺 *DocBot — iDoctor Cancún*\n\nEscríbeme sobre:\n• Precios\n• Horarios/ubicación\n"
        "• Diagnóstico gratis\n• Garantías\n• Accesorios\n\nO describe el problema de tu equipo. 📱",
        parse_mode="Markdown",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = update.message.text
    uid = str(user.id)

    # Onboarding mode
    if _is_owner(user.id) and _onboarding.is_onboarding(uid):
        resp = _onboarding.process_answer(uid, text)
        await update.message.reply_text(resp, parse_mode="Markdown")
        return

    # Customer chat
    if not _agent_loop:
        await update.message.reply_text("Estamos configurando. Llama al 998 213 4708. 📞")
        return

    await update.message.chat.send_action("typing")
    response = await _agent_loop.process_message(
        message=text, session_id=f"tg_{user.id}", channel="telegram", sender_name=user.first_name,
    )
    await update.message.reply_text(response)

    # Notify owner on urgencies
    state = _agent_loop.states.get_state(f"tg_{user.id}")
    if state.lead_status in ("LEAD_URGENTE", "GARANTIA_ESCALADO") and settings.telegram_owner_id:
        emoji = "🔴" if state.lead_status == "LEAD_URGENTE" else "⚠️"
        await context.bot.send_message(
            chat_id=int(settings.telegram_owner_id),
            text=f"{emoji} *{state.lead_status}*\n👤 {user.first_name}\n💬 _{text[:200]}_",
            parse_mode="Markdown",
        )
