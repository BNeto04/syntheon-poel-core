import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# OpenAI
MODEL = os.getenv("POEL_MODEL", "gpt-4o")
MAX_OUTPUT_TOKENS = int(os.getenv("POEL_MAX_OUTPUT_TOKENS", "800"))
WINDOW_TURNS = int(os.getenv("POEL_WINDOW_TURNS", "12"))

# Sechel Integration
SECHEL_API_URL = os.getenv("SECHEL_API_URL", "http://localhost:8001")
SECHEL_ENABLED = os.getenv("SECHEL_ENABLED", "false").lower() == "true"

# Session Management
SESSION_TTL = timedelta(hours=int(os.getenv("SESSION_TTL_HOURS", "3")))
SESSION_DIR = os.getenv("SESSION_DIR", ".sessions")
