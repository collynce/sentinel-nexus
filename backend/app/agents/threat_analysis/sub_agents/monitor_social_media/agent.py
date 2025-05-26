from google.adk.agents import Agent
from .prompt import MONITOR_SOCIAL_MEDIA_PROMPT
from app.services.adk_service import ADKService
from app.agents.threat_analysis.utils.mcp_init import check_monitor_social_media_tools

MODEL = ADKService().get_litellm_model()


def create_monitor_social_media_agent():
    return Agent(
        name="MonitorSocialMediaAgent",
        model=MODEL,
        instruction=MONITOR_SOCIAL_MEDIA_PROMPT,
        description="Monitors social media for threat intelligence using MCP tools.",
        before_model_callback=check_monitor_social_media_tools,
        output_key="social_media_data"
    )
