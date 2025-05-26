from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.analysis import Analysis, AnalysisCreate, AnalysisResult
from app.services.analysis_service import AnalysisService

router = APIRouter()


@router.post("/", response_model=AnalysisResult, status_code=status.HTTP_202_ACCEPTED)
async def analyze_content(analysis: AnalysisCreate, db: AsyncSession = Depends(get_db)):
    """Submit content for threat analysis"""
    analysis_service = AnalysisService(db)
    return await analysis_service.analyze_content(analysis)


@router.get("/results", response_model=List[Analysis])
async def get_analysis_results(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None, description="Filter by analysis status"),
    db: AsyncSession = Depends(get_db),
):
    """Get list of analysis results with optional filtering"""
    analysis_service = AnalysisService(db)
    return await analysis_service.get_analysis_results(skip=skip, limit=limit, status=status)


@router.get("/results/{analysis_id}", response_model=Analysis)
async def get_analysis_result(analysis_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific analysis result by ID"""
    analysis_service = AnalysisService(db)
    analysis = await analysis_service.get_analysis_result(analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis with ID {analysis_id} not found",
        )
    return analysis


@router.post("/extract-iocs")
async def extract_iocs(text: str):
    """Extract IOCs from text using AI"""
    # This would use the LLM service to extract IOCs
    # For now, return a placeholder
    return {
        "iocs": [
            {"type": "ip", "value": "192.168.1.1", "confidence": 0.95},
            {"type": "domain", "value": "example.com", "confidence": 0.92},
        ]
    }
