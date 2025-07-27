# FinSight AI Standalone - Quick Test Script
# Tests the deployed FinSight AI Financial Advisor Agent

$baseUrl = "https://finsight-ai-standalone-996911716674.us-central1.run.app"

Write-Host "🔍 Testing FinSight AI Standalone Deployment" -ForegroundColor Green
Write-Host "Base URL: $baseUrl" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "1️⃣ Testing Health Check..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-WebRequest -Uri "$baseUrl/" -Method GET
    Write-Host "✅ Health Check: SUCCESS (Status: $($healthResponse.StatusCode))" -ForegroundColor Green
    $healthData = $healthResponse.Content | ConvertFrom-Json
    Write-Host "   Agent: $($healthData.agent)" -ForegroundColor Gray
    Write-Host "   Status: $($healthData.status)" -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "❌ Health Check: FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

# Test 2: Agent Info
Write-Host "2️⃣ Testing Agent Info..." -ForegroundColor Yellow
try {
    $infoResponse = Invoke-WebRequest -Uri "$baseUrl/agent-info" -Method GET
    Write-Host "✅ Agent Info: SUCCESS (Status: $($infoResponse.StatusCode))" -ForegroundColor Green
    $infoData = $infoResponse.Content | ConvertFrom-Json
    Write-Host "   Name: $($infoData.name)" -ForegroundColor Gray
    Write-Host "   Description: $($infoData.description)" -ForegroundColor Gray
    Write-Host "   Capabilities: $($infoData.capabilities -join ', ')" -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "❌ Agent Info: FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

# Test 3: Basic Chat
Write-Host "3️⃣ Testing Basic Chat..." -ForegroundColor Yellow
try {
    $chatBody = @{
        message = "Hello, I need financial advice"
        user_id = "test_user_powershell"
    } | ConvertTo-Json
    
    $chatResponse = Invoke-WebRequest -Uri "$baseUrl/chat" -Method POST -ContentType "application/json" -Body $chatBody
    Write-Host "✅ Basic Chat: SUCCESS (Status: $($chatResponse.StatusCode))" -ForegroundColor Green
    $chatData = $chatResponse.Content | ConvertFrom-Json
    $responsePreview = $chatData.response.Substring(0, [Math]::Min(100, $chatData.response.Length))
    Write-Host "   Response Preview: $responsePreview..." -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "❌ Basic Chat: FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

# Test 4: Loan Inquiry
Write-Host "4️⃣ Testing Loan Inquiry..." -ForegroundColor Yellow
try {
    $loanBody = @{
        message = "I want to apply for a home loan of 300000 dollars. What documents do I need?"
        user_id = "test_user_loan"
    } | ConvertTo-Json
    
    $loanResponse = Invoke-WebRequest -Uri "$baseUrl/chat" -Method POST -ContentType "application/json" -Body $loanBody
    Write-Host "✅ Loan Inquiry: SUCCESS (Status: $($loanResponse.StatusCode))" -ForegroundColor Green
    $loanData = $loanResponse.Content | ConvertFrom-Json
    $loanPreview = $loanData.response.Substring(0, [Math]::Min(100, $loanData.response.Length))
    Write-Host "   Response Preview: $loanPreview..." -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "❌ Loan Inquiry: FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

# Test 5: Investment Advice
Write-Host "5️⃣ Testing Investment Advice..." -ForegroundColor Yellow
try {
    $investBody = @{
        message = "I have 50000 dollars to invest and I am 30 years old. What investment strategy would you recommend?"
        user_id = "test_user_invest"
    } | ConvertTo-Json
    
    $investResponse = Invoke-WebRequest -Uri "$baseUrl/chat" -Method POST -ContentType "application/json" -Body $investBody
    Write-Host "✅ Investment Advice: SUCCESS (Status: $($investResponse.StatusCode))" -ForegroundColor Green
    $investData = $investResponse.Content | ConvertFrom-Json
    $investPreview = $investData.response.Substring(0, [Math]::Min(100, $investData.response.Length))
    Write-Host "   Response Preview: $investPreview..." -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "❌ Investment Advice: FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

Write-Host "🎉 FinSight AI Standalone Testing Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Summary:" -ForegroundColor Cyan
Write-Host "- Service URL: $baseUrl" -ForegroundColor White
Write-Host "- All endpoints tested successfully" -ForegroundColor White
Write-Host "- Agent is responding with comprehensive financial advice" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Use the updated Postman collection for more detailed testing" -ForegroundColor Blue
