#!/usr/bin/env python3
"""
Quick test script to verify bot structure and imports.
"""

import sys
from pathlib import Path

# Add bot directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        # Test config
        from bot.config import settings
        print("✅ Config module imported")
        
        # Test messages
        from bot.utils.messages import messages
        print("✅ Messages module imported")
        
        # Test keyboards
        from bot.keyboards.inline import keyboards
        print("✅ Keyboards module imported")
        
        # Test animations
        from bot.utils.animations import MessageAnimator
        print("✅ Animations module imported")
        
        # Test handlers
        from bot.handlers.start import setup_start_handler
        from bot.handlers.commands import setup_command_handlers
        print("✅ Handlers modules imported")
        
        # Test middleware
        from bot.middleware.logging import LoggingMiddleware
        from bot.middleware.throttling import ThrottlingMiddleware
        print("✅ Middleware modules imported")
        
        # Test main bot
        from bot.main import TelegramBot
        print("✅ Main bot module imported")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        return False

def test_message_generation():
    """Test message generation."""
    print("\n🧪 Testing message generation...")
    
    try:
        from bot.utils.messages import messages
        
        # Test start message
        user_data = {
            'first_name': 'Test User',
            'username': 'testuser',
            'user_id': 123456
        }
        
        start_msg = messages.get_start_message(user_data)
        print(f"✅ Start message generated ({len(start_msg)} chars)")
        
        # Test help message
        help_msg = messages.get_help_message()
        print(f"✅ Help message generated ({len(help_msg)} chars)")
        
        # Test about message
        about_msg = messages.get_about_message()
        print(f"✅ About message generated ({len(about_msg)} chars)")
        
        print("\n📝 Sample start message preview:")
        print("-" * 40)
        print(start_msg[:500] + "...")
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Message generation error: {e}")
        return False

def test_keyboard_creation():
    """Test keyboard creation."""
    print("\n🧪 Testing keyboard creation...")
    
    try:
        from bot.keyboards.inline import keyboards
        
        # Test main menu
        main_menu = keyboards.main_menu()
        print(f"✅ Main menu keyboard created")
        
        # Test back button
        back_btn = keyboards.back_to_menu()
        print(f"✅ Back button keyboard created")
        
        # Test task menu
        task_menu = keyboards.task_menu()
        print(f"✅ Task menu keyboard created")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Keyboard creation error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("🤖 TELEGRAM BOT STRUCTURE TEST")
    print("=" * 50)
    
    all_passed = True
    
    # Run tests
    if not test_imports():
        all_passed = False
    
    if not test_message_generation():
        all_passed = False
    
    if not test_keyboard_creation():
        all_passed = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("\n🚀 Bot structure is ready!")
        print("\nNext steps:")
        print("1. Create .env file with your BOT_TOKEN")
        print("2. Run: python run.py")
        print("3. Start your bot in Telegram with /start")
    else:
        print("❌ SOME TESTS FAILED")
        print("Please check the errors above.")
    print("=" * 50)

if __name__ == "__main__":
    main()