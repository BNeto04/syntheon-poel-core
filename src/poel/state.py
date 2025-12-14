from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime
import uuid

@dataclass
class PoelState:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    history: List[Dict[str, str]] = field(default_factory=list)
    mode: str = "normal"
    turn_id: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)

    def add_user(self, text: str):
        self.turn_id += 1
        self.last_active = datetime.now()
        self.history.append({
            "role": "user",
            "content": text,
            "turn_id": self.turn_id,
            "timestamp": self.last_active.isoformat()
        })

    def add_assistant(self, text: str):
        self.last_active = datetime.now()
        self.history.append({
            "role": "assistant",
            "content": text,
            "turn_id": self.turn_id,
            "timestamp": self.last_active.isoformat()
        })

    def get_recent(self, turns: int) -> List[Dict[str, str]]:
        return self.history[-(turns * 2):]

    def is_expired(self, ttl) -> bool:
        return datetime.now() - self.created_at > ttl
