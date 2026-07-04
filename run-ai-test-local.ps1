# One-click local test (NO Docker required)
# Starts Model 1, Model 2, Backend, and Dashboard in separate windows.
#
# Usage (from repo root):
#   .\run-ai-test-local.ps1
#
# Then open: http://localhost:8501/ai-predictions

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot

function Start-ServiceWindow {
    param(
        [string]$Title,
        [string]$WorkingDir,
        [string]$Command
    )
    Write-Host "Starting $Title ..."
    Start-Process powershell -ArgumentList @(
        "-NoExit",
        "-Command",
        "cd '$WorkingDir'; `$Host.UI.RawUI.WindowTitle = '$Title'; $Command"
    )
}

Write-Host ""
Write-Host "=== AI Integration Local Test Launcher ===" -ForegroundColor Cyan
Write-Host ""

# 1) Model 1 — Solar Position API
Start-ServiceWindow `
    -Title "Model 1 (port 8001)" `
    -WorkingDir (Join-Path $Root "models\solar-position-api") `
    -Command "python -m uvicorn app.main:app --host 127.0.0.1 --port 8001"

Start-Sleep -Seconds 3

# 2) Model 2 — Energy Optimization API
Start-ServiceWindow `
    -Title "Model 2 (port 8002)" `
    -WorkingDir (Join-Path $Root "Solar AI") `
    -Command "`$env:PYTHONUTF8='1'; python -m uvicorn src.api:app --host 127.0.0.1 --port 8002"

Write-Host "Waiting 45 seconds for Model 2 to train..." -ForegroundColor Yellow
Start-Sleep -Seconds 45

# 3) Backend — points to local models (not Docker hostnames)
$backendCmd = @"
`$env:MODEL1_SERVICE_URL='http://127.0.0.1:8001'
`$env:ENERGY_OPTIMIZATION_SERVICE_URL='http://127.0.0.1:8002'
`$env:MODEL_SERVICE_TIMEOUT='120'
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
"@

Start-ServiceWindow `
    -Title "Backend (port 8000)" `
    -WorkingDir (Join-Path $Root "backend") `
    -Command $backendCmd

Start-Sleep -Seconds 5

# 4) Dashboard
$dashboardDir = Join-Path $Root "dashboard"
if (-not (Test-Path (Join-Path $dashboardDir ".env.local"))) {
    Copy-Item (Join-Path $dashboardDir ".env.example") (Join-Path $dashboardDir ".env.local")
}

Write-Host ""
Write-Host "Starting dashboard on http://localhost:8501 ..." -ForegroundColor Green
Write-Host ""
Write-Host "When the dashboard opens, go to:" -ForegroundColor Yellow
Write-Host "  http://localhost:8501/ai-predictions" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press F12 -> Network tab and confirm calls to /api/ai/energy/*" -ForegroundColor Yellow
Write-Host ""

Set-Location $dashboardDir
npm run dev
