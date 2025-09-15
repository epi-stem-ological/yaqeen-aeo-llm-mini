# src/providers/bing.py
from __future__ import annotations
import os
import requests
from typing import List
from src.providers.base import ProviderResult
from src.utils.domain import domain_matches

def _bing_base_and_path(endpoint: str) -> str:
    """Normalize endpoint and choose the correct path."""
    endpoint = endpoint.rstrip("/")
    # If you use the global Bing endpoint, path is /v7.0/search
    # If you use an Azure AI Services (Cognitive Services) endpoint, path is /bing/v7.0/search
    if "api.bing.microsoft.com" in endpoint:
        return f"{endpoint}/v7.0/search"
    else:
        return f"{endpoint}/bing/v7.0/search"

def search(question: str, target_domain: str) -> ProviderResult:
    """
    Query Bing Web Search and return a ProviderResult.
    Reads creds from:
      - BING_SEARCH_KEY        (required)
      - BING_SEARCH_ENDPOINT   (required; e.g. https://<your-resource>.cognitiveservices.azure.com
                                or https://api.bing.microsoft.com)
    """
    key = os.getenv("BING_SEARCH_KEY")
    endpoint = os.getenv("BING_SEARCH_ENDPOINT")

    if not key:
        raise RuntimeError("Missing BING_SEARCH_KEY environment variable.")
    if not endpoint:
        raise RuntimeError("Missing BING_SEARCH_ENDPOINT environment variable.")

    url = _bing_base_and_path(endpoint)
    headers = {"Ocp-Apim-Subscription-Key": key}
    params = {
        "q": question,
        "count": 10,
        "responseFilter": "Webpages",
        "textDecorations": "false",
        "textFormat": "Raw",
        # optionally: "mkt": "en-US",
        # optionally: "safeSearch": "Moderate",
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except requests.HTTPError as e:
        # On HTTP errors, return an empty result but keep raw error in raw_urls for debugging
        return ProviderResult(
            question=question,
            engine="bing",
            cited=False,
            cited_urls=[],
            raw_urls=[f"HTTPError {resp.status_code}: {getattr(resp, 'text', '')[:200]}"],
        )
    except Exception as e:
        return ProviderResult(
            question=question,
            engine="bing",
            cited=False,
            cited_urls=[],
            raw_urls=[f"Error: {e}"],
        )

    items = (data.get("webPages") or {}).get("value") or []
    raw_urls: List[str] = []
    for it in items:
        u = it.get("url")
        if u:
            raw_urls.append(u)

    cited_urls = [u for u in raw_urls if domain_matches(u, target_domain)]

    return ProviderResult(
        question=question,
        engine="bing",
        cited=bool(cited_urls),
        cited_urls=cited_urls,
        raw_urls=raw_urls,
    )
