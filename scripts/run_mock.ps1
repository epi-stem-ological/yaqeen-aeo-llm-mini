param(
  [string] = "yaqeeninstitute.org",
  [string] = "data\inputs\gold_questions.txt",
  [string] = "outputs\mock_run.csv"
)

# Ensure venv is active
if (-not (Test-Path .\.venv)) { python -m venv .venv }
.\.venv\Scripts\Activate.ps1

# Run with mock provider (no keys needed)
python -m src.cli --provider mock --domain  --inputs  --output 
Write-Host ("Wrote {0}" -f )
