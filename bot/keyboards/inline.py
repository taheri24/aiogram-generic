"""Inline keyboard builders for the bot."""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Optional


class InlineKeyboards:
    """Factory for creating inline keyboards."""
    
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        """Create main menu keyboard with 2x3 grid layout."""
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="📋 Tasks", callback_data="menu:tasks"),
                InlineKeyboardButton(text="🔔 Alerts", callback_data="menu:alerts")
            ],
            [
                InlineKeyboardButton(text="📊 Stats", callback_data="menu:stats"),
                InlineKeyboardButton(text="🛠️ Tools", callback_data="menu:tools")
            ],
            [
                InlineKeyboardButton(text="❓ Help", callback_data="menu:help"),
                InlineKeyboardButton(text="ℹ️ About", callback_data="menu:about")
            ]
        ])
        return keyboard
    
    @staticmethod
    def back_to_menu() -> InlineKeyboardMarkup:
        """Create back to menu button."""
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Back to Main Menu", callback_data="back:menu")]
        ])
        return keyboard
    
    @staticmethod
    def task_menu() -> InlineKeyboardMarkup:
        """Create task management menu."""
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="📝 Create Task", callback_data="task:create"),
                InlineKeyboardButton(text="📃 View Tasks", callback_data="task:view")
            ],
            [
                InlineKeyboardButton(text="✅ Complete Task", callback_data="task:complete"),
                InlineKeyboardButton(text="🗑️ Delete Task", callback_data="task:delete")
            ],
            [
                InlineKeyboardButton(text="📊 Task Stats", callback_data="task:stats")
            ],
            [
                InlineKeyboardButton(text="◀️ Back", callback_data="back:menu")
            ]
        ])
        return keyboard
    
    @staticmethod
    def alerts_menu() -> InlineKeyboardMarkup:
        """Create alerts management menu."""
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="⏰ Set Reminder", callback_data="alert:set"),
                InlineKeyboardButton(text="📅 View Alerts", callback_data="alert:view")
            ],
            [
                InlineKeyboardButton(text="🔕 Mute", callback_data="alert:mute"),
                InlineKeyboardButton(text="⚙️ Settings", callback_data="alert:settings")
            ],
            [
                InlineKeyboardButton(text="◀️ Back", callback_data="back:menu")
            ]
        ])
        return keyboard
    
    @staticmethod
    def tools_menu() -> InlineKeyboardMarkup:
        """Create tools menu."""
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🧮 Calculator", callback_data="tool:calc"),
                InlineKeyboardButton(text="🔤 Text Format", callback_data="tool:text")
            ],
            [
                InlineKeyboardButton(text="🎲 Random", callback_data="tool:random"),
                InlineKeyboardButton(text="⏱️ Timer", callback_data="tool:timer")
            ],
            [
                InlineKeyboardButton(text="🌐 URL Short", callback_data="tool:url"),
                InlineKeyboardButton(text="📝 Notes", callback_data="tool:notes")
            ],
            [
                InlineKeyboardButton(text="◀️ Back", callback_data="back:menu")
            ]
        ])
        return keyboard
    
    @staticmethod
    def settings_menu() -> InlineKeyboardMarkup:
        """Create settings menu."""
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🌍 Language", callback_data="settings:language"),
                InlineKeyboardButton(text="🎨 Theme", callback_data="settings:theme")
            ],
            [
                InlineKeyboardButton(text="🔔 Notifications", callback_data="settings:notifications"),
                InlineKeyboardButton(text="👤 Profile", callback_data="settings:profile")
            ],
            [
                InlineKeyboardButton(text="◀️ Back", callback_data="back:menu")
            ]
        ])
        return keyboard
    
    @staticmethod
    def confirm_action(action_id: str) -> InlineKeyboardMarkup:
        """Create confirmation keyboard."""
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Yes", callback_data=f"confirm:yes:{action_id}"),
                InlineKeyboardButton(text="❌ No", callback_data=f"confirm:no:{action_id}")
            ]
        ])
        return keyboard
    
    @staticmethod
    def pagination(current_page: int, total_pages: int, callback_prefix: str) -> InlineKeyboardMarkup:
        """Create pagination keyboard."""
        buttons = []
        
        # Previous button
        if current_page > 1:
            buttons.append(InlineKeyboardButton(
                text="◀️ Previous",
                callback_data=f"{callback_prefix}:page:{current_page-1}"
            ))
        
        # Page indicator
        buttons.append(InlineKeyboardButton(
            text=f"📄 {current_page}/{total_pages}",
            callback_data="noop"
        ))
        
        # Next button
        if current_page < total_pages:
            buttons.append(InlineKeyboardButton(
                text="Next ▶️",
                callback_data=f"{callback_prefix}:page:{current_page+1}"
            ))
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            buttons,
            [InlineKeyboardButton(text="◀️ Back", callback_data="back:menu")]
        ])
        return keyboard
    
    @staticmethod
    def rate_bot() -> InlineKeyboardMarkup:
        """Create rating keyboard."""
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="⭐", callback_data="rate:1"),
                InlineKeyboardButton(text="⭐⭐", callback_data="rate:2"),
                InlineKeyboardButton(text="⭐⭐⭐", callback_data="rate:3"),
                InlineKeyboardButton(text="⭐⭐⭐⭐", callback_data="rate:4"),
                InlineKeyboardButton(text="⭐⭐⭐⭐⭐", callback_data="rate:5")
            ],
            [
                InlineKeyboardButton(text="💬 Leave Feedback", callback_data="feedback"),
                InlineKeyboardButton(text="◀️ Skip", callback_data="back:menu")
            ]
        ])
        return keyboard
    
    @staticmethod
    def social_links() -> InlineKeyboardMarkup:
        """Create social media links keyboard."""
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="💬 Support Chat", url="https://t.me/support"),
                InlineKeyboardButton(text="📢 News Channel", url="https://t.me/news")
            ],
            [
                InlineKeyboardButton(text="🌐 Website", url="https://example.com"),
                InlineKeyboardButton(text="📧 Email", url="mailto:support@example.com")
            ],
            [
                InlineKeyboardButton(text="◀️ Back", callback_data="back:menu")
            ]
        ])
        return keyboard


# Global keyboards instance
keyboards = InlineKeyboards()