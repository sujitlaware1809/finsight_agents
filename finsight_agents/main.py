"""
Main entry point for FinSight AI Agent
Supports both local development and cloud deployment
"""

import os
import logging
from typing import Any, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the application"""
    try:
        # Import the delegator agent
        from delegator.agent import root_agent
        
        # For cloud deployment, we need to return the agent
        return root_agent
        
    except Exception as e:
        logger.error(f"Failed to create app: {e}")
        raise

def main(request=None):
    """
    Cloud Functions entry point
    """
    try:
        agent = create_app()
        
        if request is None:
            # Local development mode
            logger.info("Starting in local development mode")
            return agent
        
        # Cloud Functions mode
        if request.method == 'POST':
            # Handle agent interaction
            data = request.get_json()
            if not data:
                return {'error': 'No data provided'}, 400
            
            # Process the request through the agent
            response = agent.run(data.get('message', ''))
            return {'response': response}
        
        elif request.method == 'GET':
            # Health check
            return {'status': 'healthy', 'agent': agent.name}
        
        else:
            return {'error': 'Method not allowed'}, 405
            
    except Exception as e:
        logger.error(f"Error in main function: {e}")
        return {'error': str(e)}, 500

# For local ADK web development
if __name__ == "__main__":
    # Check if running with ADK web
    if os.getenv('ADK_WEB_MODE'):
        # ADK web will import the agent directly
        from delegator.agent import root_agent
        print(f"Agent {root_agent.name} ready for ADK web interface")
    else:
        # Manual local testing
        agent = create_app()
        print(f"Agent {agent.name} created successfully")
        
        # Simple test interaction
        test_message = "Hello, I need financial advice"
        try:
            response = agent.run(test_message)
            print(f"Test response: {response}")
        except Exception as e:
            print(f"Test failed: {e}")
