from google.adk.agents import Agent
from app.services.adk_service import ADKService
from app.agents.threat_analysis.sub_agents.threat_analysis.prompt import THREAT_ANALYSIS_PROMPT

MODEL = ADKService().get_litellm_model()

def create_threat_analysis_agent():
    return Agent(
        name="ThreatAnalysisAgent",
        model=MODEL,
        instruction=THREAT_ANALYSIS_PROMPT,
        description="Extracts, enriches, assesses, and recommends actions for threats in a single step.",
        output_key="threat_analysis"
    )   
