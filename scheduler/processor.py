import asyncio
import logging
from datetime import datetime
from utils.db import CampaignDB, ProspectDB, MessageDB
from core.prospector import LinkedInProspector
from core.researcher import DeepResearcher
from core.generator import MessageGenerator
from core.scorer import BANTScorer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CampaignProcessor:
    def __init__(self):
        self.campaign_db = CampaignDB()
        self.prospect_db = ProspectDB()
        self.message_db = MessageDB()
        
        self.prospector = LinkedInProspector()
        self.researcher = DeepResearcher()
        self.generator = MessageGenerator()
        self.scorer = BANTScorer()
    
    async def process_campaign(self, campaign):
        """Process a single campaign with AI"""
        campaign_id = campaign['_id']
        user_id = campaign['user']
        
        logger.info(f"🚀 Processing campaign: {campaign.get('name')} ({campaign_id})")
        
        try:
            # Step 1: Discover prospects
            prospects = self.prospector.search(
                event_type=campaign.get('eventType'),
                criteria=campaign.get('targetAudience', {}),
                limit=100
            )
            
            if not prospects:
                logger.warning(f"⚠️ No prospects found for campaign {campaign_id}")
                self.campaign_db.mark_processed(campaign_id)
                return
            
            # Step 2: Research each prospect
            for prospect in prospects:
                research = self.researcher.analyze(
                    company=prospect.get('company'),
                    industry=prospect.get('industry')
                )
                prospect['research'] = research
            
            # Step 3: Score prospects
            for prospect in prospects:
                score, qualification = self.scorer.evaluate(
                    prospect=prospect,
                    budget=campaign.get('budget', 50000),
                    event_type=campaign.get('eventType')
                )
                prospect['engagementScore'] = score
                prospect['qualification'] = qualification
            
            # Step 4: Save prospects to DB
            saved_ids = self.prospect_db.save_prospects(
                prospects=prospects,
                campaign_id=campaign_id,
                user_id=user_id
            )
            
            logger.info(f"✅ Saved {len(saved_ids)} prospects")
            
            # Step 5: Generate messages for top prospects
            top_prospects = prospects[:20]  # Top 20 prospects
            messages = []
            
            for prospect in top_prospects:
                if prospect.get('engagementScore', 0) > 70:  # Only HOT leads
                    msg = self.generator.create_message(
                        prospect=prospect,
                        channel='linkedin',
                        personalization_level='high'
                    )
                    messages.append({
                        'prospect': prospect.get('_id'),
                        'campaign': campaign_id,
                        'user': user_id,
                        'content': msg,
                        'channel': 'linkedin',
                        'status': 'draft'
                    })
            
            # Step 6: Save messages
            if messages:
                self.message_db.save_messages(messages, campaign_id, user_id)
                logger.info(f"✅ Generated {len(messages)} messages")
            
            # Step 7: Update campaign
            self.campaign_db.update_campaign(campaign_id, {
                'ai_processed': True,
                'prospects_found': len(prospects),
                'hot_leads': len([p for p in prospects if p.get('engagementScore', 0) > 70]),
                'messages_generated': len(messages)
            })
            
            logger.info(f"✅ Campaign {campaign_id} processed successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to process campaign {campaign_id}: {e}")
            self.campaign_db.update_campaign(campaign_id, {
                'ai_error': str(e),
                'ai_processed': False
            })
    
    async def run(self):
        """Main processor loop"""
        logger.info("🔄 Starting AI campaign processor...")
        
        while True:
            try:
                # Get pending campaigns
                campaigns = self.campaign_db.get_pending_campaigns()
                
                if campaigns:
                    logger.info(f"📊 Found {len(campaigns)} campaigns to process")
                    
                    # Process each campaign
                    for campaign in campaigns:
                        await self.process_campaign(campaign)
                        await asyncio.sleep(5)  # Rate limiting
                else:
                    logger.info("⏳ No pending campaigns, sleeping...")
                
                # Wait before next check
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"❌ Processor error: {e}")
                await asyncio.sleep(60)

# Run processor
if __name__ == "__main__":
    processor = CampaignProcessor()
    asyncio.run(processor.run())
