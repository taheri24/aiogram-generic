# 🤖 Telegram Utility Bot with Cool Start Messages

A modern, feature-rich Telegram bot built with aiogram 3.x featuring engaging emoji-rich welcome messages, inline keyboard navigation, and essential utility commands.

## ✨ Features

### 🎨 Cool Start Message
- **Friendly & Playful Design**: Emoji-rich welcome messages with personalized greetings
- **Time-based Greetings**: Dynamic greetings based on time of day (Good morning/afternoon/evening)
- **Animation Effects**: Progressive message reveal and emoji celebrations for new users
- **Inline Keyboard Navigation**: 2x3 grid menu for easy navigation

### 📋 Core Functionality
- **Task Management**: Create, view, and manage tasks
- **Alerts & Reminders**: Set and manage notifications
- **Statistics**: Track your activity and progress
- **Utility Tools**: Calculator, text formatter, random generator, and more
- **Help System**: Comprehensive help with all available commands
- **About Section**: Learn more about the bot with social links

### 🛡️ Security & Performance
- **Rate Limiting**: Prevents spam with configurable limits
- **Anti-Spam Protection**: Detects and blocks repetitive messages
- **Command Cooldowns**: Prevents command abuse
- **Comprehensive Logging**: Track all bot activities
- **Error Handling**: Graceful error recovery with user-friendly messages

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/taheri24/aiogram-generic.git
cd aiogram-generic
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
```

Edit `.env` file with your configuration:
```env
# Bot Configuration
BOT_TOKEN=your_bot_token_here
BOT_NAME=Your Bot Name
BOT_USERNAME=@yourbotusername

# Admin Settings
ADMIN_IDS=123456789,987654321

# Logging
LOG_LEVEL=INFO
LOG_FILE=bot.log

# Features
ENABLE_ANIMATIONS=true
DEFAULT_MESSAGE_STYLE=friendly
RATE_LIMIT_PER_MINUTE=30
```

5. **Run the bot:**
```bash
python -m bot.main
```

## 📱 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | 🏠 Start the bot and show main menu |
| `/help` | ❓ Show help information |
| `/about` | ℹ️ About this bot |
| `/stats` | 📊 View your statistics |
| `/settings` | ⚙️ Bot settings |
| `/cancel` | ❌ Cancel current operation |

## 🎯 Usage Example

1. **Start the bot:**
   - Send `/start` to see the cool welcome message
   - Use the inline keyboard to navigate through features

2. **Access features:**
   - Click "📋 Tasks" to manage your tasks
   - Click "🔔 Alerts" to set reminders
   - Click "📊 Stats" to view your statistics
   - Click "🛠️ Tools" to access utility tools

3. **Get help:**
   - Send `/help` for a list of all commands
   - Send `/about` to learn more about the bot

## 🏗️ Project Structure

```
aiogram-generic/
├── bot/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── config.py            # Configuration management
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py         # /start command with cool messages
│   │   └── commands.py      # Other command handlers
│   ├── keyboards/
│   │   ├── __init__.py
│   │   └── inline.py        # Inline keyboard builders
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── messages.py      # Message templates
│   │   ├── animations.py    # Animation effects
│   │   └── logger.py        # Logging configuration
│   └── middleware/
│       ├── __init__.py
│       ├── logging.py       # Request logging
│       └── throttling.py    # Rate limiting
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🎨 Customization

### Changing the Welcome Message Style

Edit `bot/utils/messages.py` to customize the start message:

```python
def get_start_message(self, user_data: Dict[str, Any]) -> str:
    # Customize your welcome message here
    return f"""
    ✨ Your custom welcome message ✨
    Hello {user_data['first_name']}!
    """
```

### Adding New Commands

1. Add handler in `bot/handlers/commands.py`:
```python
async def your_command(self, message: Message):
    await message.answer("Your response")
```

2. Register in the router:
```python
self.router.message(Command("yourcommand"))(self.your_command)
```

### Modifying Inline Keyboards

Edit `bot/keyboards/inline.py` to customize keyboards:

```python
@staticmethod
def main_menu() -> InlineKeyboardMarkup:
    # Customize your keyboard layout
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Your Button", callback_data="your_action")]
    ])
    return keyboard
```

## 🐳 Docker Deployment

### Using Docker

1. **Build the image:**
```bash
docker build -t telegram-bot .
```

2. **Run the container:**
```bash
docker run -d --name my-bot --env-file .env telegram-bot
```

### Using Docker Compose

```bash
docker-compose up -d
```

## 📊 Monitoring & Logs

Logs are stored in the `logs/` directory:
- `bot.log` - Main application logs
- Logs rotate daily and are kept for 7 days
- Compressed archives for older logs

View logs:
```bash
tail -f logs/bot.log
```

## 🔧 Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `BOT_TOKEN` | Telegram Bot API token | Required |
| `BOT_NAME` | Bot display name | "Utility Bot" |
| `ADMIN_IDS` | Comma-separated admin IDs | [] |
| `LOG_LEVEL` | Logging level | "INFO" |
| `ENABLE_ANIMATIONS` | Enable message animations | true |
| `RATE_LIMIT_PER_MINUTE` | Max requests per minute | 30 |

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [aiogram](https://github.com/aiogram/aiogram) - Modern Telegram Bot API framework
- Logging with [loguru](https://github.com/Delgan/loguru) - Python logging made simple
- Configuration with [pydantic](https://github.com/pydantic/pydantic) - Data validation using Python type annotations

## 📞 Support

- 💬 [Support Chat](https://t.me/support)
- 📢 [News Channel](https://t.me/news)
- 📧 [Email Support](mailto:support@example.com)

## 🎯 Roadmap

- [ ] Database integration for persistent data
- [ ] Multi-language support
- [ ] Advanced task scheduling
- [ ] Voice message support
- [ ] File sharing capabilities
- [ ] Web dashboard for analytics
- [ ] Webhook support for production
- [ ] Custom themes and personalization

---

**Made with ❤️ by Your Development Team**

*Version 2.0.1 - Last updated: November 2024*