from typing import List, Dict
from .state import PoelState
from .config import WORKING_MEMORY_TURNS
from .identity import POEL_INSTRUCTIONS

def extract_anchors(history: List[Dict[str, str]]) -> str:
    """
    Extracts structural decisions and key facts from the conversation history.

    This is a placeholder implementation. A real implementation would use NLP
    techniques to identify anchors like "app de finanças" or "stack: React".
    """
    # TODO: Implement a proper anchor extraction mechanism.
    return "No anchors defined yet. This is a placeholder."

def build_context(state: PoelState, user_text: str) -> List[Dict[str, str]]:
    """
    Builds the context for the LLM, including long-term anchors
    and the recent conversation window.
    """
    anchors = extract_anchors(state.history)
    recent_history = state.get_recent(WORKING_MEMORY_TURNS)

    system_prompt = f"""
{POEL_INSTRUCTIONS}

<anchors>
{anchors}
</anchors>
"""

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(recent_history)
    messages.append({"role": "user", "content": user_text})

    return messages
