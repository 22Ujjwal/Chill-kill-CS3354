# backend-run.ps1
# Quick start script for Nintendo RAG Chatbot Backend
# Usage: .\backend-run.ps1

$ErrorActionPreference = "Stop"

$SCRIPT_DIR = $PSScriptRoot
$BACKEND_DIR = Join-Path $SCRIPT_DIR "backend"
$VENV_PATH = Join-Path $SCRIPT_DIR ".venv"

Write-Host "[*] Starting Nintendo Chatbot Backend..." -ForegroundColor Green
Write-Host ""

# Check if venv exists
if (-not (Test-Path (Join-Path $VENV_PATH "Scripts\python.exe"))) {
    Write-Host "[ERROR] Virtual environment not found at $VENV_PATH" -ForegroundColor Red
    Write-Host "Please set up the venv first with: python -m venv .venv."
    Write-Host "Then run: .\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt"
    exit 1
}

# Check if backend directory exists
if (-not (Test-Path $BACKEND_DIR)) {
    Write-Host "[ERROR] Backend directory not found at $BACKEND_DIR" -ForegroundColor Red
    exit 1
}

# Check if .env exists
$envPath = Join-Path $BACKEND_DIR ".env"
if (-not (Test-Path $envPath)) {
    Write-Host "[ERROR] .env file not found at $envPath" -ForegroundColor Red
    Write-Host "Please create it with your API keys"
    exit 1
}

# Start the backend in background
Set-Location $BACKEND_DIR
Write-Host "Starting Flask server on port 5002..." -ForegroundColor Cyan

$env:PORT = "5002"
$pythonExe = Join-Path $VENV_PATH "Scripts\python.exe"

# Start in background job
$job = Start-Job -ScriptBlock {
    param($pythonPath, $backendDir)
    Set-Location $backendDir
    $env:PORT = "5002"
    & $pythonPath app.py
} -ArgumentList $pythonExe, $BACKEND_DIR

Write-Host "[OK] Backend started (Job ID: $($job.Id))" -ForegroundColor Green
Write-Host ""

# Wait for server to be ready
Write-Host "[*] Waiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "[OK] Server started successfully" -ForegroundColor Green
Write-Host ""

# Initialize the chatbot
Write-Host ""
Write-Host "[*] Initializing chatbot..." -ForegroundColor Cyan

try {
    $initResponse = Invoke-RestMethod -Uri "http://127.0.0.1:5002/api/initialize" `
        -Method Post `
        -ContentType "application/json" `
        -Body '{"rebuild":true}' `
        -TimeoutSec 300 `
        -ErrorAction SilentlyContinue

    if ($initResponse.status -eq "initialized" -or $initResponse.status -eq "already_initialized") {
        Write-Host "[OK] Chatbot is ready" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] Initialization response: $($initResponse | ConvertTo-Json -Compress)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[WARNING] Could not initialize chatbot: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[*] Nintendo Chatbot is now running!" -ForegroundColor Green
Write-Host ""
Write-Host "[*] Server: http://127.0.0.1:5002" -ForegroundColor Cyan
Write-Host "[*] Query endpoint: http://127.0.0.1:5002/api/query" -ForegroundColor Cyan
Write-Host "[*] Stats endpoint: http://127.0.0.1:5002/api/stats" -ForegroundColor Cyan
Write-Host "[*] Health endpoint: http://127.0.0.1:5002/api/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "Example query:" -ForegroundColor Yellow
Write-Host '  Invoke-RestMethod -Uri "http://127.0.0.1:5002/api/query" `' -ForegroundColor Gray
Write-Host '    -Method Post `' -ForegroundColor Gray
Write-Host '    -ContentType "application/json" `' -ForegroundColor Gray
Write-Host '    -Body ''{"query":"Tell me about Nintendo","top_k":5}''' -ForegroundColor Gray
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "To view job output: Receive-Job $($job.Id)" -ForegroundColor Gray
Write-Host ""

# Keep script running until interrupted
try {
    while ($true) {
        $jobState = (Get-Job -Id $job.Id).State
        if ($jobState -eq "Failed" -or $jobState -eq "Stopped") {
            Write-Host "[ERROR] Backend job stopped unexpectedly" -ForegroundColor Red
            Receive-Job -Job $job
            break
        }
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host ""
    Write-Host "Stopping backend..." -ForegroundColor Yellow
    Stop-Job -Job $job -ErrorAction SilentlyContinue
    Remove-Job -Job $job -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] Backend stopped" -ForegroundColor Green
}
