# src/providers/base.py
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List

@dataclass
class ProviderResult:
    question: str
    engine: str
    cited: bool
    cited_urls: List[str]
    raw_urls: List[str]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class Provider:
    name: str = "base"
    def probe(self, question: str, target_domain: str) -> ProviderResult:  # pragma: no cover
        raise NotImplementedError
    def __enter__(self):  # optional context manager
        return self
    def __exit__(self, exc_type, exc, tb):
        return False
