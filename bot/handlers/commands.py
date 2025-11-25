"""Handlers for basic bot commands."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.utils.messages import messages
from bot.keyboards.inline import keyboards
from bot.utils.logger import logger


class CommandHandlers:
    """Handles basic bot commands like /help and /about."""
    
    def __init__(self):
        """Initialize command handlers."""
        self.router = Router(name="command_handlers")
        self._register_handlers()
    
    def _register_handlers(self):
        """Register all command handlers."""
        self.router.message(Command("help"))(self.help_command)
        self.router.message(Command("about"))(self.about_command)
        self.router.message(Command("stats"))(self.stats_command)
        self.router.message(Command("settings"))(self.settings_command)
        self.router.message(Command("cancel"))(self.cancel_command)
    
    async def help_command(self, message: Message) -> None:
        """
        Handle /help command.
        
        Args:
            message: Incoming message
        """
        try:
            logger.info(
                f"Help command from user {message.from_user.id} "
                f"(@{message.from_user.username or 'no_username'})"
            )
            
            help_text = messages.get_help_message()
            await message.answer(
                text=help_text,
                reply_markup=keyboards.back_to_menu(),
                parse_mode="Markdown"
            )
            
        except Exception as e:
            logger.error(f"Error in help command: {e}")
            error_text = messages.get_error_message("generic")
            await message.answer(error_text)
    
    async def about_command(self, message: Message) -> None:
        """
        Handle /about command.
        
        Args:
            message: Incoming message
        """
        try:
            logger.info(
                f"About command from user {message.from_user.id} "
                f"(@{message.from_user.username or 'no_username'})"
            )
            
            about_text = messages.get_about_message()
            await message.answer(
                text=about_text,
                reply_markup=keyboards.social_links(),
                parse_mode="Markdown"
            )
            
        except Exception as e:
            logger.error(f"Error in about command: {e}")
            error_text = messages.get_error_message("generic")
            await message.answer(error_text)
    
    async def stats_command(self, message: Message) -> None:
        """
        Handle /stats command.
        
        Args:
            message: Incoming message
        """
        try:
            logger.info(
                f"Stats command from user {message.from_user.id} "
                f"(@{message.from_user.username or 'no_username'})"
            )
            
            # Generate sample stats for demonstration
            user_stats = {
                'total_tasks': 42,
                'completed_tasks': 28,
                'pending_tasks': 14,
                'streak_days': 7
            }
            
            stats_text = messages.get_stats_message(user_stats)
            await message.answer(
                text=stats_text,
                reply_markup=keyboards.back_to_menu(),
                parse_mode="Markdown"
            )
            
        except Exception as e:
            logger.error(f"Error in stats command: {e}")
            error_text = messages.get_error_message("generic")
            await message.answer(error_text)
    
    async def settings_command(self, message: Message) -> None:
        """
        Handle /settings command.
        
        Args:
            message: Incoming message
        """
        try:
            logger.info(
                f"Settings command from user {message.from_user.id} "
                f"(@{message.from_user.username or 'no_username'})"
            )
            
            settings_text = """
⚙️ *Settings*

Configure your bot preferences:

• 🌍 Language: English
• 🎨 Theme: Default
• 🔔 Notifications: Enabled
• ⏰ Timezone: UTC

_Select an option to modify:_
"""
            
            await message.answer(
                text=settings_text,
                reply_markup=keyboards.settings_menu(),
                parse_mode="Markdown"
            )
            
        except Exception as e:
            logger.error(f"Error in settings command: {e}")
            error_text = messages.get_error_message("generic")
            await message.answer(error_text)
    
    async def cancel_command(
        self, 
        message: Message,
        state: FSMContext
    ) -> None:
        """
        Handle /cancel command to cancel current operation.
        
        Args:
            message: Incoming message
            state: FSM context
        """
        try:
            logger.info(
                f"Cancel command from user {message.from_user.id} "
                f"(@{message.from_user.username or 'no_username'})"
            )
            
            # Clear any active state
            await state.clear()
            
            await message.answer(
                text="❌ Operation cancelled.\n\nUse /start to return to main menu.",
                reply_markup=keyboards.back_to_menu(),
                parse_mode="Markdown"
            )
            
        except Exception as e:
            logger.error(f"Error in cancel command: {e}")
            error_text = messages.get_error_message("generic")
            await message.answer(error_text)


def setup_command_handlers() -> Router:
    """
    Setup and return the command handlers router.
    
    Returns:
        Configured router
    """
    handler = CommandHandlers()
    return handler.router