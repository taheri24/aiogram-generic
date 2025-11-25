"""Handler for /start command with cool welcome message."""

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.utils.messages import messages
from bot.keyboards.inline import keyboards
from bot.utils.animations import MessageAnimator
from bot.utils.logger import logger
from bot.config import settings


class UserStates(StatesGroup):
    """User state definitions."""
    new_user = State()
    main_menu = State()
    task_creation = State()
    settings = State()


class StartHandler:
    """Handles /start command with cool messages and animations."""
    
    def __init__(self, animator: MessageAnimator):
        """
        Initialize start handler.
        
        Args:
            animator: MessageAnimator instance for effects
        """
        self.router = Router(name="start_handler")
        self.animator = animator
        self._register_handlers()
    
    def _register_handlers(self):
        """Register all handlers for this router."""
        # Register /start command handler
        self.router.message(CommandStart())(self.start_command)
        
        # Register callback handlers for main menu
        self.router.callback_query(F.data.startswith("menu:"))(self.handle_menu_callback)
        self.router.callback_query(F.data == "back:menu")(self.back_to_menu)
        
        # Register sub-menu callbacks
        self.router.callback_query(F.data.startswith("task:"))(self.handle_task_callback)
        self.router.callback_query(F.data.startswith("alert:"))(self.handle_alert_callback)
        self.router.callback_query(F.data.startswith("tool:"))(self.handle_tool_callback)
    
    async def start_command(
        self, 
        message: Message, 
        state: FSMContext
    ) -> None:
        """
        Handle /start command with cool animation.
        
        Args:
            message: Incoming message
            state: FSM context for state management
        """
        try:
            # Log user action
            user = message.from_user
            logger.info(
                f"Start command from user {user.id} "
                f"(@{user.username or 'no_username'})"
            )
            
            # Get user data for personalization
            user_data = {
                'first_name': user.first_name or 'Friend',
                'username': user.username,
                'user_id': user.id,
                'is_premium': getattr(user, 'is_premium', False)
            }
            
            # Check if this is a new user (you can implement actual check later)
            is_new_user = await self._is_new_user(user.id)
            
            if is_new_user and settings.enable_animations:
                # Show welcome animation for new users
                await self.animator.welcome_animation(
                    message,
                    user_data['first_name'],
                    enable_animations=True
                )
            else:
                # Show regular welcome message
                if settings.enable_animations:
                    await self.animator.typing_effect(message.chat.id, 1.5)
                
                welcome_text = messages.get_start_message(user_data)
                await message.answer(
                    text=welcome_text,
                    reply_markup=keyboards.main_menu(),
                    parse_mode="Markdown"
                )
            
            # Set user state to main menu
            await state.set_state(UserStates.main_menu)
            
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            error_text = messages.get_error_message("generic")
            await message.answer(error_text)
    
    async def handle_menu_callback(
        self, 
        callback: CallbackQuery,
        state: FSMContext
    ) -> None:
        """
        Handle main menu inline keyboard callbacks.
        
        Args:
            callback: Callback query from inline keyboard
            state: FSM context
        """
        try:
            action = callback.data.split(":")[1]
            
            # Log user action
            logger.info(
                f"Menu action '{action}' from user {callback.from_user.id}"
            )
            
            # Handle different menu options
            if action == "tasks":
                response_text = messages.get_task_menu_message()
                reply_markup = keyboards.task_menu()
            elif action == "alerts":
                response_text = messages.get_alerts_menu_message()
                reply_markup = keyboards.alerts_menu()
            elif action == "stats":
                # Generate sample stats for demonstration
                user_stats = {
                    'total_tasks': 42,
                    'completed_tasks': 28,
                    'pending_tasks': 14,
                    'streak_days': 7
                }
                response_text = messages.get_stats_message(user_stats)
                reply_markup = keyboards.back_to_menu()
            elif action == "tools":
                response_text = messages.get_tools_menu_message()
                reply_markup = keyboards.tools_menu()
            elif action == "help":
                response_text = messages.get_help_message()
                reply_markup = keyboards.back_to_menu()
            elif action == "about":
                response_text = messages.get_about_message()
                reply_markup = keyboards.social_links()
            else:
                response_text = "🔄 Processing your request..."
                reply_markup = keyboards.back_to_menu()
            
            # Edit message with response
            await callback.message.edit_text(
                text=response_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
            # Answer callback to remove loading state
            await callback.answer()
            
        except Exception as e:
            logger.error(f"Error handling menu callback: {e}")
            await callback.answer(
                "❌ Something went wrong. Please try again.",
                show_alert=True
            )
    
    async def back_to_menu(
        self,
        callback: CallbackQuery,
        state: FSMContext
    ) -> None:
        """
        Handle back to menu button.
        
        Args:
            callback: Callback query
            state: FSM context
        """
        try:
            # Get user data for personalized menu
            user = callback.from_user
            user_data = {
                'first_name': user.first_name or 'Friend',
                'username': user.username,
                'user_id': user.id
            }
            
            # Show main menu again
            welcome_text = messages.get_start_message(user_data)
            await callback.message.edit_text(
                text=welcome_text,
                reply_markup=keyboards.main_menu(),
                parse_mode="Markdown"
            )
            
            # Set state back to main menu
            await state.set_state(UserStates.main_menu)
            
            await callback.answer()
            
        except Exception as e:
            logger.error(f"Error returning to menu: {e}")
            await callback.answer("❌ Error returning to menu", show_alert=True)
    
    async def handle_task_callback(
        self,
        callback: CallbackQuery,
        state: FSMContext
    ) -> None:
        """Handle task-related callbacks."""
        try:
            action = callback.data.split(":")[1]
            
            task_responses = {
                'create': "📝 *Create New Task*\n\nPlease send me the task description:",
                'view': "📃 *Your Tasks*\n\n1. ✅ Complete bot implementation\n2. ⏳ Add database support\n3. ⏳ Deploy to server",
                'complete': "✅ *Mark Task Complete*\n\nSelect a task to mark as complete:",
                'delete': "🗑️ *Delete Task*\n\nSelect a task to delete:",
                'stats': "📊 *Task Statistics*\n\n• Total: 15\n• Completed: 10\n• Pending: 5\n• Completion rate: 66.7%"
            }
            
            response_text = task_responses.get(
                action, 
                "🔄 Feature coming soon!"
            )
            
            await callback.message.edit_text(
                text=response_text,
                reply_markup=keyboards.back_to_menu(),
                parse_mode="Markdown"
            )
            
            await callback.answer()
            
        except Exception as e:
            logger.error(f"Error handling task callback: {e}")
            await callback.answer("❌ Error processing task", show_alert=True)
    
    async def handle_alert_callback(
        self,
        callback: CallbackQuery,
        state: FSMContext
    ) -> None:
        """Handle alert-related callbacks."""
        try:
            action = callback.data.split(":")[1]
            
            alert_responses = {
                'set': "⏰ *Set New Reminder*\n\nWhat would you like to be reminded about?",
                'view': "📅 *Your Alerts*\n\n• Daily standup - 9:00 AM\n• Lunch break - 12:30 PM\n• Team meeting - 3:00 PM",
                'mute': "🔕 *Notifications Muted*\n\nYou won't receive alerts for the next 8 hours.",
                'settings': "⚙️ *Alert Settings*\n\n• Sound: Enabled ✅\n• Vibration: Enabled ✅\n• Preview: Enabled ✅"
            }
            
            response_text = alert_responses.get(
                action,
                "🔄 Feature coming soon!"
            )
            
            await callback.message.edit_text(
                text=response_text,
                reply_markup=keyboards.back_to_menu(),
                parse_mode="Markdown"
            )
            
            await callback.answer()
            
        except Exception as e:
            logger.error(f"Error handling alert callback: {e}")
            await callback.answer("❌ Error processing alert", show_alert=True)
    
    async def handle_tool_callback(
        self,
        callback: CallbackQuery,
        state: FSMContext
    ) -> None:
        """Handle tool-related callbacks."""
        try:
            action = callback.data.split(":")[1]
            
            tool_responses = {
                'calc': "🧮 *Calculator*\n\nEnter your calculation (e.g., 2+2):",
                'text': "🔤 *Text Formatter*\n\nSend me text to format:",
                'random': f"🎲 *Random Number*\n\nYour random number: *{random.randint(1, 100)}*",
                'timer': "⏱️ *Timer*\n\nHow many minutes should I set the timer for?",
                'url': "🌐 *URL Shortener*\n\nSend me a URL to shorten:",
                'notes': "📝 *Notes*\n\nWhat would you like to note down?"
            }
            
            import random
            response_text = tool_responses.get(
                action,
                "🔄 Tool loading..."
            )
            
            await callback.message.edit_text(
                text=response_text,
                reply_markup=keyboards.back_to_menu(),
                parse_mode="Markdown"
            )
            
            await callback.answer()
            
        except Exception as e:
            logger.error(f"Error handling tool callback: {e}")
            await callback.answer("❌ Error loading tool", show_alert=True)
    
    async def _is_new_user(self, user_id: int) -> bool:
        """
        Check if user is new (placeholder implementation).
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            True if new user, False otherwise
        """
        # TODO: Implement actual database check
        # For now, return True for demonstration
        return True


def setup_start_handler(animator: MessageAnimator) -> Router:
    """
    Setup and return the start handler router.
    
    Args:
        animator: MessageAnimator instance
        
    Returns:
        Configured router
    """
    handler = StartHandler(animator)
    return handler.router