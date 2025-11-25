"""Middleware for logging and monitoring bot activity."""

from typing import Callable, Dict, Any, Awaitable
from datetime import datetime
from aiogram import BaseMiddleware
from aiogram.types import Update, Message, CallbackQuery
from loguru import logger


class LoggingMiddleware(BaseMiddleware):
    """Middleware to log all bot interactions."""
    
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        """
        Process update with logging.
        
        Args:
            handler: Next handler in chain
            event: Update event
            data: Additional data
            
        Returns:
            Handler result
        """
        start_time = datetime.now()
        user = data.get("event_from_user")
        
        # Log incoming update
        if user:
            update_type = self._get_update_type(event)
            logger.info(
                f"📥 Update | Type: {update_type} | "
                f"User: {user.id} (@{user.username or 'no_username'}) | "
                f"Name: {user.first_name}"
            )
            
            # Log specific content
            if isinstance(event, Message) and event.message:
                if event.message.text:
                    logger.debug(f"Message text: {event.message.text[:50]}...")
            elif isinstance(event, CallbackQuery) and event.callback_query:
                logger.debug(f"Callback data: {event.callback_query.data}")
        
        try:
            # Process the update
            result = await handler(event, data)
            
            # Log successful processing
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.info(
                f"✅ Processed in {processing_time:.2f}s | "
                f"Type: {self._get_update_type(event)}"
            )
            
            return result
            
        except Exception as e:
            # Log error
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.error(
                f"❌ Error after {processing_time:.2f}s | "
                f"Type: {self._get_update_type(event)} | "
                f"Error: {e.__class__.__name__}: {e}"
            )
            logger.exception("Full traceback:")
            raise
    
    def _get_update_type(self, event: Update) -> str:
        """
        Get human-readable update type.
        
        Args:
            event: Update event
            
        Returns:
            Update type string
        """
        if hasattr(event, 'message') and event.message:
            if event.message.text and event.message.text.startswith('/'):
                return f"Command: {event.message.text.split()[0]}"
            return "Message"
        elif hasattr(event, 'callback_query') and event.callback_query:
            return "Callback"
        elif hasattr(event, 'inline_query') and event.inline_query:
            return "Inline Query"
        else:
            return "Unknown"


class UserActivityMiddleware(BaseMiddleware):
    """Middleware to track user activity."""
    
    def __init__(self):
        """Initialize user activity tracker."""
        self.user_last_activity = {}
    
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        """
        Track user activity.
        
        Args:
            handler: Next handler in chain
            event: Update event
            data: Additional data
            
        Returns:
            Handler result
        """
        user = data.get("event_from_user")
        
        if user:
            # Update last activity timestamp
            self.user_last_activity[user.id] = datetime.now()
            
            # Add activity info to data
            data['user_last_activity'] = self.user_last_activity.get(user.id)
            
            # Log if user is returning after inactivity
            if user.id in self.user_last_activity:
                time_since_last = (
                    datetime.now() - self.user_last_activity[user.id]
                ).total_seconds()
                
                if time_since_last > 3600:  # More than 1 hour
                    hours = time_since_last / 3600
                    logger.info(
                        f"👋 User {user.id} returned after "
                        f"{hours:.1f} hours of inactivity"
                    )
        
        return await handler(event, data)


class ErrorHandlingMiddleware(BaseMiddleware):
    """Middleware to handle errors gracefully."""
    
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        """
        Handle errors in update processing.
        
        Args:
            handler: Next handler in chain
            event: Update event
            data: Additional data
            
        Returns:
            Handler result
        """
        try:
            return await handler(event, data)
        except Exception as e:
            # Log the error
            user = data.get("event_from_user")
            if user:
                logger.error(
                    f"Error processing update for user {user.id}: {e}"
                )
            
            # Send user-friendly error message
            if hasattr(event, 'message') and event.message:
                await event.message.answer(
                    "❌ Sorry, something went wrong. Please try again later.\n"
                    "If the problem persists, contact support."
                )
            elif hasattr(event, 'callback_query') and event.callback_query:
                await event.callback_query.answer(
                    "❌ Error processing your request. Please try again.",
                    show_alert=True
                )
            
            # Re-raise for debugging in development
            # In production, you might want to suppress this
            raise