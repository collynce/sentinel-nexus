from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

from app.models.threat import SeverityLevel, ThreatType
from app.schemas.base import BaseSchema


class IOCBase(BaseModel):
    """Base schema for Indicators of Compromise"""
    type: str
    value: str
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class TTPBase(BaseModel):
    """Base schema for Tactics, Techniques, and Procedures"""
    tactic: str
    technique: str
    procedure: Optional[str] = None
    mitre_id: Optional[str] = None


class ThreatBase(BaseModel):
    """Base schema for threat data"""
    title: str
    description: Optional[str] = None
    severity: SeverityLevel = SeverityLevel.MEDIUM
    threat_type: ThreatType = ThreatType.OTHER
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    source_id: Optional[str] = None
    source_url: Optional[str] = None


class ThreatCreate(ThreatBase):
    """Schema for creating a new threat"""
    raw_content: Optional[str] = None
    iocs: Optional[List[Dict[str, Any]]] = None
    ttps: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None
    related_threats: Optional[List[str]] = None


class ThreatUpdate(ThreatBase):
    """Schema for updating an existing threat"""
    title: Optional[str] = None
    raw_content: Optional[str] = None
    iocs: Optional[List[Dict[str, Any]]] = None
    ttps: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None
    related_threats: Optional[List[str]] = None


class Threat(ThreatBase, BaseSchema):
    """Complete threat schema with all fields"""
    raw_content: Optional[str] = None
    iocs: Optional[List[Dict[str, Any]]] = None
    ttps: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None
    related_threats: Optional[List[str]] = None
