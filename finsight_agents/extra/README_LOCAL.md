# FinSight AI Local Development Server

A local API server for FinSight AI financial advisor that you can run on your machine and integrate with your frontend.

## 🚀 Quick Start

### 1. Start the Local Server

**Option A: Using PowerShell Script (Recommended)**
```powershell
.\start_local_server.ps1
```

**Option B: Manual Start**
```bash
# Install dependencies
pip install -r local_requirements.txt

# Start server
python local_server.py
```

### 2. Access the Server

- **Server URL:** `http://localhost:8000`
- **Test Interface:** Open `test_local_api.html` in your browser
- **API Documentation:** `http://localhost:8000/docs` (FastAPI auto-generated)

## 📋 API Endpoints

### GET `/` - Health Check
```bash
curl http://localhost:8000/
```
**Response:**
```json
{
    "status": "healthy",
    "agent": "finsight-ai-local",
    "message": "FinSight AI Local Server is running!",
    "server_url": "http://localhost:8000"
}
```

### GET `/agent-info` - Agent Information
```bash
curl http://localhost:8000/agent-info
```
**Response:**
```json
{
    "name": "finsight-ai-local",
    "description": "FinSight AI Financial Advisor - Local Development Server",
    "status": "active",
    "server_type": "local_development",
    "capabilities": [
        "Loan Guidance with EMI calculations",
        "Investment Planning with age-based strategies",
        "Tax Assistance",
        "Credit Score Improvement with timelines",
        "Budget Planning with income analysis",
        "Scam Detection",
        "Government Schemes",
        "Credit Card Advice"
    ]
}
```

### POST `/chat` - Chat with Agent
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need a home loan for $300,000",
    "user_id": "user123"
  }'
```
**Response:**
```json
{
    "response": "🏠 FinSight AI - Home Loan Advisory 🏠\n\n...",
    "status": "success"
}
```

## 💻 Frontend Integration

### JavaScript/React Example
```javascript
const API_BASE = 'http://localhost:8000';

// Chat with the agent
async function chatWithAgent(message, userId = 'default') {
    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                user_id: userId
            })
        });
        
        const data = await response.json();
        return data.response;
    } catch (error) {
        console.error('Error:', error);
        return 'Sorry, I encountered an error. Please try again.';
    }
}

// Example usage
chatWithAgent("I need help with investment planning")
    .then(response => console.log(response));
```

### Python Example
```python
import requests

API_BASE = "http://localhost:8000"

def chat_with_agent(message, user_id="default"):
    try:
        response = requests.post(f"{API_BASE}/chat", json={
            "message": message,
            "user_id": user_id
        })
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error: {e}"

# Example usage
response = chat_with_agent("How to improve my credit score of 620?")
print(response)
```

## 🧪 Test Queries

Try these example queries to test different capabilities:

### Loan Queries
- `"I need a home loan for $300,000"`
- `"Personal loan of $50,000 for 5 years"`
- `"Education loan for medical school"`

### Investment Queries
- `"How to invest $50,000 at age 30?"`
- `"Best mutual funds for long-term wealth building"`
- `"SIP strategy for retirement planning"`

### Credit Score Queries
- `"My credit score is 620, how to improve?"`
- `"Steps to reach 750+ credit score"`
- `"Credit report analysis and improvement"`

### Budget Planning
- `"Create budget for $6000 monthly income"`
- `"Saving strategies for young professionals"`
- `"Emergency fund planning"`

### Credit Cards
- `"Best credit card for beginners"`
- `"Cashback vs rewards credit cards"`
- `"How to use credit cards responsibly"`

## 🔧 Features

### Smart Context Recognition
The agent extracts context from your queries:
- **Amounts:** Recognizes $300,000, 300k, 300 thousand
- **Age:** Extracts age for personalized advice
- **Income:** Identifies income levels for budget planning
- **Credit Score:** Detects scores for improvement plans

### Dynamic Responses
- Personalized advice based on extracted context
- EMI calculations for loans
- Age-based investment strategies
- Income-specific budget breakdowns
- Credit score improvement timelines

### CORS Enabled
The server includes CORS middleware, so you can call it from:
- React/Vue/Angular applications
- Static HTML pages
- Mobile applications
- Any frontend framework

## 🛠️ Development

### File Structure
```
FinsightAI/
├── local_server.py           # Main server file
├── local_requirements.txt    # Dependencies
├── start_local_server.ps1   # Startup script
├── test_local_api.html      # Test interface
└── README_LOCAL.md          # This file
```

### Customization
You can easily customize the responses by editing the `process_message` method in `local_server.py`. The agent uses keyword detection and context extraction to provide relevant financial advice.

### Adding New Features
1. Add new keyword patterns in `process_message`
2. Create helper methods for complex calculations
3. Update the capabilities list in `agent_info` endpoint

## 📱 Production Deployment

When ready for production:
1. Update CORS settings in `local_server.py`
2. Add authentication if needed
3. Use a production WSGI server like Gunicorn
4. Deploy to cloud platforms (AWS, Google Cloud, etc.)

## 🔍 Troubleshooting

### Server Won't Start
- Ensure Python 3.8+ is installed
- Install dependencies: `pip install -r local_requirements.txt`
- Check if port 8000 is available

### CORS Issues
- The server allows all origins by default for development
- For production, update the `allow_origins` in the CORS middleware

### API Not Responding
- Check server is running: `http://localhost:8000/`
- Verify JSON format in POST requests
- Check browser console for errors

## 💡 Pro Tips

1. **Use the Test Interface**: Open `test_local_api.html` for quick testing
2. **Context Matters**: Include specific amounts, ages, and situations for better responses
3. **Mobile Testing**: The API works great with mobile app development
4. **Performance**: The server handles multiple concurrent requests efficiently

Happy coding! 🚀
