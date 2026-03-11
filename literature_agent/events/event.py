from dataclasses import dataclass, field
from typing import Dict, Any
import uuid
import time


@dataclass
class Event:
    type: str
    payload: Dict[str, Any]
    source: str | None = None
    parent_id: str | None = None

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)