import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/eventflow-ai')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # LinkedIn (optional - for future automation)
    LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL', '')
    LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD', '')
    
    # API Settings
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 8000))
    
    # Processing
    MAX_PROSPECTS_PER_CAMPAIGN = int(os.getenv('MAX_PROSPECTS', 100))
    PROCESSING_INTERVAL = int(os.getenv('PROCESSING_INTERVAL', 3600))  # 1 hour

config = Config()
