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

RunPy @("-m","compileall","-q","src")
RunPy @("-m","pip","install","-e",".")
RunPy @("-c","import yyfe_lab; import yyfe_lab.math_utils; print('IMPORT_OK')")
RunPy @("-m","pytest","-q")
RunPy @("-m","build")

Write-Host "YY-FE QA: PASS" -ForegroundColor Green