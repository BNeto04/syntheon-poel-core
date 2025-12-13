import os
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("POEL_MODEL", "gpt-5.2")
MAX_OUTPUT_TOKENS = int(os.getenv("POEL_MAX_OUTPUT_TOKENS", "800"))
WINDOW_TURNS = int(os.getenv("POEL_WINDOW_TURNS", "12"))
