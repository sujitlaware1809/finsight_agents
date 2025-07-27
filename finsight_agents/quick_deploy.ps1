# Quick Deploy FinSight AI to Google Cloud
# PowerShell script for fast deployment

$PROJECT_ID = "driven-edition-467110-p6"
$REGION = "us-central1"
$BUCKET_NAME = "$PROJECT_ID-finsight-bucket"

Write-Host "🚀 Quick Deploy FinSight AI to Google Cloud" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Update .env for cloud deployment
Write-Host "📝 Updating environment configuration..." -ForegroundColor Yellow
$envContent = @"
GOOGLE_API_KEY=AIzaSyDJI7lYSEAcEe8qorR45wyu2fGQpOgI7Lk
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=$PROJECT_ID
GOOGLE_CLOUD_LOCATION=$REGION
GOOGLE_CLOUD_STORAGE_BUCKET=$BUCKET_NAME
"@

$envContent | Out-File -FilePath "delegator\.env" -Encoding UTF8
Write-Host "✅ Environment updated" -ForegroundColor Green

# Enable required APIs
Write-Host "🔌 Enabling required APIs..." -ForegroundColor Yellow
gcloud services enable aiplatform.googleapis.com --project=$PROJECT_ID
gcloud services enable cloudfunctions.googleapis.com --project=$PROJECT_ID
gcloud services enable run.googleapis.com --project=$PROJECT_ID
gcloud services enable storage.googleapis.com --project=$PROJECT_ID

# Create bucket
Write-Host "🪣 Creating storage bucket..." -ForegroundColor Yellow
gsutil mb -p $PROJECT_ID -l $REGION gs://$BUCKET_NAME 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Bucket created" -ForegroundColor Green
} else {
    Write-Host "ℹ️ Bucket already exists or creation failed" -ForegroundColor Yellow
}

# Deploy to Cloud Run (simplest option)
Write-Host "🚢 Deploying to Cloud Run..." -ForegroundColor Yellow

# Create a simple Dockerfile for deployment
$dockerfileContent = @"
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV GOOGLE_GENAI_USE_VERTEXAI=TRUE
ENV GOOGLE_CLOUD_PROJECT=$PROJECT_ID
ENV GOOGLE_CLOUD_LOCATION=$REGION
ENV PORT=8080

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
"@

$dockerfileContent | Out-File -FilePath "Dockerfile" -Encoding UTF8

# Create a simple FastAPI wrapper for the agent
$appContent = @"
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FinSight AI Agent", version="1.0.0")

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

# Load agent
try:
    from delegator.agent import root_agent
    logger.info(f"Agent {root_agent.name} loaded successfully")
except Exception as e:
    logger.error(f"Failed to load agent: {e}")
    root_agent = None

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "agent": root_agent.name if root_agent else "not loaded",
        "message": "FinSight AI Agent is running"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not root_agent:
        raise HTTPException(status_code=500, detail="Agent not loaded")
    
    try:
        # Process the message through the agent
        response = root_agent.run(request.message)
        return ChatResponse(response=str(response))
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/agent-info")
def agent_info():
    if not root_agent:
        return {"error": "Agent not loaded"}
    
    return {
        "name": root_agent.name,
        "description": root_agent.description,
        "model": root_agent.model if hasattr(root_agent, 'model') else "unknown",
        "tools": len(root_agent.tools) if hasattr(root_agent, 'tools') else 0
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
"@

$appContent | Out-File -FilePath "app.py" -Encoding UTF8

# Update requirements for FastAPI
$newRequirements = @"
google-adk[database]==0.3.0
google-cloud-aiplatform[agent-engines]>=1.91.0
google-genai>=1.5.0,<2.0.0
yfinance==0.2.56
psutil==5.9.5
litellm==1.66.3
google-generativeai==0.8.5
python-dotenv==1.1.0
pydantic>=2.10.6,<3.0.0
absl-py>=2.2.1,<3.0.0
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
"@

$newRequirements | Out-File -FilePath "requirements.txt" -Encoding UTF8

# Deploy to Cloud Run
gcloud run deploy finsight-ai-agent `
    --source . `
    --region $REGION `
    --allow-unauthenticated `
    --memory 2Gi `
    --cpu 1 `
    --timeout 300 `
    --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION,GOOGLE_CLOUD_STORAGE_BUCKET=$BUCKET_NAME" `
    --project $PROJECT_ID

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Deployment successful!" -ForegroundColor Green
    $serviceUrl = gcloud run services describe finsight-ai-agent --region $REGION --format="value(status.url)" --project $PROJECT_ID
    Write-Host "🌐 Service URL: $serviceUrl" -ForegroundColor Cyan
    Write-Host "🧪 Test endpoints:" -ForegroundColor Yellow
    Write-Host "   Health: $serviceUrl/" -ForegroundColor White
    Write-Host "   Chat: $serviceUrl/chat (POST)" -ForegroundColor White
    Write-Host "   Agent Info: $serviceUrl/agent-info" -ForegroundColor White
} else {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
}

Write-Host "🏁 Deployment script finished!" -ForegroundColor Cyan
