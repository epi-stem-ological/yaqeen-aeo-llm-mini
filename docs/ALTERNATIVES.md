# Alternatives Considered

## 1) Brave Search API
- Endpoint: `https://api.search.brave.com/res/v1/web/search`
- Auth: `X-Subscription-Token: <token>`
- Shape a `providers/brave.py` that mirrors the ProviderResult:
  - GET web results, collect URLs, match target domain, emit `cited`, `cited_urls`, `raw_urls`.
- Pros: modern search index; straightforward REST.
- Cons: paid key required for reviewers; API quotas vary.

## 2) “Classic” Bing Web Search (Global or Azure Cognitive Services)
- This repo includes `src/providers/bing.py`.
- Works with:
  - Global endpoint: `https://api.bing.microsoft.com/v7.0/search`
  - Azure endpoint: `https://<resource>.cognitiveservices.azure.com/bing/v7.0/search`
- Pros: widely available; stable shape.
- Cons: requires a key (reviewer supplies their own).
