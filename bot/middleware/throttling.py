"""Rate limiting middleware to prevent spam."""

from typing import Callable, Dict, Any, Awaitable
from datetime import datetime, timedelta
from collections import defaultdict
from aiogram import BaseMiddleware
from aiogram.types import Update, Message, CallbackQuery
from loguru import logger

from bot.config import settings


class ThrottlingMiddleware(BaseMiddleware):
    """Middleware for rate limiting user requests."""
    
    def __init__(self, rate_limit: int = None):
        """
        Initialize throttling middleware.
        
        Args:
            rate_limit: Requests per minute limit (default from settings)
        """
        self.rate_limit = rate_limit or settings.rate_limit_per_minute
        self.user_timestamps = defaultdict(list)
        self.user_warnings = defaultdict(int)
    
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        """
        Check rate limit before processing update.
        
        Args:
            handler: Next handler in chain
            event: Update event
            data: Additional data
            
        Returns:
            Handler result or None if rate limited
        """
        user = data.get("event_from_user")
        
        if not user:
            return await handler(event, data)
        
        user_id = user.id
        now = datetime.now()
        
        # Clean old timestamps (older than 1 minute)
        self._clean_old_timestamps(user_id, now)
        
        # Check if user is rate limited
        if len(self.user_timestamps[user_id]) >= self.rate_limit:
            # User exceeded rate limit
            await self._handle_rate_limit(event, user_id)
            return None
        
        # Add current timestamp
        self.user_timestamps[user_id].append(now)
        
        # Reset warnings if user is behaving
        if len(self.user_timestamps[user_id]) < self.rate_limit / 2:
            self.user_warnings[user_id] = 0
        
        # Process the update
        return await handler(event, data)
    
    def _clean_old_timestamps(self, user_id: int, now: datetime):
        """
        Remove timestamps older than 1 minute.
        
        Args:
            user_id: User ID
            now: Current time
        """
        one_minute_ago = now - timedelta(minutes=1)
        self.user_timestamps[user_id] = [
            ts for ts in self.user_timestamps[user_id]
            if ts > one_minute_ago
        ]
    
    async def _handle_rate_limit(self, event: Update, user_id: int):
        """
        Handle rate limit exceeded.
        
        Args:
            event: Update event
            user_id: User ID
        """
        self.user_warnings[user_id] += 1
        warnings = self.user_warnings[user_id]
        
        logger.warning(
            f"Rate limit exceeded for user {user_id} "
            f"(warning #{warnings})"
        )
        
        # Prepare warning message based on warning count
        if warnings == 1:
            message = (
                "⚠️ *Slow down!*\n\n"
                "You're sending requests too quickly. "
                "Please wait a moment before trying again."
            )
        elif warnings == 2:
            message = (
                "⛔ *Rate limit exceeded!*\n\n"
                "You've been temporarily restricted. "
                "Please wait 1 minute before continuing."
            )
        else:
            message = (
                "🚫 *You've been temporarily blocked*\n\n"
                f"Due to excessive requests, you've been blocked for {warnings} minutes. "
                "Please respect the rate limits."
            )
            # Implement actual blocking logic here if needed
        
        # Send warning message
        if hasattr(event, 'message') and event.message:
            await event.message.answer(message, parse_mode="Markdown")
        elif hasattr(event, 'callback_query') and event.callback_query:
            await event.callback_query.answer(
                "⚠️ Too many requests! Please slow down.",
                show_alert=True
            )


class CommandThrottlingMiddleware(BaseMiddleware):
    """Special throttling for specific commands."""
    
    def __init__(self):
        """Initialize command throttling."""
        self.command_cooldowns = {
            '/start': 5,  # 5 seconds
            '/help': 3,   # 3 seconds
            '/stats': 10, # 10 seconds
        }
        self.user_last_command = defaultdict(dict)
    
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        """
        Check command cooldowns.
        
        Args:
            handler: Next handler in chain
            event: Update event
            data: Additional data
            
        Returns:
            Handler result or None if on cooldown
        """
        # Only check messages with commands
        if not (hasattr(event, 'message') and event.message and 
                event.message.text and event.message.text.startswith('/')):
            return await handler(event, data)
        
        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)
        
        command = event.message.text.split()[0].lower()
        
        # Check if command has cooldown
        if command not in self.command_cooldowns:
            return await handler(event, data)
        
        user_id = user.id
        now = datetime.now()
        cooldown = self.command_cooldowns[command]
        
        # Check last usage
        if command in self.user_last_command[user_id]:
            last_usage = self.user_last_command[user_id][command]
            time_passed = (now - last_usage).total_seconds()
            
            if time_passed < cooldown:
                remaining = cooldown - time_passed
                await event.message.answer(
                    f"⏳ Please wait {remaining:.0f} seconds before using {command} again."
                )
                logger.info(
                    f"Command {command} on cooldown for user {user_id} "
                    f"({remaining:.0f}s remaining)"
                )
                return None
        
        # Update last usage
        self.user_last_command[user_id][command] = now
        
        # Process the command
        return await handler(event, data)


class AntiSpamMiddleware(BaseMiddleware):
    """Middleware to detect and prevent spam."""
    
    def __init__(self):
        """Initialize anti-spam middleware."""
        self.user_message_history = defaultdict(list)
        self.spam_threshold = 5  # Same message 5 times = spam
    
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        """
        Check for spam patterns.
        
        Args:
            handler: Next handler in chain
            event: Update event
            data: Additional data
            
        Returns:
            Handler result or None if spam detected
        """
        # Only check text messages
        if not (hasattr(event, 'message') and event.message and event.message.text):
            return await handler(event, data)
        
        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)
        
        user_id = user.id
        message_text = event.message.text.lower().strip()
        now = datetime.now()
        
        # Clean old messages (older than 1 minute)
        one_minute_ago = now - timedelta(minutes=1)
        self.user_message_history[user_id] = [
            (msg, ts) for msg, ts in self.user_message_history[user_id]
            if ts > one_minute_ago
        ]
        
        # Check for repeated messages
        recent_messages = [msg for msg, _ in self.user_message_history[user_id]]
        if recent_messages.count(message_text) >= self.spam_threshold - 1:
            logger.warning(f"Spam detected from user {user_id}: '{message_text}'")
            await event.message.answer(
                "🚫 *Spam detected!*\n\n"
                "Please stop sending the same message repeatedly.",
                parse_mode="Markdown"
            )
            return None
        
        # Add message to history
        self.user_message_history[user_id].append((message_text, now))
        
        # Process the message
        return await handler(event, data)