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
    # Try loading agents in order of preference
    try:
        from delegator.agent import root_agent
        logger.info(f"Full agent {root_agent.name} loaded successfully")
    except Exception as e:
        logger.warning(f"Full agent failed, trying simple agent: {e}")
        try:
            from delegator.simple_agent import root_agent
            logger.info(f"Simple agent {root_agent.name} loaded successfully")
        except Exception as e2:
            logger.warning(f"Simple agent failed, using fallback: {e2}")
            from delegator.fallback_agent import root_agent
            logger.info(f"Fallback agent {root_agent.name} loaded successfully")
except Exception as e:
    logger.error(f"Failed to load any agent: {e}")
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
    uvicorn.run("app:app", host="0.0.0.0", port=port)
