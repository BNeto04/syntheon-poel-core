from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from datetime import datetime
import uuid


class HistoryTurn(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    turn_id: int
    timestamp: datetime


class ContextPack(BaseModel):
    canonical_state: str
    relevant_context: str
    open_conflicts: List[str]
    trace: List[str]


class PoelStateData(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    history: List[HistoryTurn] = Field(default_factory=list)
    mode: str = "normal"
    turn_id: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    last_active: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
