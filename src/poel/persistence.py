import json
import time
import uuid
from pathlib import Path
from .state import PoelState
from .config import MAX_WINDOW_TURNS, SESSION_TTL

SESSION_DIR = Path("sessions")
SESSION_DIR.mkdir(exist_ok=True)

def get_session_file(session_id: str) -> Path:
    return SESSION_DIR / f"{session_id}.json"

def load_state(session_id: str) -> PoelState:
    session_file = get_session_file(session_id)
    if session_file.exists():
        # Check if the session has expired
        last_modified = session_file.stat().st_mtime
        if time.time() - last_modified > SESSION_TTL:
            return PoelState()  # Return a new state if expired

        data = json.loads(session_file.read_text(encoding="utf-8"))
        state = PoelState()
        state.history = data.get("history", [])
        state.facts = data.get("facts", [])
        state.mode = data.get("mode", "normal")
        return state
    return PoelState()

def save_state(session_id: str, state: PoelState):
    max_items = MAX_WINDOW_TURNS * 2
    state.history = state.history[-max_items:]
    data = {
        "history": state.history,
        "facts": state.facts,
        "mode": state.mode
    }
    session_file = get_session_file(session_id)
    session_file.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def create_new_session() -> str:
    return str(uuid.uuid4())

def get_last_session() -> str | None:
    files = sorted(SESSION_DIR.iterdir(), key=lambda f: f.stat().st_mtime, reverse=True)
    if not files:
        return None

    last_session_file = files[0]
    last_modified = last_session_file.stat().st_mtime
    if time.time() - last_modified > SESSION_TTL:
        return None # Session has expired

    return last_session_file.stem
