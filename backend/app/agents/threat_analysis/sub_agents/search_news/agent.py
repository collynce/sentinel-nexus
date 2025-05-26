from google.adk.agents import Agent
from .prompt import SEARCH_NEWS_PROMPT
from app.services.adk_service import ADKService
from app.agents.threat_analysis.utils.mcp_init import check_search_news_tools

MODEL = ADKService().get_litellm_model()


def create_search_news_agent():
    return Agent(
        name="SearchNewsAgent",
        model=MODEL,
        instruction=SEARCH_NEWS_PROMPT,
        description="Searches news sources for threat intelligence using Brightdata MCP tools.",
        before_model_callback=check_search_news_tools,
        output_key="news_data"
    )
