"""Global settings loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    environment: str = "development"
    log_level: str = "INFO"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # LLM Providers
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-20250514"
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    llm_rotation_strategy: str = "priority"

    # Telegram
    telegram_token: str = ""
    telegram_owner_id: str = ""
    telegram_enabled: bool = True

    # WhatsApp
    whatsapp_enabled: bool = False
    whatsapp_number: str = ""
    whatsapp_bridge_port: int = 3001

    # Business
    business_name: str = "iDoctor Cancún"
    business_phone: str = "9982134708"
    business_address: str = "C. 71 SM 91 Mza 88 Lt 17, Tumben Cuxtal, 77516 Cancún, Q.R."
    business_gmaps_url: str = ""
    business_facebook: str = "https://www.facebook.com/idoctorcancunn91/"
    business_slogan: str = "iDoctor... ¡recupera tu vida!"

    # Database
    database_url: str = "sqlite:///data/leads.db"

    # Notifications
    owner_notification_channel: str = "telegram"

    # S3 Backups
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    s3_bucket: str = ""
    s3_backup_interval_hours: int = 6

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
