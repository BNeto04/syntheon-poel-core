import json
from pathlib import Path
from .state import PoelState
from .config import WINDOW_TURNS

STATE_FILE = Path("poel_state.json")

def load_state() -> PoelState:
    if STATE_FILE.exists():
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        state = PoelState()
        state.history = data.get("history", [])
        state.mode = data.get("mode", "normal")
        return state
    return PoelState()

def save_state(state: PoelState):
    max_items = WINDOW_TURNS * 2
    state.history = state.history[-max_items:]
    data = {"history": state.history, "mode": state.mode}
    STATE_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
