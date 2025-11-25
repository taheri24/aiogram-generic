"""Message templates and text generation utilities."""

import random
from datetime import datetime
from typing import Dict, Any, Optional


class MessageTemplates:
    """Manages all bot message templates with cool designs."""
    
    @staticmethod
    def get_time_based_greeting() -> str:
        """Get greeting based on current time."""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "🌅 Good morning"
        elif 12 <= hour < 17:
            return "☀️ Good afternoon"
        elif 17 <= hour < 22:
            return "🌆 Good evening"
        else:
            return "🌙 Good night"
    
    @staticmethod
    def get_random_welcome_emoji() -> str:
        """Get random welcome emoji combination."""
        emoji_sets = [
            "🎉✨", "🚀💫", "⭐️🌟", "🎊🎈", "💎✨",
            "🔥⚡", "🌈☀️", "💫🌙", "🎯🎪", "🎭🎨"
        ]
        return random.choice(emoji_sets)
    
    def get_start_message(self, user_data: Dict[str, Any]) -> str:
        """Generate the cool start message with friendly & playful design."""
        greeting = self.get_time_based_greeting()
        name = user_data.get('first_name', 'Friend')
        emoji = self.get_random_welcome_emoji()
        
        return f"""
{emoji} *{greeting}, {name}!* {emoji}

┌─────────────────────────┐
│  🤖 *Your AI Assistant*   │
│    _is ready to help!_    │
└─────────────────────────┘

Hey there! I'm so excited you're here! 🚀

*I can help you with:*
• 📋 Managing your tasks
• 🔔 Setting reminders
• 📈 Tracking progress
• 💬 Answering questions
• 🎮 And much more!

🌈 *Let's make today amazing together!*

_What would you like to do first?_ 👇
"""

    def get_help_message(self) -> str:
        """Generate help message."""
        return """
📚 *Available Commands*

Here's everything I can do for you:

*Basic Commands:*
/start - _Start the bot and see main menu_
/help - _Show this help message_
/about - _Learn more about this bot_

*Task Management:*
/task - _Create or manage tasks_
/list - _View your task list_

*Utilities:*
/remind - _Set a reminder_
/stats - _View your statistics_

*Settings:*
/settings - _Configure your preferences_
/language - _Change language_

💡 *Pro Tips:*
• Type / to see all available commands
• Use inline buttons for quick navigation
• You can always return to main menu with /start

_Need more help? Just ask!_ 💬
"""

    def get_about_message(self) -> str:
        """Generate about message."""
        return """
ℹ️ *About This Bot*

━━━━━━━━━━━━━━━━━━━━━━
    🤖 *Utility Bot v2.0*
━━━━━━━━━━━━━━━━━━━━━━

Your personal AI-powered assistant designed to make your life easier!

*Features:*
• ⚡ Lightning-fast responses
• 🔐 Secure and private
• 🌍 Multi-language support
• 📊 Advanced analytics
• 🎨 Beautiful interface

*Technology Stack:*
• Built with Python 🐍
• Powered by aiogram 3.x
• Async/await architecture
• Modern design patterns

*Created with ❤️ by:*
Your Development Team

*Version:* 2.0.1
*Last Updated:* {datetime.now().strftime('%B %Y')}

_Thank you for using our bot!_ 🙏
"""

    def get_task_menu_message(self) -> str:
        """Generate task menu message."""
        return """
📋 *Task Manager*

Choose what you'd like to do:

• 📝 Create new task
• 📃 View all tasks
• ✅ Mark task complete
• 🗑️ Delete task
• 📊 Task statistics

_Select an option below:_
"""

    def get_alerts_menu_message(self) -> str:
        """Generate alerts menu message."""
        return """
🔔 *Notifications & Alerts*

Manage your notifications:

• ⏰ Set new reminder
• 📅 View scheduled alerts
• 🔕 Mute notifications
• ⚙️ Alert settings

_What would you like to do?_
"""

    def get_stats_message(self, user_stats: Optional[Dict[str, Any]] = None) -> str:
        """Generate statistics message."""
        if not user_stats:
            user_stats = {
                'total_tasks': 0,
                'completed_tasks': 0,
                'pending_tasks': 0,
                'streak_days': 0
            }
        
        completion_rate = (
            user_stats['completed_tasks'] / user_stats['total_tasks'] * 100
            if user_stats['total_tasks'] > 0 else 0
        )
        
        return f"""
📊 *Your Statistics*

━━━━━━━━━━━━━━━━━━━━━━

📈 *Task Performance:*
• Total Tasks: *{user_stats['total_tasks']}*
• Completed: *{user_stats['completed_tasks']}* ✅
• Pending: *{user_stats['pending_tasks']}* ⏳
• Completion Rate: *{completion_rate:.1f}%*

🔥 *Current Streak:* {user_stats['streak_days']} days

_Keep up the great work!_ 💪
"""

    def get_tools_menu_message(self) -> str:
        """Generate tools menu message."""
        return """
🛠️ *Utility Tools*

Available tools:

• 🧮 Calculator
• 🔤 Text formatter
• 🎲 Random generator
• ⏱️ Timer/Stopwatch
• 🌐 URL shortener
• 📝 Note taking

_Select a tool to use:_
"""

    def get_error_message(self, error_type: str = "generic") -> str:
        """Generate error messages."""
        error_messages = {
            "generic": "❌ Oops! Something went wrong. Please try again.",
            "not_found": "🔍 Command not found. Type /help for available commands.",
            "rate_limit": "⚠️ Too many requests! Please wait a moment.",
            "permission": "🚫 You don't have permission to do that.",
            "invalid_input": "❓ Invalid input. Please check and try again.",
            "maintenance": "🔧 Bot is under maintenance. Please try again later."
        }
        return error_messages.get(error_type, error_messages["generic"])

    def get_back_to_menu_text(self) -> str:
        """Get back to menu button text."""
        return "◀️ Back to Main Menu"

    def get_loading_messages(self) -> list:
        """Get progressive loading messages for animations."""
        return [
            "🤖 Initializing...",
            "🤖 Initializing... ✅",
            "🔧 Loading features...",
            "🔧 Loading features... ✅",
            "🚀 Preparing your workspace...",
            "✨ Almost ready...",
            "🎉 Welcome aboard!"
        ]

    def get_emoji_celebration(self) -> str:
        """Get emoji celebration for special occasions."""
        celebrations = [
            "🎉 🎊 🥳 🎈 🎆",
            "✨ 💫 ⭐ 🌟 💎",
            "🚀 🔥 ⚡ 💥 💫",
            "🌈 ☀️ 🌻 🌺 🌸",
            "🎯 🏆 🥇 👑 💪"
        ]
        return random.choice(celebrations)


# Global message templates instance
messages = MessageTemplates()