from sqlalchemy import Column, String, Text, JSON, Enum, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum

from app.db.base_class import Base


class AnalysisStatus(str, enum.Enum):
    """Enumeration for analysis status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalysisType(str, enum.Enum):
    """Enumeration for analysis types"""
    IOC_EXTRACTION = "ioc_extraction"
    RISK_ASSESSMENT = "risk_assessment"
    ENTITY_RECOGNITION = "entity_recognition"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    FULL_ANALYSIS = "full_analysis"


class Analysis(Base):
    """Model for AI analysis results"""
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content_id = Column(String, nullable=True)  # Optional reference to original content
    content = Column(Text, nullable=True)  # Raw content that was analyzed
    analysis_type = Column(Enum(AnalysisType), nullable=False, default=AnalysisType.FULL_ANALYSIS)
    status = Column(Enum(AnalysisStatus), nullable=False, default=AnalysisStatus.PENDING, index=True)
    
    # Analysis results
    results = Column(JSON, nullable=True)
    
    # Extracted entities
    extracted_iocs = Column(JSON, nullable=True)
    extracted_ttps = Column(JSON, nullable=True)
    
    # Risk assessment
    risk_score = Column(JSON, nullable=True)
    
    # Model metadata
    model_used = Column(String(255), nullable=True)
    model_parameters = Column(JSON, nullable=True)
    
    # Error information (if failed)
    error = Column(Text, nullable=True)
