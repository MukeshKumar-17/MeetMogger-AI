"""
Main entry point for MeetMogger AI application.

Provides command-line interface and application initialization.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ui.dashboard import create_dashboard
from utils.logger import setup_logger

# Setup logging
logger = setup_logger("meetmogger_main")


def main():
    """Main application entry point."""
    try:
        logger.info("Starting MeetMogger AI application")
        create_dashboard()
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise


if __name__ == "__main__":
    main()
