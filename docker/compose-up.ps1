# Start the full stack with Docker Compose.
#
# Usage:
#   From repo root:  .\docker\compose-up.ps1
#   From docker dir: .\compose-up.ps1
#
# Or directly:
#   cd docker
#   docker compose up --build

$ErrorActionPreference = "Stop"
$DockerDir = $PSScriptRoot
$RepoRoot = Split-Path $DockerDir -Parent

function Test-DockerAvailable {
    $docker = Get-Command docker -ErrorAction SilentlyContinue
    if ($docker) { return $true }

    $defaultPath = "C:\Program Files\Docker\Docker\resources\bin\docker.exe"
    return Test-Path $defaultPath
}

if (-not (Test-DockerAvailable)) {
    Write-Host ""
    Write-Host "Docker is not installed or not on your PATH." -ForegroundColor Red
    Write-Host ""
    Write-Host "The command 'docker compose up --build' requires Docker Desktop for Windows."
    Write-Host ""
    Write-Host "Option A - Install Docker (full stack with AI models):" -ForegroundColor Yellow
    Write-Host "  1. Download Docker Desktop: https://www.docker.com/products/docker-desktop/"
    Write-Host "  2. Install and restart your PC if prompted"
    Write-Host "  3. Start Docker Desktop and wait until it shows 'Running'"
    Write-Host "  4. Open a NEW PowerShell window, then run:"
    Write-Host "       cd `"$DockerDir`""
    Write-Host "       docker compose up --build"
    Write-Host ""
    Write-Host "Option B - Run without Docker (backend + frontend only):" -ForegroundColor Yellow
    Write-Host "  From repo root:"
    Write-Host "       .\run-local.ps1"
    Write-Host ""
    Write-Host "  Requires: Python venv in backend/, Node.js, and MySQL running locally."
    Write-Host "  AI models (Model 1 / Model 2) need Docker OR separate local model servers."
    Write-Host ""
    exit 1
}

Set-Location $DockerDir
Write-Host "Starting Docker Compose from $DockerDir ..."
Write-Host ""
Write-Host "Prerequisites:" -ForegroundColor Yellow
Write-Host "  - Docker Desktop running (WSL 2 backend enabled)"
Write-Host "  - If Docker was just installed, reboot Windows once after WSL setup"
Write-Host "  - Complete Ubuntu first-run setup if prompted (wsl -d Ubuntu)"
Write-Host ""
docker compose up --build
