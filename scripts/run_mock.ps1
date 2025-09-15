# Run the offline-safe mock provider end-to-end
if (!(Test-Path .\.venv\Scripts\Activate.ps1)) { python -m venv .venv }
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

# Ensure inputs exist
if (!(Test-Path .\data\inputs\gold_questions.txt)) {
  Write-Host "Missing data\inputs\gold_questions.txt" -ForegroundColor Yellow
  exit 1
}

# Run
python -m src.cli --provider mock --domain yaqeeninstitute.org --inputs .\data\inputs\gold_questions.txt --output .\outputs\mock_run.csv

Write-Host "`nWrote outputs\mock_run.csv" -ForegroundColor Green
Get-Content .\outputs\mock_run.csv | Select-Object -First 10
