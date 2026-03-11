from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from utils.db import ProspectDB
from core.prospector import LinkedInProspector
from core.researcher import DeepResearcher
from core.scorer import BANTScorer
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/ai/prospects", tags=["ai-prospects"])

class ProspectRequest(BaseModel):
    campaign_id: str
    user_id: str
    event_type: str
    target_audience: dict
    budget: Optional[float] = 50000

class ProspectResponse(BaseModel):
    id: str
    name: str
    title: str
    company: str
    industry: str
    location: str
    email: Optional[str]
    linkedinUrl: Optional[str]
    engagementScore: int
    qualification: dict

@router.post("/discover")
async def discover_prospects(request: ProspectRequest):
    """AI-powered prospect discovery"""
    try:
        # Initialize components
        prospector = LinkedInProspector()
        researcher = DeepResearcher()
        scorer = BANTScorer()
        db = ProspectDB()
        
        # Step 1: Find prospects
        logger.info(f"🔍 Discovering prospects for campaign {request.campaign_id}")
        prospects = prospector.search(
            event_type=request.event_type,
            criteria=request.target_audience,
            limit=100
        )
        
        if not prospects:
            return {"success": True, "count": 0, "message": "No prospects found"}
        
        # Step 2: Deep research each prospect
        logger.info(f"📚 Researching {len(prospects)} prospects")
        for prospect in prospects:
            research = researcher.analyze(
                company=prospect.get('company'),
                industry=prospect.get('industry')
            )
            prospect['research'] = research
        
        # Step 3: Score prospects
        logger.info(f"⭐ Scoring prospects with BANT")
        for prospect in prospects:
            score, qualification = scorer.evaluate(
                prospect=prospect,
                budget=request.budget,
                event_type=request.event_type
            )
            prospect['engagementScore'] = score
            prospect['qualification'] = qualification
        
        # Step 4: Save to MongoDB
        saved_ids = db.save_prospects(
            prospects=prospects,
            campaign_id=request.campaign_id,
            user_id=request.user_id
        )
        
        logger.info(f"✅ Saved {len(saved_ids)} prospects to database")
        
        return {
            "success": True,
            "count": len(saved_ids),
            "prospects": prospects[:5]  # Return first 5 as sample
        }
        
    except Exception as e:
        logger.error(f"❌ Prospect discovery failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/campaign/{campaign_id}")
async def get_campaign_prospects(campaign_id: str):
    """Get AI-discovered prospects for campaign"""
    db = ProspectDB()
    prospects = list(db.collection.find({'campaign': campaign_id}))
    
    # Convert ObjectId to string
    for p in prospects:
        p['_id'] = str(p['_id'])
    
    return {"success": True, "count": len(prospects), "prospects": prospects}
