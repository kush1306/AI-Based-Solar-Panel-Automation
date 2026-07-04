# Run backend + frontend together (local development — no Docker required)
# Usage: .\run-local.ps1
#
# For the FULL stack (MySQL + both AI models in containers), install Docker Desktop
# and run: .\docker\compose-up.ps1

$Root = $PSScriptRoot
$Backend = Join-Path $Root "backend"
$Dashboard = Join-Path $Root "dashboard"

Write-Host "Starting backend on http://localhost:8000 ..."
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$Backend'; .\.venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
)

Write-Host "Starting frontend on http://localhost:8501 ..."
Set-Location $Dashboard
if (-not (Test-Path ".env.local")) {
    Copy-Item ".env.example" ".env.local"
    Write-Host "Created dashboard/.env.local from .env.example"
}
npm run dev
