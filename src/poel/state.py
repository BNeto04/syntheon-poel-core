from datetime import datetime
from .schemas import PoelStateData, HistoryTurn
from .config import settings


class PoelState:
    def __init__(self, data: PoelStateData):
        self._data = data

    @classmethod
    def create_new(cls, session_id: str = None) -> "PoelState":
        if session_id:
            return cls(PoelStateData(session_id=session_id))
        return cls(PoelStateData())

    @property
    def session_id(self) -> str:
        return self._data.session_id

    def add_user(self, text: str):
        self._data.turn_id += 1
        self._data.last_active = datetime.now()
        self._data.history.append(
            HistoryTurn(
                role="user",
                content=text,
                turn_id=self._data.turn_id,
                timestamp=self._data.last_active,
            )
        )

    def add_assistant(self, text: str):
        self._data.last_active = datetime.now()
        self._data.history.append(
            HistoryTurn(
                role="assistant",
                content=text,
                turn_id=self._data.turn_id,
                timestamp=self._data.last_active,
            )
        )

    def get_recent_dict(self, turns: int) -> list[dict]:
        recent_turns = self._data.history[-(turns * 2) :]
        return [turn.model_dump(include={"role", "content"}) for turn in recent_turns]

    def is_expired(self) -> bool:
        return datetime.now() - self._data.created_at > settings.SESSION_TTL

    def to_json(self) -> str:
        # Pydantic's `model_dump_json` handles datetime serialization correctly
        return self._data.model_dump_json(indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "PoelState":
        data = PoelStateData.model_validate_json(json_str)
        return cls(data)

    @property
    def turn_id(self) -> int:
        return self._data.turn_id

    def truncate_history(self, max_turns: int = None):
        """Mantém apenas últimos N turnos."""
        if max_turns is None:
            max_turns = settings.POEL_WINDOW_TURNS * 2

        if len(self._data.history) > max_turns:
            self._data.history = self._data.history[-max_turns:]
