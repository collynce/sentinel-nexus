from fastapi import APIRouter

from app.api.v1.endpoints import health, threats, sources, analysis, actions, copilot

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(threats.router, prefix="/threats", tags=["threats"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(actions.router, prefix="/actions", tags=["actions"])
api_router.include_router(copilot.router, prefix="/copilot", tags=["copilot"])
