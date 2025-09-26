"""
MeetMogger AI - Production-Ready Call Intelligence Platform

This is the main entry point for the refactored MeetMogger AI application.
It uses the new modular architecture with proper separation of concerns.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Import and run the dashboard
from meetmogger.main import main

if __name__ == "__main__":
    main()
