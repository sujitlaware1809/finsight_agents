import React, { useState, useEffect } from 'react';

// Custom hook for FinSight AI integration
export const useFinSightAI = (baseUrl = 'http://localhost:8000') => {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState('');
  const [error, setError] = useState(null);
  const [serverStatus, setServerStatus] = useState('checking');

  // Check server status
  const checkServerStatus = async () => {
    try {
      const response = await fetch(`${baseUrl}/`);
      const data = await response.json();
      setServerStatus(data.status === 'healthy' ? 'online' : 'offline');
      return true;
    } catch (error) {
      setServerStatus('offline');
      return false;
    }
  };

  // Send message to AI
  const askAI = async (message, userId = 'default') => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${baseUrl}/chat`, {
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
      
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to get response');
      }
      
      setResponse(data.response);
      return data.response;
      
    } catch (err) {
      setError(err.message);
      setResponse('Sorry, there was an error connecting to FinSight AI.');
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Get agent information
  const getAgentInfo = async () => {
    try {
      const response = await fetch(`${baseUrl}/agent-info`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Failed to get agent info:', error);
      return null;
    }
  };

  useEffect(() => {
    checkServerStatus();
  }, []);

  return {
    askAI,
    getAgentInfo,
    checkServerStatus,
    loading,
    response,
    error,
    serverStatus
  };
};

// React Component Example
export const FinSightAIChat = () => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const { askAI, loading, serverStatus, checkServerStatus } = useFinSightAI();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    // Add user message to chat
    const userMessage = { type: 'user', content: message, timestamp: Date.now() };
    setChatHistory(prev => [...prev, userMessage]);

    // Get AI response
    const response = await askAI(message);
    
    if (response) {
      const aiMessage = { type: 'ai', content: response, timestamp: Date.now() };
      setChatHistory(prev => [...prev, aiMessage]);
    }

    setMessage('');
  };

  const quickTests = [
    "Hello, I need financial advice",
    "I want a $250,000 home loan",
    "How to invest $50,000 at age 30?",
    "Improve my 620 credit score",
    "Create budget for $8000 income",
    "Best credit card for beginners"
  ];

  return (
    <div className="finsight-chat">
      <div className="chat-header">
        <h2>🏦 FinSight AI Assistant</h2>
        <div className={`status ${serverStatus}`}>
          {serverStatus === 'online' ? '🟢 Online' : '🔴 Offline'}
          <button onClick={checkServerStatus}>🔄</button>
        </div>
      </div>

      <div className="chat-messages">
        {chatHistory.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            <div className="message-content">
              {msg.content}
            </div>
            <div className="message-timestamp">
              {new Date(msg.timestamp).toLocaleTimeString()}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message ai">
            <div className="message-content">🤔 Thinking...</div>
          </div>
        )}
      </div>

      <div className="quick-tests">
        {quickTests.map((test, index) => (
          <button
            key={index}
            onClick={() => setMessage(test)}
            className="quick-test-btn"
          >
            {test}
          </button>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="chat-input">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask me anything about finances..."
          rows="3"
          disabled={loading || serverStatus === 'offline'}
        />
        <button
          type="submit"
          disabled={loading || !message.trim() || serverStatus === 'offline'}
        >
          {loading ? '⏳' : '💬'} Send
        </button>
      </form>
    </div>
  );
};

// Vanilla JavaScript Integration
export const FinSightAIClient = class {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  async checkHealth() {
    try {
      const response = await fetch(`${this.baseUrl}/`);
      return await response.json();
    } catch (error) {
      throw new Error('Server unavailable');
    }
  }

  async sendMessage(message, userId = 'default') {
    try {
      const response = await fetch(`${this.baseUrl}/chat`, {
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
      
      if (!response.ok) {
        throw new Error(data.detail || 'Request failed');
      }

      return data;
    } catch (error) {
      throw new Error(`Failed to send message: ${error.message}`);
    }
  }

  async getAgentInfo() {
    try {
      const response = await fetch(`${this.baseUrl}/agent-info`);
      return await response.json();
    } catch (error) {
      throw new Error('Failed to get agent info');
    }
  }
};

// Usage Examples:

/*
// 1. React Hook Usage:
function MyFinanceApp() {
  const { askAI, loading, response, serverStatus } = useFinSightAI();

  const handleQuestion = async () => {
    await askAI("I need a home loan for $300,000");
  };

  return (
    <div>
      <button onClick={handleQuestion} disabled={loading}>
        Ask AI
      </button>
      {loading && <p>Loading...</p>}
      {response && <p>{response}</p>}
    </div>
  );
}

// 2. Vanilla JavaScript Usage:
const aiClient = new FinSightAIClient();

// Check if server is running
aiClient.checkHealth()
  .then(health => console.log('Server status:', health))
  .catch(error => console.error('Server offline:', error));

// Send a message
aiClient.sendMessage('I want to invest $50,000', 'user_123')
  .then(response => console.log('AI Response:', response.response))
  .catch(error => console.error('Error:', error));

// 3. Async/Await Usage:
async function getFinancialAdvice() {
  try {
    const client = new FinSightAIClient();
    const response = await client.sendMessage('Help me with budgeting');
    console.log(response.response);
  } catch (error) {
    console.error('Error getting advice:', error);
  }
}
*/
