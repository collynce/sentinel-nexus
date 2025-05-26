from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging

router = APIRouter(prefix="/api/copilot", tags=["copilot"])

class Message(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    messages: List[Message]
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    response: Message
    context: Optional[dict] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_with_copilot(request: ChatRequest):
    """
    Main endpoint for SOC Co-Pilot chat functionality.
    Processes user messages and returns AI-generated responses.
    """
    try:
        # TODO: Integrate with actual AI model (OpenRouter via LiteLLM)
        # For now, we'll use a simple response generator
        user_message = request.messages[-1].content.lower()
        
        # Simple response generation (to be replaced with AI model)
        response_content = generate_response(user_message, request.context or {})
        
        return ChatResponse(
            response=Message(
                role="assistant",
                content=response_content,
                timestamp=datetime.utcnow()
            ),
            context=request.context
        )
    except Exception as e:
        logging.error(f"Error in copilot chat: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing your request")

def generate_response(message: str, context: dict) -> str:
    """Generate a response based on the user's message and context."""
    # This is a simple rule-based response generator
    # In a production environment, this would call an AI model
    
    if any(word in message for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm your SOC Co-Pilot. How can I assist you with threat intelligence today?"
    
    if 'threat' in message and 'recent' in message:
        return "Here are the recent threats we've detected:\n\n" \
               "1. **Phishing Campaign** - Active in healthcare sector\n" \
               "2. **Ransomware Activity** - Targeting unpatched VPNs\n" \
               "3. **Credential Stuffing** - Multiple login attempts detected"
    
    if 'help' in message:
        return "I can help you with:\n\n" \
               "- Threat analysis and investigation\n" \
               "- Security recommendations\n" \
               "- Incident response guidance\n" \
               "- Threat intelligence reports\n\n" \
               "What would you like to know more about?"
    
    return "I'm here to help with your security operations. Could you please provide more details about what you're looking for?"
