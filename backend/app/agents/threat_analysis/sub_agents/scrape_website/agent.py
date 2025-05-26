from google.adk.agents import Agent
from .prompt import SCRAPE_WEBSITE_PROMPT
from app.services.adk_service import ADKService
from app.agents.threat_analysis.utils.mcp_init import check_scrape_website_tools

MODEL = ADKService().get_litellm_model()

def create_scrape_website_agent():
    return Agent(
        name="ScrapeWebsiteAgent",
        model=MODEL,
        instruction=SCRAPE_WEBSITE_PROMPT,
        description="Scrapes structured data from specified websites using Bright Data MCP tools.",
        before_model_callback=check_scrape_website_tools,
        output_key="website_data"
    )
