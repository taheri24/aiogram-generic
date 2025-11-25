"""Message animation utilities for cool effects."""

import asyncio
import random
from typing import List, Optional
from aiogram import Bot
from aiogram.types import Message
from loguru import logger


class MessageAnimator:
    """Handles message animations and cool effects."""
    
    def __init__(self, bot: Bot):
        """
        Initialize animator with bot instance.
        
        Args:
            bot: Aiogram Bot instance
        """
        self.bot = bot
    
    async def typing_effect(
        self, 
        chat_id: int, 
        duration: float = 2.0
    ) -> None:
        """
        Show typing indicator for specified duration.
        
        Args:
            chat_id: Chat ID to show typing in
            duration: Duration in seconds
        """
        try:
            await self.bot.send_chat_action(
                chat_id=chat_id, 
                action="typing"
            )
            await asyncio.sleep(duration)
        except Exception as e:
            logger.error(f"Error showing typing effect: {e}")
    
    async def progressive_reveal(
        self, 
        message: Message,
        stages: List[str],
        delay: float = 1.0,
        final_message: Optional[str] = None
    ) -> Message:
        """
        Progressively reveal message content with animation.
        
        Args:
            message: Original message to reply to
            stages: List of message stages to display
            delay: Delay between stages in seconds
            final_message: Optional final message to display
        
        Returns:
            The final message object
        """
        msg = None
        try:
            for stage in stages:
                if msg is None:
                    msg = await message.answer(stage)
                else:
                    await msg.edit_text(stage)
                await asyncio.sleep(delay)
            
            # Display final message if provided
            if final_message and msg:
                await msg.edit_text(final_message, parse_mode="Markdown")
            
            return msg
        except Exception as e:
            logger.error(f"Error in progressive reveal: {e}")
            return await message.answer("Welcome! 🎉")
    
    async def emoji_rain(
        self,
        message: Message,
        emojis: Optional[List[str]] = None,
        count: int = 10,
        duration: float = 2.0
    ) -> None:
        """
        Send emoji rain effect.
        
        Args:
            message: Message to reply to
            emojis: List of emojis to use
            count: Number of emojis to display
            duration: How long to show the emoji rain
        """
        if emojis is None:
            emojis = ["🎉", "✨", "🚀", "💫", "⭐", "🎊", "🎈", "🎆", "🌟", "💎"]
        
        try:
            emoji_msg = " ".join(random.choices(emojis, k=count))
            rain_msg = await message.answer(emoji_msg)
            await asyncio.sleep(duration)
            await rain_msg.delete()
        except Exception as e:
            logger.error(f"Error in emoji rain: {e}")
    
    async def welcome_animation(
        self,
        message: Message,
        user_name: str,
        enable_animations: bool = True
    ) -> Message:
        """
        Display welcome animation sequence.
        
        Args:
            message: Message to reply to
            user_name: User's name for personalization
            enable_animations: Whether to show animations
        
        Returns:
            Final welcome message
        """
        if not enable_animations:
            # Skip animation if disabled
            from bot.utils.messages import messages
            welcome_text = messages.get_start_message({'first_name': user_name})
            from bot.keyboards.inline import keyboards
            return await message.answer(
                text=welcome_text,
                reply_markup=keyboards.main_menu(),
                parse_mode="Markdown"
            )
        
        try:
            # Show typing effect
            await self.typing_effect(message.chat.id, 2)
            
            # Progressive reveal stages
            stages = [
                "🤖 Initializing...",
                "🤖 Initializing... ✅",
                "🔧 Loading features...",
                "🔧 Loading features... ✅",
                "🚀 Preparing your workspace...",
                "✨ Almost ready...",
            ]
            
            # Show progressive reveal
            msg = await self.progressive_reveal(
                message, 
                stages, 
                delay=0.8
            )
            
            # Show emoji celebration for new users
            await self.emoji_rain(message)
            
            # Send final welcome message
            from bot.utils.messages import messages
            welcome_text = messages.get_start_message({'first_name': user_name})
            from bot.keyboards.inline import keyboards
            
            if msg:
                await msg.delete()
            
            return await message.answer(
                text=welcome_text,
                reply_markup=keyboards.main_menu(),
                parse_mode="Markdown"
            )
            
        except Exception as e:
            logger.error(f"Error in welcome animation: {e}")
            # Fallback to simple welcome
            from bot.utils.messages import messages
            welcome_text = messages.get_start_message({'first_name': user_name})
            from bot.keyboards.inline import keyboards
            return await message.answer(
                text=welcome_text,
                reply_markup=keyboards.main_menu(),
                parse_mode="Markdown"
            )
    
    async def pulse_effect(
        self,
        message: Message,
        text: str,
        pulses: int = 3,
        delay: float = 0.5
    ) -> Message:
        """
        Create a pulsing text effect.
        
        Args:
            message: Message to reply to
            text: Text to pulse
            pulses: Number of pulses
            delay: Delay between pulses
        
        Returns:
            Final message
        """
        msg = None
        try:
            for i in range(pulses):
                if msg is None:
                    msg = await message.answer(f"_{text}_", parse_mode="Markdown")
                else:
                    await msg.edit_text(f"*{text}*", parse_mode="Markdown")
                await asyncio.sleep(delay)
                await msg.edit_text(f"_{text}_", parse_mode="Markdown")
                await asyncio.sleep(delay)
            
            await msg.edit_text(f"*{text}*", parse_mode="Markdown")
            return msg
        except Exception as e:
            logger.error(f"Error in pulse effect: {e}")
            return await message.answer(text)
    
    async def countdown_effect(
        self,
        message: Message,
        start: int = 3,
        end_text: str = "🚀 Let's go!"
    ) -> Message:
        """
        Show countdown animation.
        
        Args:
            message: Message to reply to
            start: Starting number for countdown
            end_text: Text to show after countdown
        
        Returns:
            Final message
        """
        msg = None
        try:
            for i in range(start, 0, -1):
                text = f"*{i}*" + " " + "⏳" * i
                if msg is None:
                    msg = await message.answer(text, parse_mode="Markdown")
                else:
                    await msg.edit_text(text, parse_mode="Markdown")
                await asyncio.sleep(1)
            
            await msg.edit_text(end_text, parse_mode="Markdown")
            return msg
        except Exception as e:
            logger.error(f"Error in countdown effect: {e}")
            return await message.answer(end_text)


# Export animator class
__all__ = ['MessageAnimator']