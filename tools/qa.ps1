param(
  [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

Write-Host "YY-FE QA: start" -ForegroundColor Cyan
Write-Host "PWD: $PWD" -ForegroundColor DarkGray

function Run([string[]]$cmd) {
  $line = ($cmd -join " ")
  Write-Host "Running: $line" -ForegroundColor Yellow
  & $cmd[0] $cmd[1..($cmd.Length-1)]
  if ($LASTEXITCODE -ne 0) {
    throw "Command failed (exit=$LASTEXITCODE): $line"
  }
}

# 1) Syntax sanity
Run @($Python, "-m", "compileall", "-q", "src")

# 2) Tests
Run @($Python, "-m", "pytest", "-q")

# 3) Editable install (best-effort, but we treat failure as real failure to surface env issues)
Run @($Python, "-m", "pip", "install", "-e", ".")

# 4) Build (sdist+wheel)
Run @($Python, "-m", "build")

Write-Host "YY-FE QA: PASS" -ForegroundColor Green