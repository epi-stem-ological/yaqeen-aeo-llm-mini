# src/cli.py
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone   # <-- added
from typing import Callable, Dict, Iterable, List

from src.providers.base import ProviderResult
from src.providers import mock, bing  # providers we have

# A provider is any callable that takes (query, target_domain) -> ProviderResult
ProviderFn = Callable[[str, str], ProviderResult]

PROVIDERS: Dict[str, ProviderFn] = {
    "mock": mock.search,
    "bing": bing.search,
}

def _iter_questions(inputs_path: str | None, single_query: str | None) -> Iterable[str]:
    """Yield questions from a file (one per line) or a single CLI query.
    Strips any UTF-8 BOM and surrounding whitespace.
    """
    def _clean(s: str) -> str:
        return s.lstrip("\ufeff").strip()

    if inputs_path:
        with open(inputs_path, "r", encoding="utf-8-sig") as f:
            for line in f:
                q = _clean(line)
                if q:
                    yield q
    else:
        assert single_query is not None
        yield _clean(single_query)

def _write_csv(results: List[ProviderResult], path: str) -> None:
    fieldnames = ["question", "engine", "cited", "cited_urls", "raw_urls", "timestamp"]  # <-- added timestamp
    now_iso = datetime.now(timezone.utc).isoformat()  # <-- added
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in results:
            w.writerow({
                "question": r.question,
                "engine": r.engine,
                "cited": str(r.cited),
                "cited_urls": ";".join(r.cited_urls),
                "raw_urls": ";".join(r.raw_urls),
                "timestamp": now_iso,  # <-- added
            })

def main() -> None:
    p = argparse.ArgumentParser(
        description="Probe whether search results cite a specific target domain.",
    )
    p.add_argument("--provider", choices=sorted(PROVIDERS.keys()), default="mock",
                   help="Which search provider to use.")
    # accept both --target-domain and --domain
    p.add_argument("--target-domain", "--domain", dest="target_domain", required=True,
                   help="Domain you expect/hope to see in the citations (e.g., yaqeeninstitute.org).")
    p.add_argument("--inputs", help="Path to a newline-delimited questions file.")
    p.add_argument("--output", help="Path to write CSV results. If omitted, prints to stdout.")
    p.add_argument("query", nargs="?", help="Single question if --inputs is not provided.")
    args = p.parse_args()

    if not args.inputs and not args.query:
        p.error("Provide a QUERY or --inputs <file>.")

    provider = PROVIDERS[args.provider]
    results: List[ProviderResult] = []

    for q in _iter_questions(args.inputs, args.query):
        r = provider(q, args.target_domain)
        results.append(r)
        if not args.output:
            print(f"[{r.engine}] {q} -> cited={r.cited} "
                  f"cited_urls={r.cited_urls} raw_urls={r.raw_urls}")

    if args.output:
        _write_csv(results, args.output)

if __name__ == "__main__":
    main()
