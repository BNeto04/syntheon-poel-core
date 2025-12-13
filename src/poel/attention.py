from .state import PoelState
from .config import WINDOW_TURNS

def build_input(state: PoelState, user_text: str):
    recent = state.get_recent(WINDOW_TURNS)
    return recent + [{"role": "user", "content": user_text}]
