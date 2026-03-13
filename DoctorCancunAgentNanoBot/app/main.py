"""DoctorCancúnAgentNanoBot — Main FastAPI Application."""

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config.settings import settings
from app.core.agent_loop import AgentLoop
from app.services.llm_router import LLMRouter
from app.services.lead_manager import LeadManager
from app.services.price_engine import PriceEngine
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# --- Global instances ---
agent_loop: AgentLoop | None = None
llm_router: LLMRouter | None = None
lead_manager: LeadManager | None = None
price_engine: PriceEngine | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic."""
    global agent_loop, llm_router, lead_manager, price_engine

    logger.info("🩺 Starting DoctorCancúnAgentNanoBot...")
    logger.info(f"   Environment: {settings.environment}")
    logger.info(f"   Business: {settings.business_name}")

    # Initialize services
    llm_router = LLMRouter()
    lead_manager = LeadManager()
    price_engine = PriceEngine()
    agent_loop = AgentLoop(
        llm_router=llm_router,
        lead_manager=lead_manager,
        price_engine=price_engine,
    )

    await lead_manager.initialize()
    logger.info("✅ All services initialized")

    # Start channel listeners
    if settings.telegram_enabled and settings.telegram_token:
        from app.channels.telegram import start_telegram_bot
        asyncio.create_task(start_telegram_bot(agent_loop))
        logger.info("📱 Telegram bot started")

    logger.info("🩺 DocBot ready — iDoctor... ¡recupera tu vida!")

    yield

    # Shutdown
    logger.info("🛑 Shutting down DocBot...")
    await lead_manager.close()


app = FastAPI(
    title="DoctorCancúnAgentNanoBot",
    description="AI chatbot for iDoctor Cancún",
    version="0.1.0",
    lifespan=lifespan,
)

# Static files and templates
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")


# --- API Routes ---


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard."""
    stats = await lead_manager.get_stats() if lead_manager else {}
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "stats": stats, "business": settings.business_name},
    )


@app.get("/api/status")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "DoctorCancúnAgentNanoBot",
        "business": settings.business_name,
        "version": "0.1.0",
        "llm_providers": llm_router.available_providers() if llm_router else [],
    }


@app.get("/api/leads")
async def get_leads(status: str | None = None, limit: int = 50):
    """Get leads from CRM."""
    if not lead_manager:
        return JSONResponse({"error": "Lead manager not initialized"}, status_code=503)
    leads = await lead_manager.get_leads(status=status, limit=limit)
    return {"leads": leads, "count": len(leads)}


@app.get("/api/leads/stats")
async def get_lead_stats():
    """Get lead statistics."""
    if not lead_manager:
        return JSONResponse({"error": "Lead manager not initialized"}, status_code=503)
    return await lead_manager.get_stats()


@app.post("/api/chat")
async def web_chat(request: Request):
    """Web widget chat endpoint."""
    body = await request.json()
    message = body.get("message", "")
    session_id = body.get("session_id", "web_anonymous")

    if not agent_loop:
        return JSONResponse({"error": "Agent not initialized"}, status_code=503)

    response = await agent_loop.process_message(
        message=message,
        session_id=session_id,
        channel="web",
    )
    return {"response": response}


@app.get("/api/prices/{device_model}")
async def get_price(device_model: str):
    """Look up price for a device model."""
    if not price_engine:
        return JSONResponse({"error": "Price engine not initialized"}, status_code=503)
    result = price_engine.lookup(device_model)
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.environment == "development",
    )
