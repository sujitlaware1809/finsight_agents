# FinSight AI Local Server Startup Script
# Run this script to start your local development server

Write-Host "🚀 FinSight AI Local Development Server" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ first." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install -r local_requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🌟 Starting FinSight AI Local Server..." -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Server will be available at: http://localhost:8000" -ForegroundColor White
Write-Host "📋 API Endpoints:" -ForegroundColor White
Write-Host "   - GET  http://localhost:8000/           - Health check" -ForegroundColor Gray
Write-Host "   - GET  http://localhost:8000/agent-info - Agent information" -ForegroundColor Gray
Write-Host "   - POST http://localhost:8000/chat       - Chat with agent" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Frontend Integration:" -ForegroundColor Yellow
Write-Host "   Use 'http://localhost:8000' as your API base URL" -ForegroundColor Gray
Write-Host ""
Write-Host "🛑 Press Ctrl+C to stop the server" -ForegroundColor Red
Write-Host ""

# Start the server
python local_server.py
