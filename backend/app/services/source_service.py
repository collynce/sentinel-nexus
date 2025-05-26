from typing import List, Optional, Dict, Any
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.source import Source
from app.schemas.source import SourceCreate, SourceUpdate


class SourceService:
    """Service for managing data collection sources"""
    
    def __init__(self, db: AsyncSession):
        """Initialize with database session"""
        self.db = db
    
    async def get_sources(
        self, 
        skip: int = 0, 
        limit: int = 100,
        source_type: Optional[str] = None,
        enabled: Optional[bool] = None,
    ) -> List[Source]:
        """Get list of sources with optional filtering"""
        query = select(Source).offset(skip).limit(limit)
        
        # Apply filters if provided
        if source_type:
            query = query.filter(Source.source_type == source_type)
        
        if enabled is not None:
            query = query.filter(Source.enabled == enabled)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_source(self, source_id: str) -> Optional[Source]:
        """Get a specific source by ID"""
        query = select(Source).filter(Source.id == source_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def create_source(self, source_data: SourceCreate) -> Source:
        """Create a new data source"""
        # Convert Pydantic model to dict, excluding None values
        source_dict = source_data.model_dump(exclude_none=True)
        
        # Create new source object
        db_source = Source(**source_dict)
        
        # Add to database
        self.db.add(db_source)
        await self.db.commit()
        await self.db.refresh(db_source)
        
        return db_source
    
    async def update_source(self, source_id: str, source_data: SourceUpdate) -> Optional[Source]:
        """Update an existing data source"""
        # Get existing source
        db_source = await self.get_source(source_id)
        if not db_source:
            return None
        
        # Convert Pydantic model to dict, excluding None values
        update_data = source_data.model_dump(exclude_none=True)
        
        # Update source attributes
        for key, value in update_data.items():
            setattr(db_source, key, value)
        
        # Save changes
        await self.db.commit()
        await self.db.refresh(db_source)
        
        return db_source
    
    async def delete_source(self, source_id: str) -> bool:
        """Delete a data source"""
        # Get existing source
        db_source = await self.get_source(source_id)
        if not db_source:
            return False
        
        # Delete source
        await self.db.delete(db_source)
        await self.db.commit()
        
        return True
