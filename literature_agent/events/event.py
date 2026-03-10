from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Event:
    type: str
    payload: Dict[str, Any]
    source: str | None = None