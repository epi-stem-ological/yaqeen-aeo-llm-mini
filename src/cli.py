import argparse
from typing import Dict, Callable, List
from .models import SearchResult
from .utils.domain import domain_matches

# Providers
from .providers import mock
try:
    from .providers import bing_api  # optional
    HAS_BING = True
except Exception:
    HAS_BING = False

ProviderFn = Callable[[str, int], List[SearchResult]]

PROVIDERS: Dict[str, ProviderFn] = {"mock": mock.search}
if HAS_BING:
    PROVIDERS["bing"] = bing_api.search

def main():
    ap = argparse.ArgumentParser(description="Check if search results cite a target domain.")
    ap.add_argument("query", help="Search query (e.g. 'what is hadith')")
    ap.add_argument("--provider", choices=sorted(PROVIDERS.keys()), default="mock", help="Search provider")
    ap.add_argument("--target-domain", default="yaqeeninstitute.org", help="Domain to look for")
    ap.add_argument("--count", type=int, default=10, help="Number of results to inspect")
    args = ap.parse_args()

    results = PROVIDERS[args.provider](args.query, args.count)

    found_any = False
    for i, r in enumerate(results, 1):
        is_match = domain_matches(r.url, args.target_domain)
        if is_match:
            found_any = True
        mark = "Y" if is_match else " "
        print(f"{i:2}. [{mark}] {r.title} — {r.url}")

    if found_any:
        print(f"\n✅ Found at least one result from {args.target_domain}")
    else:
        print(f"\n❌ No results from {args.target_domain}")

if __name__ == "__main__":
    main()
