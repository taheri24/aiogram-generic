"""Configuration management for the Telegram bot."""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Bot settings
    bot_token: str = Field(..., description="Telegram Bot API token")
    bot_name: str = Field(default="Utility Bot", description="Bot display name")
    bot_username: str = Field(default="@utility_bot", description="Bot username")
    
    # Admin settings
    admin_ids: List[int] = Field(default_factory=list, description="List of admin user IDs")
    
    # Features
    enable_animations: bool = Field(default=True, description="Enable message animations")
    default_message_style: str = Field(default="friendly", description="Default message style")
    rate_limit_per_minute: int = Field(default=30, description="Rate limit per minute per user")
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str = Field(default="bot.log", description="Log file path")
    
    class Config:
        """Pydantic settings configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    @property
    def admin_ids_list(self) -> List[int]:
        """Parse admin IDs from comma-separated string if needed."""
        if isinstance(self.admin_ids, str):
            return [int(id.strip()) for id in self.admin_ids.split(",") if id.strip()]
        return self.admin_ids


# Create global settings instance
try:
    settings = Settings()
except Exception as e:
    print(f"Error loading settings: {e}")
    print("Please ensure .env file exists with required configuration")
    raise