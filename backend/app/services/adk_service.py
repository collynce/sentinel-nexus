from typing import Dict, List, Optional, Any
import asyncio
import json
from loguru import logger

# Google ADK imports
from google.adk.models.lite_llm import LiteLlm

from app.core.config import settings
from app.services.bright_data_service import BrightDataService


class ADKService:
    """
    Utility service for Google ADK model instantiation and shared config.

    - Agents are now defined modularly in app/agents/*/agent.py (e.g., SequentialAgent, ParallelAgent).
    - Tools are defined in app/agents/*/tools.py.
    - This service provides a shared LiteLlm model instance for all agents and any shared utility logic.
    """
    def __init__(self):
        self.model = settings.DEFAULT_LLM_MODEL


    def get_litellm_model(self):
        """
        Utility function to provide the shared LiteLlm model instance for agents.
        """
        print(f'OPENROUTER_API_KEY {settings.OPENROUTER_API_KEY}')
        print(f'DEFAULT_LLM_MODEL {settings.DEFAULT_LLM_MODEL}')
        return self.model
    
    async def _extract_iocs_tool(self, text: str) -> Dict[str, Any]:
        """Tool implementation for IOC extraction"""
        # This would use the model directly through ADK
        # For now, we'll use a simple implementation
        messages = [
            Message(
                role="system",
                content="You are a cybersecurity expert. Extract all potential Indicators of Compromise (IOCs) from the provided text."
            ),
            Message(
                role="user",
                content=f"""
                Extract all potential Indicators of Compromise (IOCs) from the following text.
                Return the results as a JSON object with the following structure:
                {{
                    "ip_addresses": [
                        {{"value": "1.2.3.4", "confidence": 0.95}}
                    ],
                    "domains": [
                        {{"value": "example.com", "confidence": 0.92}}
                    ],
                    "urls": [
                        {{"value": "https://malicious.com/path", "confidence": 0.88}}
                    ],
                    "hashes": [
                        {{"type": "md5", "value": "d41d8cd98f00b204e9800998ecf8427e", "confidence": 0.97}}
                    ],
                    "emails": [
                        {{"value": "phish@example.com", "confidence": 0.91}}
                    ]
                }}
                
                Only include items that are likely to be actual IOCs. For each IOC, provide a confidence score between 0 and 1.
                
                Text to analyze:
                {text}
                """
            )
        ]
        
        response = await self.model_manager.generate_content(
            model=settings.DEFAULT_LLM_MODEL,
            messages=messages
        )
        
        try:
            content = response.text
            # Try to parse as JSON
            return json.loads(content)
        except json.JSONDecodeError:
            # If parsing fails, return empty results
            logger.error(f"Failed to parse IOC extraction response: {content}")
            return {
                "ip_addresses": [],
                "domains": [],
                "urls": [],
                "hashes": [],
                "emails": []
            }
    
    async def _assess_risk_tool(self, content: str, iocs: Dict[str, Any]) -> Dict[str, Any]:
        """Tool implementation for risk assessment"""
        messages = [
            Message(
                role="system",
                content="You are a cybersecurity risk analyst. Assess the risk level of the provided threat intelligence."
            ),
            Message(
                role="user",
                content=f"""
                Assess the risk level of the following threat intelligence content and extracted IOCs.
                Return the results as a JSON object with the following structure:
                {{
                    "overall_risk_score": 0.85,
                    "risk_level": "high",
                    "confidence": 0.92,
                    "reasoning": "This appears to be a sophisticated phishing campaign targeting financial institutions...",
                    "recommended_actions": [
                        "Block all identified IP addresses",
                        "Monitor for additional indicators"
                    ]
                }}
                
                Content:
                {content}
                
                Extracted IOCs:
                {json.dumps(iocs, indent=2)}
                """
            )
        ]
        
        response = await self.model_manager.generate_content(
            model=settings.DEFAULT_LLM_MODEL,
            messages=messages
        )
        
        try:
            content = response.text
            # Try to parse as JSON
            return json.loads(content)
        except json.JSONDecodeError:
            # If parsing fails, return a default assessment
            logger.error(f"Failed to parse risk assessment response: {content}")
            return {
                "overall_risk_score": 0.5,
                "risk_level": "medium",
                "confidence": 0.7,
                "reasoning": "Unable to properly assess risk from the provided content.",
                "recommended_actions": ["Manual review required"]
            }
