# src/check_citations.py
import argparse
import csv
from pathlib import Path

from src.providers.base import ProviderResult
from src.providers.bing import BingProvider
from src.providers.mock import MockProvider

def read_questions(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    ap = argparse.ArgumentParser(description="LLM/Answer-surface citation checker → CSV")
    ap.add_argument("--questions", required=True, help="Path to TXT with one question per line")
    ap.add_argument("--engine", choices=["bing", "mock"], default="bing", help="Which engine/provider to use")
    ap.add_argument("--domain", required=True, help="Target domain (e.g., yaqeeninstitute.org)")
    ap.add_argument("--out", default="outputs/llm_citations.csv", help="CSV output path")
    ap.add_argument("--delay", type=float, default=6.0, help="Seconds between requests (politeness)")
    ap.add_argument("--max-results", type=int, default=10, help="How many top results to scan")
    ap.add_argument("--headful", action="store_true", help="Show browser (debug)")
    args = ap.parse_args()

    Path(Path(args.out).parent).mkdir(parents=True, exist_ok=True)
    questions = read_questions(args.questions)

    if args.engine == "bing":
        provider_ctx = BingProvider(headless=not args.headful, delay=args.delay, max_results=args.max_results)
    else:
        provider_ctx = MockProvider()

    with provider_ctx as provider, open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["question", "engine", "cited", "cited_urls", "raw_urls", "timestamp"],
        )
        writer.writeheader()

        for q in questions:
            try:
                res: ProviderResult = provider.probe(q, args.domain)
            except Exception as e:
                print(f"Error probing '{q}': {e}")
                continue

            writer.writerow({
                "question": res.question,
                "engine": res.engine,
                "cited": int(res.cited),
                "cited_urls": "|".join(res.cited_urls),
                "raw_urls": "|".join(res.raw_urls),
                "timestamp": res.timestamp,
            })
            print(f"[{res.engine}] {q} → cited={res.cited} ({len(res.cited_urls)}/{len(res.raw_urls)})")

    print(f"\nCSV written → {args.out}")

if __name__ == "__main__":
    main()
