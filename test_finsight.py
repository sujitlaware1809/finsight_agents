#!/usr/bin/env python3
"""
Simple test for deployed FinSight AI agent
"""

import os
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv

def test_deployed_agent():
    """Test the deployed FinSight AI agent"""
    print("🧪 TESTING DEPLOYED FINSIGHT AI")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize Vertex AI
    project = os.getenv('GOOGLE_CLOUD_PROJECT', 'driven-edition-467110-p6')
    location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
    
    vertexai.init(project=project, location=location)
    print(f"📡 Project: {project}")
    print(f"🌍 Location: {location}")
    
    # Agent details
    agent_id = "7093829120085196800"
    agent_resource = f"projects/996911716674/locations/us-central1/reasoningEngines/{agent_id}"
    
    print(f"🤖 Agent ID: {agent_id}")
    print(f"📋 Resource: {agent_resource}")
    
    try:
        # Get the deployed agent
        agent_engine = agent_engines.get(agent_resource)
        print("✅ Successfully connected to agent!")
        
        # Simple test query
        test_query = "I have $5000 to invest. What are my options?"
        print(f"\n📝 Test Query: {test_query}")
        
        # Send query to agent
        response = agent_engine.stream_query(input=test_query)
        
        # Collect response
        full_response = ""
        print("🤖 Agent Response:")
        print("-" * 30)
        
        for chunk in response:
            if hasattr(chunk, 'text') and chunk.text:
                full_response += chunk.text
                print(chunk.text, end="")
        
        print("\n" + "-" * 30)
        print("✅ TEST SUCCESSFUL!")
        print(f"📊 Response length: {len(full_response)} characters")
        
        # API endpoint info
        print(f"\n🌐 API Endpoint:")
        print(f"https://us-central1-aiplatform.googleapis.com/v1/projects/{project}/locations/{location}/reasoningEngines/{agent_id}:streamQuery")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_deployed_agent()
    if success:
        print("\n🎉 FinSight AI is working perfectly!")
    else:
        print("\n💥 There was an issue with the agent")
