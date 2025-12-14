import json
from pathlib import Path
from datetime import datetime
from .state import PoelState
from .config import WINDOW_TURNS, SESSION_DIR, SESSION_TTL

Path(SESSION_DIR).mkdir(exist_ok=True)

def load_state(session_id: str = None) -> PoelState:
    """Carrega estado de uma sessão específica ou a última ativa."""

    if not session_id:
        session_id = _get_last_active_session()
        if not session_id:
            return PoelState()

    state_file = Path(SESSION_DIR) / f"{session_id}.json"

    if not state_file.exists():
        return PoelState(session_id=session_id)

    data = json.loads(state_file.read_text(encoding="utf-8"))

    # Reconstruir state
    state = PoelState(session_id=session_id)
    state.history = data.get("history", [])
    state.mode = data.get("mode", "normal")
    state.turn_id = data.get("turn_id", 0)
    state.created_at = datetime.fromisoformat(data["created_at"])
    state.last_active = datetime.fromisoformat(data["last_active"])

    # Verificar expiração
    if state.is_expired(SESSION_TTL):
        print(f"⚠️  Sessão {session_id[:8]} expirou. Criando nova sessão.")
        return PoelState()

    return state

def save_state(state: PoelState):
    """Salva estado com truncamento de janela."""
    max_items = WINDOW_TURNS * 2
    state.history = state.history[-max_items:]

    data = {
        "session_id": state.session_id,
        "history": state.history,
        "mode": state.mode,
        "turn_id": state.turn_id,
        "created_at": state.created_at.isoformat(),
        "last_active": state.last_active.isoformat()
    }

    state_file = Path(SESSION_DIR) / f"{state.session_id}.json"
    state_file.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def _get_last_active_session() -> str | None:
    """Retorna session_id mais recente."""
    session_dir = Path(SESSION_DIR)
    if not session_dir.exists():
        return None

    sessions = list(session_dir.glob("*.json"))
    if not sessions:
        return None

    # Ordenar por última modificação
    latest = max(sessions, key=lambda p: p.stat().st_mtime)
    return latest.stem  # nome do arquivo sem .json
