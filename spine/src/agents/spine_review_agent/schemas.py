from dataclasses import dataclass
from typing import List

@dataclass
class PaperExtraction:
    research_problem: str
    materials: List[str]
    methods: List[str]
    key_findings: List[str]
    limitations: List[str]
