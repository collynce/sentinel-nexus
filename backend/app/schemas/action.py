from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, HttpUrl

from app.schemas.base import BaseSchema


class ActionBase(BaseModel):
    """Base schema for security actions"""
    threat_id: str = Field(..., description="ID of the threat to take action on")
    description: Optional[str] = None


class FirewallAction(ActionBase):
    """Schema for firewall blocking actions"""
    action_type: str = "block"
    target_type: str = Field(..., description="Type of entity to block (ip, domain, url)")
    target_value: str = Field(..., description="Value to block")
    duration: Optional[str] = Field("permanent", description="Duration of the block (e.g., '24h', 'permanent')")
    firewall_type: Optional[str] = None


class WebhookAction(ActionBase):
    """Schema for webhook notification actions"""
    webhook_url: HttpUrl = Field(..., description="URL to send the webhook to")
    service_type: str = Field("slack", description="Type of service (slack, teams, generic)")
    message: str = Field(..., description="Message to include in the notification")
    severity: str = Field("medium", description="Severity of the alert (low, medium, high, critical)")
    additional_data: Optional[Dict[str, Any]] = None


class ActionResult(BaseModel):
    """Schema for action result response"""
    action_id: str
    status: str
    message: str
    details: Optional[Dict[str, Any]] = None
