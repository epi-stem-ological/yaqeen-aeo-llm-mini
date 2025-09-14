# src/providers/bing.py
from typing import List
from urllib.parse import quote_plus
import time

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
from src.providers.base import Provider, ProviderResult
from src.utils.domain import domain_matches

class BingProvider(Provider):
    """
    Scrapes Bing web results (public SERP) for a query and checks if target domain appears.
    Uses Playwright (Chromium). No login. Be gentle with --delay.
    """
    name = "bing-web"

    def __init__(self, headless: bool = True, delay: float = 6.0, max_results: int = 10):
        self.headless = headless
        self.delay = delay
        self.max_results = max_results
        self._play = None
        self._browser = None
        self._context = None
        self._page = None

    def __enter__(self):
        self._play = sync_playwright().start()
        self._browser = self._play.chromium.launch(headless=self.headless)
        self._context = self._browser.new_context()
        self._page = self._context.new_page()
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if self._context:
                self._context.close()
            if self._browser:
                self._browser.close()
        finally:
            if self._play:
                self._play.stop()

    def _search_links(self, q: str) -> List[str]:
        url = f"https://www.bing.com/search?q={quote_plus(q)}"
        self._page.goto(url, wait_until="domcontentloaded", timeout=30000)
        self._page.wait_for_selector("#b_content", timeout=30000)

        links: List[str] = []
        # organic result selectors
        for a in self._page.query_selector_all("li.b_algo h2 a, ol#b_results li h2 a"):
            href = a.get_attribute("href")
            if href and href.startswith("http"):
                links.append(href)
                if len(links) >= self.max_results:
                    break
        return links

    def probe(self, question: str, target_domain: str) -> ProviderResult:
        if self.delay:
            time.sleep(self.delay)  # politeness between requests
        try:
            urls = self._search_links(question)
        except PWTimeout:
            urls = []

        cited_urls = [u for u in urls if domain_matches(u, target_domain)]
        return ProviderResult(
            question=question,
            engine=self.name,
            cited=bool(cited_urls),
            cited_urls=cited_urls,
            raw_urls=urls,
        )
