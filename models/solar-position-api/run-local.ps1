# Local setup and run for Solar Position API (Member 1 AI model)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path "venv")) {
    python -m venv venv
}

& ".\venv\Scripts\Activate.ps1"
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

if (-not (Test-Path "src\model\best_model.pkl")) {
    Write-Host "Training model (first run only — may take several minutes)..."
    python -m src.train
}

Write-Host "Starting API at http://localhost:8001"
Write-Host "  Health:   http://localhost:8001/health"
Write-Host "  Predict:  http://localhost:8001/predict"
Write-Host "  Docs:     http://localhost:8001/docs"
uvicorn app.main:app --reload --port 8001
