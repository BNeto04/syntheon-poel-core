from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum, auto

class ConflictResolution(Enum):
    ASK_CLARIFICATION = auto()
    LAST_WINS = auto()
    MAINTAIN_BOTH = auto()

class CoherenceManager:
    def detect_conflict(self, new_fact: Dict[str, Any], state: 'PoelState') -> bool:
        """
        Detects if a new fact contradicts existing facts in the state.

        This is a placeholder implementation. A real implementation would
        use more sophisticated logic to find contradictions.
        """
        # TODO: Implement a proper conflict detection mechanism.
        # Placeholder: check for direct key-value contradictions.
        for fact in state.facts:
            if fact.get("key") == new_fact.get("key") and fact.get("value") != new_fact.get("value"):
                return True
        return False

    def resolve(self, strategy: ConflictResolution = ConflictResolution.LAST_WINS):
        """
        Resolves a detected conflict based on the chosen strategy.

        This is a placeholder implementation.
        """
        # TODO: Implement conflict resolution logic.
        # In a real implementation, this would contain logic for each strategy.
        pass

@dataclass
class PoelState:
    history: List[Dict[str, str]] = field(default_factory=list)
    facts: List[Dict[str, Any]] = field(default_factory=list)
    mode: str = "normal"
    coherence_manager: CoherenceManager = field(default_factory=CoherenceManager)

    def add_user(self, text: str):
        self.history.append({"role": "user", "content": text})
        # Placeholder for fact extraction from user input
        # new_fact = {"key": "database", "value": "MySQL"}
        # if self.coherence_manager.detect_conflict(new_fact, self):
        #     self.coherence_manager.resolve()

    def add_assistant(self, text: str):
        self.history.append({"role": "assistant", "content": text})

    def get_recent(self, turns: int) -> List[Dict[str, str]]:
        return self.history[-(turns * 2):]
