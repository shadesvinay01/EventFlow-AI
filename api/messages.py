from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from utils.db import MessageDB, ProspectDB
from core.generator import MessageGenerator
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/ai/messages", tags=["ai-messages"])

class MessageRequest(BaseModel):
    campaign_id: str
    user_id: str
    prospect_ids: List[str]
    message_type: str = "linkedin"  # linkedin, email, whatsapp

class MessageResponse(BaseModel):
    id: str
    prospect_id: str
    content: str
    channel: str
    personalization_score: int

@router.post("/generate")
async def generate_messages(request: MessageRequest):
    """Generate AI-personalized messages for prospects"""
    try:
        generator = MessageGenerator()
        prospect_db = ProspectDB()
        message_db = MessageDB()
        
        messages = []
        
        for prospect_id in request.prospect_ids[:10]:  # Limit to 10 at a time
            # Get prospect from DB
            prospect = prospect_db.collection.find_one({'_id': prospect_id})
            if not prospect:
                continue
            
            # Generate personalized message
            message_content = generator.create_message(
                prospect=prospect,
                channel=request.message_type,
                personalization_level="high"
            )
            
            # Create message record
            message = {
                'prospect': prospect_id,
                'campaign': request.campaign_id,
                'user': request.user_id,
                'content': message_content,
                'channel': request.message_type,
                'status': 'draft',
                'personalization_score': 95  # Example score
            }
            messages.append(message)
        
        # Save to MongoDB
        if messages:
            saved_ids = message_db.save_messages(
                messages=messages,
                campaign_id=request.campaign_id,
                user_id=request.user_id
            )
            
            logger.info(f"✅ Generated {len(saved_ids)} personalized messages")
            
            return {
                "success": True,
                "count": len(saved_ids),
                "messages": messages[:3]  # Return first 3 as sample
            }
        else:
            return {"success": True, "count": 0, "message": "No messages generated"}
            
    except Exception as e:
        logger.error(f"❌ Message generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
