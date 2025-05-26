from typing import Dict, Optional, Any
from pydantic import BaseModel, Field, HttpUrl

from app.models.source import SourceType
from app.schemas.base import BaseSchema


class BrightDataConfig(BaseModel):
    """Configuration for Bright Data services"""
    service_type: str = Field(..., description="Type of Bright Data service (web_unlocker, web_scraper, proxy)")
    endpoint: Optional[str] = None
    zone: Optional[str] = None
    country: Optional[str] = None
    session_id: Optional[str] = None
    custom_headers: Optional[Dict[str, str]] = None
    proxy_options: Optional[Dict[str, Any]] = None


class SourceBase(BaseModel):
    """Base schema for data sources"""
    name: str
    description: Optional[str] = None
    source_type: SourceType = SourceType.OTHER
    url: Optional[HttpUrl] = None
    enabled: bool = True


class SourceCreate(SourceBase):
    """Schema for creating a new data source"""
    bright_data_config: Optional[BrightDataConfig] = None
    schedule: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    credentials: Optional[Dict[str, Any]] = None


class SourceUpdate(SourceBase):
    """Schema for updating an existing data source"""
    name: Optional[str] = None
    bright_data_config: Optional[BrightDataConfig] = None
    schedule: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    credentials: Optional[Dict[str, Any]] = None


class Source(SourceBase, BaseSchema):
    """Complete source schema with all fields"""
    bright_data_config: Optional[BrightDataConfig] = None
    schedule: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    last_collection_status: Optional[Dict[str, Any]] = None
