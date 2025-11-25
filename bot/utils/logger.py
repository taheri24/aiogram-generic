"""Logging configuration for the bot."""

import sys
from pathlib import Path
from loguru import logger
from typing import Optional


class BotLogger:
    """Configures and manages bot logging."""
    
    def __init__(self, log_level: str = "INFO", log_file: Optional[str] = None):
        """
        Initialize logger configuration.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional log file path
        """
        self.log_level = log_level
        self.log_file = log_file
        self._configure()
    
    def _configure(self):
        """Configure loguru logger."""
        # Remove default logger
        logger.remove()
        
        # Add console logger with colors
        logger.add(
            sys.stdout,
            format=self._get_console_format(),
            level=self.log_level,
            colorize=True,
            backtrace=True,
            diagnose=True
        )
        
        # Add file logger if specified
        if self.log_file:
            # Create logs directory if it doesn't exist
            log_path = Path(self.log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            logger.add(
                self.log_file,
                format=self._get_file_format(),
                level=self.log_level,
                rotation="1 day",
                retention="7 days",
                compression="zip",
                backtrace=True,
                diagnose=True
            )
    
    @staticmethod
    def _get_console_format() -> str:
        """Get console log format with colors."""
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        )
    
    @staticmethod
    def _get_file_format() -> str:
        """Get file log format."""
        return (
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level: <8} | "
            "{name}:{function}:{line} - "
            "{message}"
        )
    
    @staticmethod
    def log_startup_info(bot_name: str, version: str = "2.0.1"):
        """Log bot startup information."""
        logger.info("=" * 50)
        logger.info(f"🤖 {bot_name} v{version} Starting...")
        logger.info("=" * 50)
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Platform: {sys.platform}")
        logger.info("Bot initialization in progress...")
    
    @staticmethod
    def log_shutdown_info():
        """Log bot shutdown information."""
        logger.info("=" * 50)
        logger.info("🛑 Bot shutting down...")
        logger.info("=" * 50)
    
    @staticmethod
    def log_user_action(user_id: int, username: str, action: str, details: str = ""):
        """Log user action for analytics."""
        logger.info(
            f"User Action | ID: {user_id} | Username: @{username} | "
            f"Action: {action} | Details: {details}"
        )
    
    @staticmethod
    def log_error_with_context(error: Exception, context: dict):
        """Log error with additional context."""
        logger.error(f"Error occurred: {error.__class__.__name__}: {error}")
        logger.error(f"Context: {context}")
        logger.exception("Full traceback:")


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = "logs/bot.log"):
    """
    Setup logging for the entire application.
    
    Args:
        log_level: Logging level
        log_file: Optional log file path
    """
    bot_logger = BotLogger(log_level, log_file)
    return logger


# Export logger instance
__all__ = ['logger', 'setup_logging', 'BotLogger']