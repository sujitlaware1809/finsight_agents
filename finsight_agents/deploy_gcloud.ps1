# FinSight AI - Google Cloud Deployment Script
# PowerShell script for deploying FinSight AI to Google Cloud

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-central1",
    
    [Parameter(Mandatory=$false)]
    [string]$BucketName = "",
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("agent-engines", "cloud-functions", "cloud-run")]
    [string]$DeploymentType = "agent-engines"
)

# Colors for output
$ErrorColor = "Red"
$SuccessColor = "Green"
$InfoColor = "Cyan"
$WarningColor = "Yellow"

Write-Host "🚀 FinSight AI Deployment Script" -ForegroundColor $InfoColor
Write-Host "=================================" -ForegroundColor $InfoColor
Write-Host "Project ID: $ProjectId" -ForegroundColor $InfoColor
Write-Host "Region: $Region" -ForegroundColor $InfoColor
Write-Host "Deployment Type: $DeploymentType" -ForegroundColor $InfoColor

# Set default bucket name if not provided
if ([string]::IsNullOrEmpty($BucketName)) {
    $BucketName = "$ProjectId-finsight-ai-bucket"
}
Write-Host "Bucket Name: $BucketName" -ForegroundColor $InfoColor

# Function to check if command exists
function Test-Command {
    param($Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

# Check prerequisites
Write-Host "`n📋 Checking prerequisites..." -ForegroundColor $WarningColor

if (!(Test-Command "gcloud")) {
    Write-Host "❌ Google Cloud CLI not found. Please install it first." -ForegroundColor $ErrorColor
    exit 1
}

if (!(Test-Command "python")) {
    Write-Host "❌ Python not found. Please install Python 3.9+ first." -ForegroundColor $ErrorColor
    exit 1
}

Write-Host "✅ Prerequisites check passed" -ForegroundColor $SuccessColor

# Set Google Cloud project
Write-Host "`n🔧 Configuring Google Cloud..." -ForegroundColor $WarningColor
gcloud config set project $ProjectId
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to set project. Please check your project ID." -ForegroundColor $ErrorColor
    exit 1
}

# Enable required APIs
Write-Host "`n🔌 Enabling required APIs..." -ForegroundColor $WarningColor
$apis = @(
    "aiplatform.googleapis.com",
    "storage.googleapis.com"
)

if ($DeploymentType -eq "cloud-functions") {
    $apis += "cloudfunctions.googleapis.com"
}

if ($DeploymentType -eq "cloud-run") {
    $apis += "run.googleapis.com"
}

foreach ($api in $apis) {
    Write-Host "Enabling $api..." -ForegroundColor $InfoColor
    gcloud services enable $api
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to enable $api" -ForegroundColor $ErrorColor
        exit 1
    }
}

Write-Host "✅ APIs enabled successfully" -ForegroundColor $SuccessColor

# Create Cloud Storage bucket if it doesn't exist
Write-Host "`n🪣 Setting up Cloud Storage bucket..." -ForegroundColor $WarningColor
$bucketExists = gsutil ls -b gs://$BucketName 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating bucket gs://$BucketName..." -ForegroundColor $InfoColor
    gsutil mb -p $ProjectId -l $Region gs://$BucketName
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Bucket created successfully!" -ForegroundColor $SuccessColor
    } else {
        Write-Host "❌ Failed to create bucket!" -ForegroundColor $ErrorColor
        exit 1
    }
} else {
    Write-Host "✅ Bucket already exists" -ForegroundColor $SuccessColor
}

# Update .env file
Write-Host "`n📝 Updating environment configuration..." -ForegroundColor $WarningColor
$envContent = @"
GOOGLE_API_KEY=AIzaSyDJI7lYSEAcEe8qorR45wyu2fGQpOgI7Lk
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=$ProjectId
GOOGLE_CLOUD_LOCATION=$Region
GOOGLE_CLOUD_STORAGE_BUCKET=$BucketName
"@

$envContent | Out-File -FilePath ".env" -Encoding UTF8
Write-Host "✅ Environment configuration updated" -ForegroundColor $SuccessColor

# Install Python dependencies
Write-Host "`n📦 Installing Python dependencies..." -ForegroundColor $WarningColor
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor $ErrorColor
    exit 1
}

# Install poetry dependencies if pyproject.toml exists
if (Test-Path "pyproject.toml") {
    if (Test-Command "poetry") {
        Write-Host "Installing poetry dependencies..." -ForegroundColor $InfoColor
        poetry install --with deployment
    } else {
        Write-Host "Poetry not found, using pip for additional dependencies..." -ForegroundColor $WarningColor
        pip install google-cloud-aiplatform[agent-engines] absl-py
    }
}

Write-Host "✅ Dependencies installed successfully" -ForegroundColor $SuccessColor

# Deploy based on selected type
Write-Host "`n🚢 Starting deployment..." -ForegroundColor $WarningColor

switch ($DeploymentType) {
    "agent-engines" {
        Write-Host "Deploying to Vertex AI Agent Engines..." -ForegroundColor $InfoColor
        python deployment/deploy.py --create --project_id=$ProjectId --location=$Region --bucket=$BucketName
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Agent Engines deployment successful!" -ForegroundColor $SuccessColor
        } else {
            Write-Host "❌ Agent Engines deployment failed!" -ForegroundColor $ErrorColor
            exit 1
        }
    }
    
    "cloud-functions" {
        Write-Host "Deploying to Cloud Functions..." -ForegroundColor $InfoColor
        gcloud functions deploy finsight-ai-agent `
            --gen2 `
            --runtime python312 `
            --source . `
            --entry-point main `
            --trigger-http `
            --allow-unauthenticated `
            --region $Region `
            --memory 2Gi `
            --timeout 300s `
            --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_PROJECT=$ProjectId,GOOGLE_CLOUD_LOCATION=$Region,GOOGLE_CLOUD_STORAGE_BUCKET=$BucketName"
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Cloud Functions deployment successful!" -ForegroundColor $SuccessColor
            $functionUrl = gcloud functions describe finsight-ai-agent --region $Region --format="value(serviceConfig.uri)"
            Write-Host "🌐 Function URL: $functionUrl" -ForegroundColor $InfoColor
        } else {
            Write-Host "❌ Cloud Functions deployment failed!" -ForegroundColor $ErrorColor
            exit 1
        }
    }
    
    "cloud-run" {
        Write-Host "Deploying to Cloud Run..." -ForegroundColor $InfoColor
        gcloud run deploy finsight-ai-agent `
            --source . `
            --region $Region `
            --allow-unauthenticated `
            --memory 2Gi `
            --cpu 1 `
            --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_PROJECT=$ProjectId,GOOGLE_CLOUD_LOCATION=$Region,GOOGLE_CLOUD_STORAGE_BUCKET=$BucketName"
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Cloud Run deployment successful!" -ForegroundColor $SuccessColor
            $serviceUrl = gcloud run services describe finsight-ai-agent --region $Region --format="value(status.url)"
            Write-Host "🌐 Service URL: $serviceUrl" -ForegroundColor $InfoColor
        } else {
            Write-Host "❌ Cloud Run deployment failed!" -ForegroundColor $ErrorColor
            exit 1
        }
    }
}

Write-Host "`n🎉 Deployment completed successfully!" -ForegroundColor $SuccessColor
Write-Host "📊 You can monitor your deployment in the Google Cloud Console:" -ForegroundColor $InfoColor
Write-Host "   https://console.cloud.google.com/ai-platform/agents?project=$ProjectId" -ForegroundColor $InfoColor

# Optional: Run tests
$runTests = Read-Host "`nWould you like to run deployment tests? (y/N)"
if ($runTests -eq "y" -or $runTests -eq "Y") {
    if (Test-Path "deployment/test_deployment.py") {
        Write-Host "`n🧪 Running deployment tests..." -ForegroundColor $WarningColor
        python deployment/test_deployment.py
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ All tests passed!" -ForegroundColor $SuccessColor
        } else {
            Write-Host "⚠️ Some tests failed. Check the output above." -ForegroundColor $WarningColor
        }
    } else {
        Write-Host "⚠️ Test file not found. Skipping tests." -ForegroundColor $WarningColor
    }
}

Write-Host "`n🏁 Deployment script finished!" -ForegroundColor $SuccessColor
