"""
Utility functions for storing threat data from data collection agents.
Ensures all agent output is validated and persisted using the ThreatService.
"""
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.threat import ThreatCreate
from app.services.threat_service import ThreatService
from app.models.threat import SeverityLevel, ThreatType
import json

async def store_agent_threat(
    db_session: AsyncSession,
    agent_output: Dict[str, Any],
) -> Optional[int]:
    """
    Validates and stores agent output as a Threat record using ThreatService.
    Returns the new Threat ID if successful, else None.
    """
    try:
        threat_data = map_agent_output_to_threat_create(agent_output)
        service = ThreatService(db_session)
        threat = await service.create_threat(threat_data)
        return threat.id
    except Exception as e:
        # Optional: Add logging here
        print(f"[ThreatUtils] Failed to store threat: {e}")
        return None

def map_agent_output_to_threat_create(agent_output: Dict[str, Any]) -> ThreatCreate:
    """
    Maps the raw agent output dictionary to a ThreatCreate Pydantic model.
    """
    threat_assessment = agent_output.get("threat_assessment", {})
    technical_details = agent_output.get("technical_details", {})
    threat_actor = agent_output.get("threat_actor", {})
    impact_assessment = agent_output.get("impact_assessment", {})
    evidence = agent_output.get("evidence", {})
    metadata = agent_output.get("metadata", {})

    # Helper to convert string confidence to float
    def confidence_to_float(confidence_str: str) -> float:
        if confidence_str == "high":
            return 1.0
        elif confidence_str == "medium":
            return 0.5
        elif confidence_str == "low":
            return 0.0
        return 0.0 # Default to low if unknown

    # Map severity string to enum
    severity_level = SeverityLevel.MEDIUM
    if threat_assessment.get("severity"):
        try:
            severity_level = SeverityLevel(threat_assessment["severity"].lower())
        except ValueError:
            pass # Keep default

    # Map threat_type string to enum
    threat_type_enum = ThreatType.OTHER
    if threat_assessment.get("threat_type"):
        try:
            threat_type_enum = ThreatType(threat_assessment["threat_type"].lower())
        except ValueError:
            pass # Keep default

    # Extract IOCs (simplified for now, can be expanded)
    iocs = []
    if technical_details.get("infrastructure", {}).get("domains"):
        for domain in technical_details["infrastructure"]["domains"]:
            iocs.append({"type": "domain", "value": domain, "confidence": 1.0})
    if technical_details.get("infrastructure", {}).get("c2_servers"):
        for c2 in technical_details["infrastructure"]["c2_servers"]:
            iocs.append({"type": "c2_server", "value": c2, "confidence": 1.0})

    # Extract TTPs
    ttps = []
    if threat_actor.get("observed_ttps"):
        for ttp_id in threat_actor["observed_ttps"]:
            # This is a simplified mapping, ideally you'd parse MITRE IDs properly
            ttps.append({"tactic": "unknown", "technique": ttp_id, "mitre_id": ttp_id})

    # Construct metadata dictionary
    extra_metadata = {
        "analysis_id": agent_output.get("analysis_id"),
        "timestamp": agent_output.get("timestamp"),
        "impact_assessment": impact_assessment,
        "recommendations": agent_output.get("recommendations"),
        "agent_metadata": metadata # Include the agent's own metadata section
    }

    # Determine source_url from news_sources if available
    source_url = None
    if evidence.get("news_sources") and len(evidence["news_sources"]) > 0:
        source_url = evidence["news_sources"][0].get("url")

    return ThreatCreate(
        title=threat_assessment.get("name", "Untitled Threat"),
        description=threat_assessment.get("summary"),
        severity=severity_level,
        threat_type=threat_type_enum,
        confidence_score=confidence_to_float(threat_assessment.get("confidence", "low")),
        source_id=None, # Cannot derive from current agent output
        source_url=source_url,
        raw_content=json.dumps(agent_output, indent=2), # Store full agent output as raw content
        iocs=iocs,
        ttps=ttps,
        metadata=extra_metadata,
        related_threats=[] # Not directly available from agent output
    )
