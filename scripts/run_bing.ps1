param(
  [string] = "yaqeeninstitute.org",
  [string] = "data\inputs\gold_questions.txt",
  [string] = "outputs\bing_run.csv",
  [string] = ".env"
)

# Load .env into the current process (if present)
if (Test-Path ) {
  Get-Content  | ForEach-Object {
    if ( -match '^\s*#' -or  -match '^\s*$') { return }
     =  -split '=', 2
    if (.Count -eq 2) {
       = [0].Trim()
       = [1].Trim()
      [Environment]::SetEnvironmentVariable(, , 'Process')
    }
  }
}

# Ensure venv is active
if (-not (Test-Path .\.venv)) { python -m venv .venv }
.\.venv\Scripts\Activate.ps1

# Guardrails: require both variables
if (-not  -or -not ) {
  Write-Error "Missing BING_SEARCH_KEY or BING_SEARCH_ENDPOINT. Put them in  or export them before running."
  exit 1
}

python -m src.cli --provider bing --domain  --inputs  --output 
Write-Host ("Wrote {0}" -f )
