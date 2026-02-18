$ErrorActionPreference = "Stop"

function RunPy([string[]]$argv) {
  Write-Host ("Running: python " + ($argv -join " ")) -ForegroundColor Cyan
  & python @argv
  if ($LASTEXITCODE -ne 0) {
    throw ("Command failed (exit=" + $LASTEXITCODE + "): python " + ($argv -join " "))
  }
}

Write-Host ""
Write-Host "YY-FE QA: start" -ForegroundColor Green
Write-Host ("PWD: " + (Get-Location)) -ForegroundColor DarkGray

# 1) Syntax/bytecode sanity
RunPy @("-m","compileall","-q","src")

# 2) Install editable FIRST (src-layout)
RunPy @("-m","pip","install","-e",".")

# 3) Import smoke
RunPy @("-c","import yyfe_lab; import yyfe_lab.math_utils; print('IMPORT_OK')")

# 4) Lint + format gates (ruff)
RunPy @("-m","ruff","check",".")
RunPy @("-m","ruff","format","--check",".")

# 5) Type gate (mypy)
RunPy @("-m","mypy","src")

# 6) Tests
RunPy @("-m","pytest","-q")

# 7) Build artifacts
RunPy @("-m","build")

Write-Host "YY-FE QA: PASS" -ForegroundColor Green