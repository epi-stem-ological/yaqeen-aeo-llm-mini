# Optional: run with Bing Web Search if you have a key
# Put the following in a .env at repo root OR set them in this shell:
#   BING_SEARCH_KEY=...
#   BING_SEARCH_ENDPOINT=https://api.bing.microsoft.com
#
# This loader sets $env: vars for this process from .env if present:
if (Test-Path .\.env) {
  (Get-Content .\.env) | ForEach-Object {
    if ($_ -match '^\s*#' -or $_ -match '^\s*$') { return }
    $kv = $_ -split '=',2
    if ($kv.Length -eq 2) {
      $name = $kv[0].Trim()
      $val  = $kv[1].Trim()
      $ExecutionContext.SessionState.PSVariable.Set(( "env:" + $name ), $val)
    }
  }
}

if (-not $env:BING_SEARCH_KEY -or -not $env:BING_SEARCH_ENDPOINT) {
  Write-Host "BING_SEARCH_KEY/BING_SEARCH_ENDPOINT not set. See .env.example." -ForegroundColor Yellow
  exit 1
}

if (!(Test-Path .\.venv\Scripts\Activate.ps1)) { python -m venv .venv }
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

python -m src.cli --provider bing --domain yaqeeninstitute.org --inputs .\data\inputs\gold_questions.txt --output .\outputs\bing_run.csv

Write-Host "`nWrote outputs\bing_run.csv" -ForegroundColor Green
Get-Content .\outputs\bing_run.csv | Select-Object -First 10
