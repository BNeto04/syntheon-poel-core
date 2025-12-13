from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class PoelState:
    history: List[Dict[str, str]] = field(default_factory=list)
    mode: str = "normal"

    def add_user(self, text: str):
        self.history.append({"role": "user", "content": text})

    def add_assistant(self, text: str):
        self.history.append({"role": "assistant", "content": text})

    def get_recent(self, turns: int) -> List[Dict[str, str]]:
        return self.history[-(turns * 2):]
