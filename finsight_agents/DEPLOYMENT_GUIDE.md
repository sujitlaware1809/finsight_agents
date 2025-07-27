# FinSight AI - Google Cloud Deployment Guide

## Prerequisites

Before deploying, ensure you have:

1. **Google Cloud Project** with the following APIs enabled:
   - Vertex AI API
   - Cloud Storage API
   - Cloud Functions API (if using serverless deployment)
   - Agent Engines API

2. **Google Cloud CLI** installed and authenticated:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Required Python packages** installed (see requirements.txt)

## Environment Configuration

Update your `.env` file with your Google Cloud project details:

```
GOOGLE_API_KEY=your_gemini_api_key
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name
```

## Deployment Options

### Option 1: Vertex AI Agent Engines (Recommended)

This deploys your agent directly to Vertex AI Agent Engines for production use:

```powershell
# Navigate to the FinsightAI directory
cd "c:\Users\hp\Downloads\finsight_upload\FinsightAI"

# Install dependencies
pip install -r requirements.txt

# Deploy to Vertex AI Agent Engines
python deployment/deploy.py --create --project_id=YOUR_PROJECT_ID --location=us-central1 --bucket=YOUR_BUCKET_NAME
```

### Option 2: Cloud Functions (Serverless)

Deploy as a Cloud Function for serverless execution:

```powershell
# Navigate to the FinsightAI directory
cd "c:\Users\hp\Downloads\finsight_upload\FinsightAI"

# Deploy as Cloud Function
gcloud functions deploy finsight-ai-agent `
    --gen2 `
    --runtime python312 `
    --source . `
    --entry-point main `
    --trigger-http `
    --allow-unauthenticated `
    --region us-central1 `
    --memory 2Gi `
    --timeout 300s `
    --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID"
```

### Option 3: Cloud Run (Containerized)

Deploy as a containerized service on Cloud Run:

```powershell
# Build and deploy to Cloud Run
gcloud run deploy finsight-ai-agent `
    --source . `
    --region us-central1 `
    --allow-unauthenticated `
    --memory 2Gi `
    --cpu 1 `
    --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID"
```

## Step-by-Step Deployment

### Step 1: Prepare Your Environment

1. Update your Google Cloud project ID in the `.env` file
2. Create a Cloud Storage bucket for staging:
   ```powershell
   gsutil mb gs://your-bucket-name
   ```

### Step 2: Enable Required APIs

```powershell
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable storage.googleapis.com
```

### Step 3: Deploy (Choose one option above)

### Step 4: Test Your Deployment

After deployment, test your agent:

```powershell
# For Agent Engines deployment
python deployment/test_deployment.py

# For Cloud Functions/Cloud Run
# Use the provided endpoint URL to make HTTP requests
```

## Monitoring and Management

- **Vertex AI Console**: Monitor agent performance and logs
- **Cloud Functions Console**: View function metrics and logs
- **Cloud Run Console**: Monitor service health and scaling

## Troubleshooting

Common issues and solutions:

1. **Authentication Error**: Ensure your service account has the necessary permissions
2. **API Not Enabled**: Enable required APIs in Google Cloud Console
3. **Quota Exceeded**: Check your project quotas and request increases if needed
4. **Environment Variables**: Verify all required environment variables are set correctly

## Security Considerations

- Use IAM roles and service accounts with minimal required permissions
- Store sensitive data in Secret Manager instead of environment variables
- Enable audit logging for production deployments
- Regularly rotate API keys and credentials

## Costs

- **Vertex AI Agent Engines**: Pay-per-request pricing
- **Cloud Functions**: Pay-per-invocation and compute time
- **Cloud Run**: Pay-per-request and allocated CPU/memory

Choose the deployment option that best fits your usage patterns and budget requirements.
