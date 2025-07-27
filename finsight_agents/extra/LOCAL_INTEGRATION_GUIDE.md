# FinSight AI - Local Development Server

## 🚀 Quick Start

### 1. Start the Local Server

```bash
# Install dependencies
pip install -r requirements_local.txt

# Start the server
python local_server.py
```

The server will start on `http://localhost:8000`

### 2. Test the API

Open `frontend_demo.html` in your browser to test the API interactively.

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/agent-info` | Get agent capabilities |
| POST | `/chat` | Send message to AI |

## 💻 Frontend Integration

### JavaScript/React Integration

```javascript
// Basic usage
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "I need a home loan for $300,000",
    user_id: "user_123"
  })
});

const data = await response.json();
console.log(data.response);
```

### React Hook (recommended)

```javascript
import { useFinSightAI } from './frontend_integration';

function MyApp() {
  const { askAI, loading, response, serverStatus } = useFinSightAI();
  
  const handleClick = async () => {
    await askAI("Help me with budgeting");
  };
  
  return (
    <div>
      <button onClick={handleClick} disabled={loading}>
        Ask AI
      </button>
      {response && <p>{response}</p>}
    </div>
  );
}
```

### Vue.js Integration

```javascript
// Vue.js composition API
import { ref } from 'vue';

export function useFinSightAI() {
  const loading = ref(false);
  const response = ref('');
  
  const askAI = async (message) => {
    loading.value = true;
    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, user_id: 'vue_user' })
      });
      const data = await res.json();
      response.value = data.response;
    } catch (error) {
      response.value = 'Error connecting to AI';
    } finally {
      loading.value = false;
    }
  };
  
  return { askAI, loading, response };
}
```

### Angular Service

```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FinSightAIService {
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  sendMessage(message: string, userId: string = 'angular_user'): Observable<any> {
    return this.http.post(`${this.baseUrl}/chat`, {
      message,
      user_id: userId
    });
  }

  getAgentInfo(): Observable<any> {
    return this.http.get(`${this.baseUrl}/agent-info`);
  }
}
```

## 📋 Request/Response Format

### Chat Request

```json
{
  "message": "I need financial advice",
  "user_id": "user_123"
}
```

### Chat Response

```json
{
  "response": "🌟 Welcome to FinSight AI! Your comprehensive financial advisor...",
  "status": "success"
}
```

### Agent Info Response

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

## 🧪 Sample Queries

Test these queries to see different AI responses:

1. **Greeting**: "Hello, I need financial advice"
2. **Loan Query**: "I want a $250,000 home loan"
3. **Investment**: "How to invest $50,000 at age 30?"
4. **Credit Score**: "Improve my 620 credit score"
5. **Budgeting**: "Create budget for $8000 monthly income"
6. **Credit Cards**: "Best credit card for beginners"

## 🔧 Integration Tips

### CORS Configuration

The server includes CORS middleware to allow frontend connections. For production, update the `allow_origins` in `local_server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Error Handling

Always implement error handling in your frontend:

```javascript
try {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, user_id })
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  const data = await response.json();
  return data.response;
} catch (error) {
  console.error('API Error:', error);
  return 'Sorry, there was an error connecting to the AI.';
}
```

### Loading States

Implement loading states for better UX:

```javascript
const [loading, setLoading] = useState(false);

const handleSubmit = async () => {
  setLoading(true);
  try {
    const response = await askAI(message);
    // Handle response
  } finally {
    setLoading(false);
  }
};
```

## 🌐 Deployment Notes

For production deployment:

1. Change `host="0.0.0.0"` to `host="127.0.0.1"` for security
2. Set specific CORS origins
3. Add authentication if needed
4. Use environment variables for configuration
5. Add rate limiting
6. Implement proper logging

## 📁 File Structure

```
FinsightAI/
├── local_server.py              # Main API server
├── requirements_local.txt       # Python dependencies
├── frontend_demo.html          # Interactive test page
├── frontend_integration.js     # React/JS integration code
├── frontend_styles.css         # CSS styles for components
└── LOCAL_INTEGRATION_GUIDE.md  # This file
```

## 🐛 Troubleshooting

### Server Won't Start
- Check if port 8000 is available
- Verify Python dependencies are installed
- Check for syntax errors in local_server.py

### CORS Errors
- Ensure CORS middleware is properly configured
- Check that your frontend URL is in allowed origins

### Connection Refused
- Verify server is running on http://localhost:8000
- Check firewall settings
- Ensure you're using the correct URL in frontend

### API Returns 500 Error
- Check server logs for detailed error messages
- Verify request format matches expected schema
- Test with simple messages first

## 🔗 Next Steps

1. **Start the server**: `python local_server.py`
2. **Test the API**: Open `frontend_demo.html`
3. **Integrate with your app**: Use the provided code examples
4. **Customize responses**: Modify the agent logic in `local_server.py`
5. **Deploy to production**: Use the cloud deployment when ready

Happy coding! 🚀
