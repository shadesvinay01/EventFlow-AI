import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDB:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connect()
        return cls._instance
    
    def _connect(self):
        """Connect to MongoDB Atlas"""
        try:
            self.client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017'))
            self.db = self.client['eventflow-ai']
            logger.info("✅ Connected to MongoDB")
        except Exception as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            raise
    
    def get_collection(self, name):
        """Get MongoDB collection"""
        return self.db[name]
    
    def close(self):
        """Close MongoDB connection"""
        self.client.close()

# Campaign operations
class CampaignDB:
    def __init__(self):
        self.db = MongoDB()
        self.collection = self.db.get_collection('campaigns')
    
    def get_pending_campaigns(self):
        """Get campaigns that need AI processing"""
        return list(self.collection.find({
            'status': {'$in': ['draft', 'active']},
            'ai_processed': {'$ne': True}
        }).limit(10))
    
    def update_campaign(self, campaign_id, data):
        """Update campaign with AI results"""
        self.collection.update_one(
            {'_id': campaign_id},
            {'$set': {**data, 'ai_processed': True, 'processed_at': datetime.now()}}
        )
    
    def mark_processed(self, campaign_id):
        """Mark campaign as processed"""
        self.collection.update_one(
            {'_id': campaign_id},
            {'$set': {'ai_processed': True, 'processed_at': datetime.now()}}
        )

# Prospect operations
class ProspectDB:
    def __init__(self):
        self.db = MongoDB()
        self.collection = self.db.get_collection('prospects')
    
    def save_prospects(self, prospects, campaign_id, user_id):
        """Save multiple prospects from AI"""
        if not prospects:
            return []
        
        for prospect in prospects:
            prospect['campaign'] = campaign_id
            prospect['user'] = user_id
            prospect['createdAt'] = datetime.now()
            prospect['updatedAt'] = datetime.now()
            prospect['source'] = 'ai_discovered'
            prospect['engagementScore'] = prospect.get('engagementScore', 50)
        
        result = self.collection.insert_many(prospects)
        return result.inserted_ids
    
    def update_prospect_score(self, prospect_id, score, qualification):
        """Update prospect with BANT score"""
        self.collection.update_one(
            {'_id': prospect_id},
            {'$set': {
                'engagementScore': score,
                'qualification': qualification,
                'updatedAt': datetime.now()
            }}
        )

# Message operations
class MessageDB:
    def __init__(self):
        self.db = MongoDB()
        self.collection = self.db.get_collection('messages')
    
    def save_messages(self, messages, campaign_id, user_id):
        """Save AI-generated messages"""
        if not messages:
            return []
        
        for msg in messages:
            msg['campaign'] = campaign_id
            msg['user'] = user_id
            msg['createdAt'] = datetime.now()
            msg['updatedAt'] = datetime.now()
            msg['status'] = 'draft'
        
        result = self.collection.insert_many(messages)
        return result.inserted_ids
