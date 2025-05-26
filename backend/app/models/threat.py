from sqlalchemy import Column, String, Text, Float, JSON, ForeignKey, Enum, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum

from app.db.base_class import Base
from app.models.source import Source  # Ensure Source is imported before Threat is defined


class SeverityLevel(str, enum.Enum):
    """Enumeration for threat severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ThreatType(str, enum.Enum):
    """Enumeration for threat types"""
    MALWARE = "malware"
    PHISHING = "phishing"
    VULNERABILITY = "vulnerability"
    RANSOMWARE = "ransomware"
    APT = "apt"
    OTHER = "other"


class Threat(Base):
    """Model for threat intelligence data"""
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source_id = Column(Integer, ForeignKey("source.id"), nullable=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    severity = Column(Enum(SeverityLevel), nullable=False, default=SeverityLevel.MEDIUM, index=True)
    threat_type = Column(Enum(ThreatType), nullable=False, default=ThreatType.OTHER, index=True)
    confidence_score = Column(Float, nullable=False, default=0.0)
    source = relationship("app.models.source.Source", back_populates="threats")
    source_url = Column(String(1024), nullable=True)
    raw_content = Column(Text, nullable=True)
    # Indicators of Compromise (IOCs)
    iocs = Column(JSON, nullable=True, default=list)
    
    # Tactics, Techniques, and Procedures (TTPs)
    ttps = Column(JSON, nullable=True, default=list)
    
    # Additional metadata
    extra_metadata: Mapped[dict] = mapped_column(JSON, nullable=True, default=dict)
    
    # Relations to other threats
    related_threats = Column(JSON, nullable=True, default=list)
