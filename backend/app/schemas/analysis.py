from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from app.models.analysis import AnalysisType, AnalysisStatus
from app.schemas.base import BaseSchema


class AnalysisBase(BaseModel):
    """Base schema for analysis data"""
    analysis_type: AnalysisType = AnalysisType.FULL_ANALYSIS
    content_id: Optional[str] = None


class AnalysisCreate(AnalysisBase):
    """Schema for creating a new analysis"""
    content: str = Field(..., description="Raw content to analyze")
    model_parameters: Optional[Dict[str, Any]] = None


class AnalysisUpdate(BaseModel):
    """Schema for updating an existing analysis"""
    status: Optional[AnalysisStatus] = None
    results: Optional[Dict[str, Any]] = None
    extracted_iocs: Optional[List[Dict[str, Any]]] = None
    extracted_ttps: Optional[List[Dict[str, Any]]] = None
    risk_score: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class Analysis(AnalysisBase, BaseSchema):
    """Complete analysis schema with all fields"""
    content: Optional[str] = None
    status: AnalysisStatus = AnalysisStatus.PENDING
    results: Optional[Dict[str, Any]] = None
    extracted_iocs: Optional[List[Dict[str, Any]]] = None
    extracted_ttps: Optional[List[Dict[str, Any]]] = None
    risk_score: Optional[Dict[str, Any]] = None
    model_used: Optional[str] = None
    model_parameters: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class AnalysisResult(BaseModel):
    """Schema for analysis result response"""
    analysis_id: str
    status: AnalysisStatus
    message: str
