# src/utils/gsc_to_gold_questions.py
import argparse
from pathlib import Path
import pandas as pd

def pick_column(df, candidates):
    cols = {c.lower().strip(): c for c in df.columns}
    for name in candidates:
        if name in cols:
            return cols[name]
    return None

def main():
    ap = argparse.ArgumentParser(description="Derive 15–20 gold questions from GSC export.")
    ap.add_argument("--infile", default="data/inputs/GSC Export.xlsx", help="Path to GSC Excel export")
    ap.add_argument("--sheet", default=0, help="Excel sheet index or name")
    ap.add_argument("--top", type=int, default=20, help="How many questions to output")
    ap.add_argument("--outfile", default="data/derived/gold_questions.txt", help="Where to write one question per line")
    args = ap.parse_args()

    df = pd.read_excel(args.infile, sheet_name=args.sheet)

    qcol = pick_column(df, ["query", "queries", "search query"])
    if not qcol:
        raise SystemExit("Could not find a 'Query' column in your GSC export.")
    clicol = pick_column(df, ["clicks", "click"])
    impcol = pick_column(df, ["impressions", "impr", "impressions count"])

    use_cols = [qcol] + [c for c in [clicol, impcol] if c]
    df = df[use_cols].rename(columns={qcol: "query"})
    df["query"] = df["query"].astype(str).str.strip()
    df = df[df["query"].str.len() > 0]

    # Simple score: clicks*2 + impressions (fallbacks if missing)
    if clicol and impcol:
        df["score"] = df[clicol].fillna(0) * 2 + df[impcol].fillna(0)
    elif clicol:
        df["score"] = df[clicol].fillna(0)
    elif impcol:
        df["score"] = df[impcol].fillna(0)
    else:
        df["score"] = 1

    top = df.sort_values("score", ascending=False).drop_duplicates("query").head(args.top)
    Path(Path(args.outfile).parent).mkdir(parents=True, exist_ok=True)
    top["query"].to_csv(args.outfile, index=False, header=False)
    print(f"Wrote {len(top)} questions → {args.outfile}")

if __name__ == "__main__":
    main()
