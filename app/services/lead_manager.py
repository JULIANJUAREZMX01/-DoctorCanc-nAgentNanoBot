"""Lead Manager — Lightweight CRM with SQLite persistence."""

import aiosqlite
from datetime import datetime
from pathlib import Path

from app.utils.logger import setup_logger

logger = setup_logger(__name__)

DB_PATH = Path("data/leads.db")


class LeadManager:
    """Track and manage customer leads."""

    def __init__(self):
        self.db: aiosqlite.Connection | None = None

    async def initialize(self):
        """Create database and tables."""
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.db = await aiosqlite.connect(str(DB_PATH))
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                channel TEXT DEFAULT 'whatsapp',
                sender_name TEXT,
                message TEXT,
                intent TEXT,
                response TEXT,
                lead_status TEXT DEFAULT 'NEW',
                language TEXT DEFAULT 'es',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                session_id TEXT PRIMARY KEY,
                sender_name TEXT,
                channel TEXT,
                status TEXT DEFAULT 'NEW',
                device_model TEXT,
                device_problem TEXT,
                phone_number TEXT,
                interaction_count INTEGER DEFAULT 0,
                first_contact TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_contact TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                follow_up_at TIMESTAMP,
                notes TEXT
            )
        """)
        await self.db.commit()
        logger.info(f"Lead database initialized at {DB_PATH}")

    async def close(self):
        if self.db:
            await self.db.close()

    async def log_interaction(
        self,
        session_id: str,
        channel: str,
        sender_name: str | None,
        message: str,
        intent: str,
        response: str,
        language: str = "es",
    ):
        """Log a single interaction."""
        if not self.db:
            return

        await self.db.execute(
            """INSERT INTO interactions
               (session_id, channel, sender_name, message, intent, response, language)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (session_id, channel, sender_name, message, intent, response, language),
        )

        # Upsert lead record
        await self.db.execute(
            """INSERT INTO leads (session_id, sender_name, channel, interaction_count, last_contact)
               VALUES (?, ?, ?, 1, CURRENT_TIMESTAMP)
               ON CONFLICT(session_id) DO UPDATE SET
                   sender_name = COALESCE(excluded.sender_name, leads.sender_name),
                   interaction_count = leads.interaction_count + 1,
                   last_contact = CURRENT_TIMESTAMP""",
            (session_id, sender_name, channel),
        )
        await self.db.commit()

    async def update_lead_status(self, session_id: str, status: str):
        """Update lead status."""
        if not self.db:
            return
        await self.db.execute(
            "UPDATE leads SET status = ? WHERE session_id = ?", (status, session_id)
        )
        await self.db.commit()

    async def get_leads(self, status: str | None = None, limit: int = 50) -> list[dict]:
        """Get leads with optional status filter."""
        if not self.db:
            return []

        if status:
            cursor = await self.db.execute(
                "SELECT * FROM leads WHERE status = ? ORDER BY last_contact DESC LIMIT ?",
                (status, limit),
            )
        else:
            cursor = await self.db.execute(
                "SELECT * FROM leads ORDER BY last_contact DESC LIMIT ?", (limit,)
            )

        rows = await cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    async def get_stats(self) -> dict:
        """Get lead statistics for dashboard."""
        if not self.db:
            return {}

        stats = {}
        cursor = await self.db.execute("SELECT COUNT(*) FROM leads")
        stats["total_leads"] = (await cursor.fetchone())[0]

        cursor = await self.db.execute(
            "SELECT status, COUNT(*) FROM leads GROUP BY status"
        )
        stats["by_status"] = dict(await cursor.fetchall())

        cursor = await self.db.execute(
            "SELECT COUNT(*) FROM interactions WHERE created_at > datetime('now', '-1 day')"
        )
        stats["interactions_24h"] = (await cursor.fetchone())[0]

        cursor = await self.db.execute(
            "SELECT channel, COUNT(*) FROM leads GROUP BY channel"
        )
        stats["by_channel"] = dict(await cursor.fetchall())

        return stats
