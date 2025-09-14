# src/providers/mock.py
from typing import Dict, List, Optional
from src.providers.base import Provider, ProviderResult
from src.utils.domain import domain_matches

class MockProvider(Provider):
    """Deterministic, no-network provider for local testing."""
    name = "mock"

    def __init__(self, fixtures: Optional[Dict[str, List[str]]] = None):
        self.fixtures = fixtures or {
            "what is yaqeen institute": ["https://yaqeeninstitute.org/about"],
            "does god exist": ["https://example.com/neutral", "https://yaqeeninstitute.org/read/some-paper"],
            "who is ibn taymiyyah": ["https://en.wikipedia.org/wiki/Ibn_Taymiyyah"],
        }

    def probe(self, question: str, target_domain: str) -> ProviderResult:
        urls = self.fixtures.get(question.strip().lower(), [])
        cited_urls = [u for u in urls if domain_matches(u, target_domain)]
        return ProviderResult(
            question=question,
            engine=self.name,
            cited=bool(cited_urls),
            cited_urls=cited_urls,
            raw_urls=urls,
        )
# --- CLI adapter ---
# Provide a module-level function so the CLI can call `mock.search`
_provider = MockProvider()

def search(query: str, target_domain: str) -> ProviderResult:
    return MockProvider().probe(query, target_domain)
