from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy"}


@router.get("/db")
async def db_health_check(db: AsyncSession = Depends(get_db)):
    """Database connection health check"""
    try:
        # Execute a simple query to check database connection
        result = await db.execute("SELECT 1")
        if result.scalar() == 1:
            return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
    
    return {"status": "unhealthy", "database": "unknown error"}
