# Yaqeen AEO / LLM Visibility – Mini Project

AEO/LLM Visibility Mini Project: data‑driven diagnosis (GSC/GA4), a compact baseline, and a runnable Python CLI that checks citation of **yaqeeninstitute.org** across answer surfaces. The tool uses a pluggable provider pattern with a **mock** provider for offline testing and a **Bing Web Search** provider for real lookups.


# Mock (always works)
python -m src.cli --provider mock --domain yaqeeninstitute.org --inputs .\data\inputs\gold_questions.txt --output .\outputs\mock_run.csv

# Bing (optional; only if reviewer has a classic Bing Web Search key)
$env:BING_SEARCH_KEY="YOUR_WEB_SEARCH_KEY"
$env:BING_SEARCH_ENDPOINT="https://api.bing.microsoft.com"
python -m src.cli --provider bing --domain yaqeeninstitute.org --inputs .\data\inputs\gold_questions.txt --output .\outputs\bing_run.csv

---

## Quick Start (Windows / PowerShell)

```powershell
# 1) Create venv and install deps
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2) Run with the offline-safe provider (no keys needed)
.\scripts\run_mock.ps1

# 3) (Optional) Run with Bing Web Search if you have a key
#    Create a .env at repo root by copying .env.example, then fill:
#      BING_SEARCH_KEY=...
#      BING_SEARCH_ENDPOINT=https://api.bing.microsoft.com
.\scripts\run_bing.ps1
