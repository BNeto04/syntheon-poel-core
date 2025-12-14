import os
from dotenv import load_dotenv

load_dotenv()

# conversation settings
MODEL = os.getenv("POEL_MODEL", "gpt-5.2")
MAX_OUTPUT_TOKENS = int(os.getenv("POEL_MAX_OUTPUT_TOKENS", "800"))
# The maximum number of turns to store in the session history.
MAX_WINDOW_TURNS = int(os.getenv("POEL_WINDOW_TURNS", "12"))

# memory settings
SESSION_TTL = int(os.getenv("POEL_SESSION_TTL", "3600"))
# The number of turns to include in the context window for the LLM.
WORKING_MEMORY_TURNS = int(os.getenv("POEL_WORKING_MEMORY_TURNS", "10"))
CHECKPOINT_STRATEGY = os.getenv("POEL_CHECKPOINT_STRATEGY", "ephemeral")
