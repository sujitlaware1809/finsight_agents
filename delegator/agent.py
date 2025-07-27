from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from google.adk.tools import google_search
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams

#from .sub_agents.stock_analyst.agent import stock_analyst
from .sub_agents.tax_filing_helper.agent import tax_filing_helper
from .sub_agents.gov_scheme_suggestor.agent import gov_scheme_suggestor
from .sub_agents.loan_helper.agent import loan_helper
from .sub_agents.credit_card_provider.agent import credit_card_provider
from .sub_agents.credit_score_improver.agent import credit_score_improver


# new

from .sub_agents.investment_guide.agent import investment_guide
from .sub_agents.scam_detector.agent import scam_detector
from .sub_agents.budget_planner.agent import budget_planner


mcp_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="http://localhost:8080/mcp/stream",  # Your MCP tool endpoint
        method="POST"
    )
)

root_agent = Agent(
    name="delegator",
    model="gemini-2.0-flash",
    description="delegator agent",
    instruction="""
    You are a delegation agent that is responsible for overseeing the work of the other agents and tools.
    first greet the user:-

    **Step 1: Before performing any task, you must first call the `mcp_toolset` to fetch the user's information.** This user data will help you understand the context and requirements. Ensure that this step is completed before deciding which tool or agent to use.

    **Step 2: Based on the retrieved user information, determine the most appropriate tool or sub-agent to handle the user's needs.** Use your best judgment to delegate the task accordingly.

    You are responsible for delegating tasks to the following agent:
    - stock_analyst

    You also have access to the following tools:
    
    - loan_helper
    - gov_scheme_suggestor
    - credit_card_provider 
    - credit_score_improver
    - tax_filing_helper
    - investment_guide
    - scam_detector
    - budget_planner
    
    **Step 3: Once the appropriate tool or agent completes its task, summarize the result and present it to the user clearly and concisely as your final output.**
    Always follow this structure:
    1. Fetch user information using `mcp_toolset`.
    2. Delegate the task based on the user's data.
    3. Summarize and present the results to the user.
    """,
    # sub_agents=[stock_analyst, loan_helper, gov_scheme_suggestor, credit_card_provider, credit_score_improver],
    #sub_agents = [stock_analyst],
    
    tools=[mcp_toolset,
        AgentTool(loan_helper),
        AgentTool(gov_scheme_suggestor),
        AgentTool(credit_card_provider),
        AgentTool(credit_score_improver),
        AgentTool(tax_filing_helper),
        AgentTool(investment_guide),
        AgentTool(scam_detector),
        AgentTool(budget_planner)
        
    ],
    

)




