from sqlalchemy import Column, String, Text, Boolean, JSON, Enum, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum

from app.db.base_class import Base


class SourceType(str, enum.Enum):
    """Enumeration for data source types"""
    NEWS = "news"
    SOCIAL_MEDIA = "social_media"
    DARK_WEB = "dark_web"
    PASTE_SITE = "paste_site"
    GITHUB = "github"
    LINKEDIN = "linkedin"
    OTHER = "other"


class Source(Base):
    """Model for data collection sources"""
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    source_type = Column(Enum(SourceType), nullable=False, default=SourceType.OTHER, index=True)
    url = Column(String(1024), nullable=True)
    enabled = Column(Boolean, default=True, nullable=False, index=True)
    
    # Bright Data configuration
    bright_data_config = Column(JSON, nullable=True)
    
    # Collection schedule (cron expression)
    schedule = Column(String(100), nullable=True)
    
    # Collection parameters
    parameters = Column(JSON, nullable=True)
    
    # Authentication credentials (encrypted)
    credentials = Column(JSON, nullable=True)
    
    # Related threats
    threats = relationship("app.models.threat.Threat", back_populates="source")
    
    # Last collection timestamp and status
    last_collection_status = Column(JSON, nullable=True)
