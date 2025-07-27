# Simple Deploy Script for FinSight AI
$PROJECT_ID = "driven-edition-467110-p6"
$REGION = "us-central1"
$BUCKET_NAME = "$PROJECT_ID-finsight-bucket"

Write-Host "Deploying FinSight AI to Google Cloud Run" -ForegroundColor Cyan

# Update delegator .env file
$envContent = @"
GOOGLE_API_KEY=AIzaSyDJI7lYSEAcEe8qorR45wyu2fGQpOgI7Lk
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=$PROJECT_ID
GOOGLE_CLOUD_LOCATION=$REGION
GOOGLE_CLOUD_STORAGE_BUCKET=$BUCKET_NAME
"@

$envContent | Out-File -FilePath "delegator\.env" -Encoding UTF8
Write-Host "Environment configuration updated" -ForegroundColor Green

# Enable APIs
Write-Host "Enabling APIs..." -ForegroundColor Yellow
gcloud services enable run.googleapis.com --project=$PROJECT_ID
gcloud services enable cloudbuild.googleapis.com --project=$PROJECT_ID

# Deploy to Cloud Run
Write-Host "Deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy finsight-ai-agent --source . --region $REGION --allow-unauthenticated --memory 2Gi --cpu 1 --timeout 300 --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION" --project $PROJECT_ID

if ($LASTEXITCODE -eq 0) {
    Write-Host "Deployment successful!" -ForegroundColor Green
    $serviceUrl = gcloud run services describe finsight-ai-agent --region $REGION --format="value(status.url)" --project $PROJECT_ID
    Write-Host "Service URL: $serviceUrl" -ForegroundColor Cyan
    Write-Host "Test your agent at: $serviceUrl" -ForegroundColor Yellow
} else {
    Write-Host "Deployment failed!" -ForegroundColor Red
}
