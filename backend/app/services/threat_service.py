from typing import List, Optional, Dict, Any
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.threat import Threat
from app.schemas.threat import ThreatCreate, ThreatUpdate


class ThreatService:
    """Service for managing threat intelligence data"""
    
    def __init__(self, db: AsyncSession):
        """Initialize with database session"""
        self.db = db
    
    async def get_threats(
        self, 
        skip: int = 0, 
        limit: int = 100,
        severity: Optional[str] = None,
        source_type: Optional[str] = None,
    ) -> List[Threat]:
        """Get list of threats with optional filtering"""
        query = select(Threat).offset(skip).limit(limit)
        
        # Apply filters if provided
        if severity:
            query = query.filter(Threat.severity == severity)
        
        if source_type:
            # This would need to join with the source table
            # For simplicity, we're not implementing this filter yet
            pass
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_threat(self, threat_id: str) -> Optional[Threat]:
        """Get a specific threat by ID"""
        query = select(Threat).filter(Threat.id == threat_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def create_threat(self, threat_data: ThreatCreate) -> Threat:
        """Create a new threat"""
        # Convert Pydantic model to dict, excluding None values
        threat_dict = threat_data.model_dump(exclude_none=True)
        
        # Create new threat object
        db_threat = Threat(**threat_dict)
        
        # Add to database
        self.db.add(db_threat)
        await self.db.commit()
        await self.db.refresh(db_threat)
        
        return db_threat
    
    async def update_threat(self, threat_id: str, threat_data: ThreatUpdate) -> Optional[Threat]:
        """Update an existing threat"""
        # Get existing threat
        db_threat = await self.get_threat(threat_id)
        if not db_threat:
            return None
        
        # Convert Pydantic model to dict, excluding None values
        update_data = threat_data.model_dump(exclude_none=True)
        
        # Update threat attributes
        for key, value in update_data.items():
            setattr(db_threat, key, value)
        
        # Save changes
        await self.db.commit()
        await self.db.refresh(db_threat)
        
        return db_threat
    
    async def delete_threat(self, threat_id: str) -> bool:
        """Delete a threat"""
        # Get existing threat
        db_threat = await self.get_threat(threat_id)
        if not db_threat:
            return False
        
        # Delete threat
        await self.db.delete(db_threat)
        await self.db.commit()
        
        return True
