from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.source import Source, SourceCreate, SourceUpdate
from app.services.source_service import SourceService

router = APIRouter()


@router.get("/", response_model=List[Source])
async def get_sources(
    skip: int = 0,
    limit: int = 100,
    source_type: Optional[str] = Query(None, description="Filter by source type"),
    enabled: Optional[bool] = Query(None, description="Filter by enabled status"),
    db: AsyncSession = Depends(get_db),
):
    """Get list of data sources with optional filtering"""
    source_service = SourceService(db)
    return await source_service.get_sources(skip=skip, limit=limit, source_type=source_type, enabled=enabled)


@router.get("/{source_id}", response_model=Source)
async def get_source(source_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific data source by ID"""
    source_service = SourceService(db)
    source = await source_service.get_source(source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with ID {source_id} not found",
        )
    return source


@router.post("/", response_model=Source, status_code=status.HTTP_201_CREATED)
async def create_source(source: SourceCreate, db: AsyncSession = Depends(get_db)):
    """Create a new data source"""
    source_service = SourceService(db)
    return await source_service.create_source(source)


@router.put("/{source_id}", response_model=Source)
async def update_source(source_id: str, source: SourceUpdate, db: AsyncSession = Depends(get_db)):
    """Update an existing data source"""
    source_service = SourceService(db)
    updated_source = await source_service.update_source(source_id, source)
    if not updated_source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with ID {source_id} not found",
        )
    return updated_source


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(source_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a data source"""
    source_service = SourceService(db)
    success = await source_service.delete_source(source_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with ID {source_id} not found",
        )
    return None


@router.post("/{source_id}/trigger", status_code=status.HTTP_202_ACCEPTED)
async def trigger_source_ingestion(source_id: str, db: AsyncSession = Depends(get_db)):
    """Manually trigger data ingestion for a specific source"""
    source_service = SourceService(db)
    source = await source_service.get_source(source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with ID {source_id} not found",
        )
    
    # Trigger the ingestion process asynchronously
    # In a real implementation, this would likely use a task queue like Celery
    # For now, we'll just return a success message
    return {"status": "ingestion_triggered", "source_id": source_id}
