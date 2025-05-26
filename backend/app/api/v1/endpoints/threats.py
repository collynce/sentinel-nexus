from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.threat import Threat as ThreatModel
from app.schemas.threat import Threat as ThreatSchema, ThreatCreate, ThreatUpdate
from app.services.threat_service import ThreatService

router = APIRouter()


def threat_to_schema(threat: ThreatModel) -> ThreatSchema:
    return ThreatSchema(
        id=str(threat.id), 
        title=threat.title,
        description=threat.description,
        severity=threat.severity,
        threat_type=threat.threat_type,
        confidence_score=threat.confidence_score,
        source_id=str(threat.source_id) if threat.source_id else None,
        source_url=threat.source_url,
        raw_content=threat.raw_content,
        iocs=threat.iocs,
        ttps=threat.ttps,
        metadata=threat.extra_metadata if threat.extra_metadata else {},
        related_threats=threat.related_threats,
        created_at=threat.created_at,
        updated_at=threat.updated_at,
    )


@router.get("/", response_model=List[ThreatSchema])
async def get_threats(
    skip: int = 0,
    limit: int = 100,
    severity: Optional[str] = Query(None, description="Filter by severity level"),
    source_type: Optional[str] = Query(None, description="Filter by source type"),
    db: AsyncSession = Depends(get_db),
):
    """Get list of threats with optional filtering"""
    threat_service = ThreatService(db)
    db_threats = await threat_service.get_threats(skip=skip, limit=limit, severity=severity, source_type=source_type)
    return [threat_to_schema(threat) for threat in db_threats]


@router.get("/{threat_id}", response_model=ThreatSchema)
async def get_threat(threat_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific threat by ID"""
    threat_service = ThreatService(db)
    threat = await threat_service.get_threat(threat_id)
    if not threat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Threat with ID {threat_id} not found",
        )
    return threat_to_schema(threat)


@router.post("/", response_model=ThreatSchema, status_code=status.HTTP_201_CREATED)
async def create_threat(threat: ThreatCreate, db: AsyncSession = Depends(get_db)):
    """Create a new threat"""
    threat_service = ThreatService(db)
    db_threat = await threat_service.create_threat(threat)
    return threat_to_schema(db_threat)


@router.put("/{threat_id}", response_model=ThreatSchema)
async def update_threat(threat_id: int, threat: ThreatUpdate, db: AsyncSession = Depends(get_db)):
    """Update an existing threat"""
    threat_service = ThreatService(db)
    updated_threat = await threat_service.update_threat(threat_id, threat)
    if not updated_threat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Threat with ID {threat_id} not found",
        )
    return threat_to_schema(updated_threat)


@router.delete("/{threat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_threat(threat_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a threat"""
    threat_service = ThreatService(db)
    success = await threat_service.delete_threat(threat_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Threat with ID {threat_id} not found",
        )
    return None
