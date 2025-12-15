from pathlib import Path
from .state import PoelState
from .config import settings
import json

Path(settings.SESSION_DIR).mkdir(exist_ok=True)


def load_state(session_id: str = None) -> PoelState:
    """Carrega estado de uma sessão específica ou a última ativa."""

    if not session_id:
        session_id = _get_last_active_session()
        if not session_id:
            return PoelState.create_new()

    state_file = Path(settings.SESSION_DIR) / f"{session_id}.json"

    if not state_file.exists():
        return PoelState.create_new(session_id=session_id)

    try:
        state = PoelState.from_json(state_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError):
        print(f"⚠️  Sessão {session_id[:8]} corrompida. Criando nova sessão.")
        return PoelState.create_new()

    if state.is_expired():
        print(f"⚠️  Sessão {session_id[:8]} expirou. Criando nova sessão.")
        return PoelState.create_new()

    return state


def save_state(state: PoelState):
    """Salva estado."""
    state_file = Path(settings.SESSION_DIR) / f"{state.session_id}.json"
    state_file.write_text(state.to_json(), encoding="utf-8")


def _get_last_active_session() -> str | None:
    """Retorna session_id mais recente."""
    session_dir = Path(settings.SESSION_DIR)
    if not session_dir.exists():
        return None

    sessions = list(session_dir.glob("*.json"))
    if not sessions:
        return None

    latest = max(sessions, key=lambda p: p.stat().st_mtime)
    return latest.stem
