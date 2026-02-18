$ErrorActionPreference = 'Stop'

function Run([string]$line) {
  Write-Host "Running: $line" -ForegroundColor Cyan
  & powershell -NoProfile -Command $line
  if ($LASTEXITCODE -ne 0) {
    throw "Command failed (exit=$LASTEXITCODE): $line"
  }
}

Write-Host ""
Write-Host "YY-FE QA: start" -ForegroundColor Green
Write-Host "PWD: $(Get-Location)" -ForegroundColor DarkGray

# 1) Syntax/bytecode sanity
Run "python -m compileall -q src"

# 2) Install editable FIRST so src-layout imports work in tests
Run "python -m pip install -e ."
Run "python -c ""import yyfe_lab; import yyfe_lab.math_utils; print('IMPORT_OK')"""

# 3) Tests (now imports resolve)
Run "python -m pytest -q"

# 4) Build artifacts
Run "python -m build"

Write-Host "YY-FE QA: PASS" -ForegroundColor Green
