#!/usr/bin/env python3
"""
Simple run script for the Telegram bot.
"""

import sys
from pathlib import Path

# Add bot directory to path
sys.path.insert(0, str(Path(__file__).parent))

from bot.main import run_bot

if __name__ == "__main__":
    run_bot()