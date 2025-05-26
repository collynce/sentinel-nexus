from google.adk.agents import Agent
from .prompt import DISCOVERER_PROMPT
from app.services.adk_service import ADKService
from app.agents.threat_analysis.utils.mcp_init import check_discoverer_tools

MODEL = ADKService().get_litellm_model()


def create_discoverer_agent():
    return Agent(
        name="DiscovererAgent",
        model=MODEL,
        instruction=DISCOVERER_PROMPT,
        description="Plans and generates targeted web data discovery queries for threat intelligence.",
        before_model_callback=check_discoverer_tools,
        output_key="discovery_queries"
    )