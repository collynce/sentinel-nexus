from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.action import FirewallAction, WebhookAction, ActionResult

router = APIRouter()


@router.post("/firewall", response_model=ActionResult)
async def block_threat_firewall(action: FirewallAction, db: AsyncSession = Depends(get_db)):
    """Block a threat via firewall API integration"""
    # TODO: Implement firewall action integration
    raise HTTPException(status_code=501, detail="Firewall action integration not implemented yet.")


@router.post("/webhook", response_model=ActionResult)
async def send_webhook_alert(action: WebhookAction, db: AsyncSession = Depends(get_db)):
    """Send an alert to a webhook (e.g., Slack)"""
    # TODO: Implement webhook alert integration
    raise HTTPException(status_code=501, detail="Webhook alert integration not implemented yet.")


@router.get("/playbooks")
async def get_playbooks():
    """Get available response playbooks"""
    # This would come from a database in a real implementation
    return [
        {
            "id": "block-ip",
            "name": "Block Malicious IP",
            "description": "Blocks a malicious IP address in the firewall",
            "actions": ["firewall"],
        },
        {
            "id": "alert-team",
            "name": "Alert Security Team",
            "description": "Sends an alert to the security team via Slack",
            "actions": ["webhook"],
        },
        {
            "id": "full-response",
            "name": "Full Response Workflow",
            "description": "Blocks the threat and alerts the team",
            "actions": ["firewall", "webhook"],
        },
    ]


@router.post("/execute-playbook/{playbook_id}", response_model=ActionResult)
async def execute_playbook(playbook_id: str, threat_id: str, db: AsyncSession = Depends(get_db)):
    """Execute a response playbook for a specific threat"""
    action_service = ActionService(db)
    result = await action_service.execute_playbook(playbook_id, threat_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Playbook with ID {playbook_id} not found or threat with ID {threat_id} not found",
        )
    return result
