from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools import google_search


gov_scheme_suggestor = Agent(
    name="gov_scheme_suggestor",
    model="gemini-2.0-flash",
    description="Suggests relevant government schemes based on user needs.",
    instruction="""
    You help users discover relevant Indian government schemes based on criteria like age, profession, income, or region .

    1. Use the google_search tool to find government schemes (scholarships, employment, subsidies, etc.)
    2. Summarize key benefits, eligibility, and how to apply.
    3. Prioritize official sources and portals for up-to-date and accurate data.

    Suggested trusted sources:
    - https://www.india.gov.in/
    - https://www.mygov.in/
    - https://www.nvsp.in/
    - State government portals

    Example response:
    "You may be eligible for the PMAY scheme offering housing subsidy up to ₹2.67 lakhs. Source: https://pmaymis.gov.in/"
    """,
    tools=[google_search]
)