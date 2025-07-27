# FinSight AI API Testing Guide for Postman

## Base URL
```
https://finsight-ai-agent-996911716674.us-central1.run.app
```

## Available Endpoints

### 1. Health Check (GET)
**URL:** `https://finsight-ai-agent-996911716674.us-central1.run.app/`
**Method:** GET
**Description:** Check if the service is running

**Expected Response:**
```json
{
  "status": "healthy",
  "agent": "delegator",
  "message": "FinSight AI Agent is running"
}
```

### 2. Agent Info (GET)
**URL:** `https://finsight-ai-agent-996911716674.us-central1.run.app/agent-info`
**Method:** GET
**Description:** Get information about the agent and its capabilities

**Expected Response:**
```json
{
  "name": "delegator",
  "description": "FinSight AI Financial Advisor - A comprehensive financial assistance agent",
  "model": "gemini-2.0-flash",
  "tools": 8
}
```

### 3. Chat with Agent (POST)
**URL:** `https://finsight-ai-agent-996911716674.us-central1.run.app/chat`
**Method:** POST
**Content-Type:** application/json

**Request Body:**
```json
{
  "message": "Hello, I need help with financial planning",
  "user_id": "test_user_123"
}
```

**Expected Response:**
```json
{
  "response": "Hello! Welcome to FinSight AI. I'm here to help you with comprehensive financial guidance...",
  "status": "success"
}
```

## Sample Test Cases for Postman

### Test Case 1: Basic Greeting
```json
{
  "message": "Hi, I'm new to financial planning. Can you help me?",
  "user_id": "user_001"
}
```

### Test Case 2: Loan Inquiry
```json
{
  "message": "I want to apply for a home loan. What should I know?",
  "user_id": "user_002"
}
```

### Test Case 3: Investment Advice
```json
{
  "message": "I have $10,000 to invest. What are my options?",
  "user_id": "user_003"
}
```

### Test Case 4: Tax Help
```json
{
  "message": "I need help with tax filing for this year",
  "user_id": "user_004"
}
```

### Test Case 5: Credit Score Improvement
```json
{
  "message": "My credit score is 650. How can I improve it?",
  "user_id": "user_005"
}
```

### Test Case 6: Budget Planning
```json
{
  "message": "I earn $5000 per month. Help me create a budget",
  "user_id": "user_006"
}
```

### Test Case 7: Government Schemes
```json
{
  "message": "What government financial schemes am I eligible for?",
  "user_id": "user_007"
}
```

### Test Case 8: Scam Detection
```json
{
  "message": "I received an email asking for my bank details for a lottery win. Is this legitimate?",
  "user_id": "user_008"
}
```

## Setting up Postman Collection

### Step 1: Create New Collection
1. Open Postman
2. Click "New" → "Collection"
3. Name it "FinSight AI Agent Tests"

### Step 2: Add Environment Variables
1. Click on "Environments" in Postman
2. Create new environment "FinSight AI"
3. Add variable:
   - **Variable:** `base_url`
   - **Value:** `https://finsight-ai-agent-996911716674.us-central1.run.app`

### Step 3: Create Requests

#### Request 1: Health Check
- **Name:** Health Check
- **Method:** GET
- **URL:** `{{base_url}}/`

#### Request 2: Agent Info
- **Name:** Agent Info
- **Method:** GET
- **URL:** `{{base_url}}/agent-info`

#### Request 3: Chat - Basic Greeting
- **Name:** Chat - Basic Greeting
- **Method:** POST
- **URL:** `{{base_url}}/chat`
- **Headers:** 
  - `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "message": "Hello, I need financial advice",
  "user_id": "postman_test_user"
}
```

## Expected Behaviors

### Financial Service Delegation
The agent should automatically delegate to appropriate sub-agents based on your request:

- **Loan questions** → Loan Helper agent
- **Investment queries** → Investment Guide agent  
- **Tax questions** → Tax Filing Helper agent
- **Credit score issues** → Credit Score Improver agent
- **Budget planning** → Budget Planner agent
- **Government schemes** → Government Scheme Suggester agent
- **Scam concerns** → Scam Detector agent

### Response Format
All chat responses should include:
- Professional, helpful tone
- Specific, actionable advice
- Clear explanations in simple language
- Appropriate delegation to specialized tools
- Follow-up suggestions when relevant

## Testing Checklist

- [ ] Health check endpoint returns 200 OK
- [ ] Agent info shows correct agent details
- [ ] Chat endpoint accepts POST requests
- [ ] Agent responds appropriately to different financial topics
- [ ] Response time is reasonable (< 30 seconds)
- [ ] Error handling works for invalid requests
- [ ] Agent maintains context within conversation

## Troubleshooting

### Common Issues:
1. **Timeout errors:** The agent might take up to 30 seconds to respond for complex queries
2. **500 errors:** Check the Cloud Run logs in Google Cloud Console
3. **Empty responses:** Ensure your request includes both "message" and "user_id" fields

### Monitoring:
- Check Cloud Run metrics at: https://console.cloud.google.com/run
- View logs for detailed error information
- Monitor response times and success rates
