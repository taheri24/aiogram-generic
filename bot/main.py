"""Main entry point for the Telegram bot."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from bot.config import settings
from bot.utils.logger import setup_logging, BotLogger
from bot.utils.animations import MessageAnimator
from bot.handlers.start import setup_start_handler
from bot.handlers.commands import setup_command_handlers
from bot.middleware.logging import (
    LoggingMiddleware, 
    UserActivityMiddleware,
    ErrorHandlingMiddleware
)
from bot.middleware.throttling import (
    ThrottlingMiddleware,
    CommandThrottlingMiddleware,
    AntiSpamMiddleware
)


class TelegramBot:
    """Main bot application class."""
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize the bot.
        
        Args:
            token: Bot token (uses settings if not provided)
        """
        self.token = token or settings.bot_token
        
        # Initialize bot with default properties
        self.bot = Bot(
            token=self.token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.MARKDOWN,
                link_preview_is_disabled=True
            )
        )
        
        # Initialize dispatcher
        self.dp = Dispatcher()
        
        # Initialize animator for cool effects
        self.animator = MessageAnimator(self.bot)
        
        # Setup components
        self._setup_logging()
        self._setup_middleware()
        self._setup_handlers()
    
    def _setup_logging(self):
        """Configure logging for the application."""
        setup_logging(
            log_level=settings.log_level,
            log_file=f"logs/{settings.log_file}"
        )
        BotLogger.log_startup_info(
            bot_name=settings.bot_name,
            version="2.0.1"
        )
    
    def _setup_middleware(self):
        """Register all middleware."""
        # Order matters! Middleware are executed in registration order
        
        # Logging middleware (first to log everything)
        self.dp.update.middleware(LoggingMiddleware())
        
        # Error handling
        self.dp.update.middleware(ErrorHandlingMiddleware())
        
        # Anti-spam and rate limiting
        self.dp.update.middleware(AntiSpamMiddleware())
        self.dp.update.middleware(ThrottlingMiddleware())
        self.dp.update.middleware(CommandThrottlingMiddleware())
        
        # User activity tracking
        self.dp.update.middleware(UserActivityMiddleware())
        
        logger.info("✅ Middleware registered successfully")
    
    def _setup_handlers(self):
        """Register all command and callback handlers."""
        # Setup start handler with animations
        start_router = setup_start_handler(self.animator)
        self.dp.include_router(start_router)
        
        # Setup other command handlers
        command_router = setup_command_handlers()
        self.dp.include_router(command_router)
        
        logger.info("✅ Handlers registered successfully")
    
    async def on_startup(self):
        """Actions to perform on bot startup."""
        # Get bot info
        bot_info = await self.bot.get_me()
        logger.info(f"🤖 Bot started: @{bot_info.username}")
        logger.info(f"🆔 Bot ID: {bot_info.id}")
        logger.info(f"📝 Bot name: {bot_info.first_name}")
        
        # Set bot commands
        await self._set_bot_commands()
        
        logger.info("=" * 50)
        logger.info("🚀 Bot is ready to receive updates!")
        logger.info("=" * 50)
    
    async def _set_bot_commands(self):
        """Set bot commands for the menu."""
        from aiogram.types import BotCommand
        
        commands = [
            BotCommand(command="start", description="🏠 Start the bot and show main menu"),
            BotCommand(command="help", description="❓ Show help information"),
            BotCommand(command="about", description="ℹ️ About this bot"),
            BotCommand(command="stats", description="📊 View your statistics"),
            BotCommand(command="settings", description="⚙️ Bot settings"),
            BotCommand(command="cancel", description="❌ Cancel current operation"),
        ]
        
        await self.bot.set_my_commands(commands)
        logger.info(f"✅ Registered {len(commands)} bot commands")
    
    async def on_shutdown(self):
        """Actions to perform on bot shutdown."""
        BotLogger.log_shutdown_info()
        
        # Close bot session
        await self.bot.session.close()
        logger.info("✅ Bot session closed")
    
    async def start(self):
        """Start the bot with polling."""
        try:
            # Startup actions
            await self.on_startup()
            
            # Delete webhook to use polling
            await self.bot.delete_webhook(drop_pending_updates=True)
            logger.info("🔄 Starting polling...")
            
            # Start polling
            await self.dp.start_polling(
                self.bot,
                allowed_updates=[
                    "message",
                    "callback_query",
                    "inline_query"
                ]
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")
            raise
        finally:
            await self.on_shutdown()
    
    def run(self):
        """Run the bot (blocking)."""
        try:
            asyncio.run(self.start())
        except KeyboardInterrupt:
            logger.info("⏹️ Bot stopped by user (Ctrl+C)")
        except Exception as e:
            logger.error(f"❌ Bot crashed: {e}")
            logger.exception("Full traceback:")
            sys.exit(1)


async def main():
    """Main async entry point."""
    # Check if token is available
    if not settings.bot_token:
        logger.error("❌ BOT_TOKEN not found in environment variables!")
        logger.error("Please create a .env file with your bot token.")
        logger.error("Example: BOT_TOKEN=your_bot_token_here")
        sys.exit(1)
    
    # Create and run bot
    bot = TelegramBot()
    await bot.start()


def run_bot():
    """Synchronous entry point for running the bot."""
    try:
        # Print startup banner
        print("=" * 50)
        print("🤖 TELEGRAM UTILITY BOT v2.0.1")
        print("=" * 50)
        print()
        
        # Check Python version
        if sys.version_info < (3, 9):
            print("❌ Python 3.9+ is required!")
            sys.exit(1)
        
        # Run the bot
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_bot()