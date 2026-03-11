#!/usr/bin/env python3
"""
EventFlow-AI Main Entry Point
Runs both API server and background processor
"""

import asyncio
import uvicorn
import threading
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import prospects, messages
from scheduler.processor import CampaignProcessor
from utils.config import config
from utils.db import MongoDB

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="EventFlow-AI API",
    description="AI-powered prospecting and messaging for event organizers",
    version="1.0.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(prospects.router)
app.include_router(messages.router)

@app.on_event("startup")
async def startup_event():
    """Start background processor on startup"""
    logger.info("🚀 Starting EventFlow-AI services...")
    
    # Test MongoDB connection
    MongoDB()
    
    # Start background processor in separate thread
    def run_processor():
        asyncio.run(CampaignProcessor().run())
    
    processor_thread = threading.Thread(target=run_processor, daemon=True)
    processor_thread.start()
    
    logger.info("✅ EventFlow-AI is ready!")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean shutdown"""
    logger.info("👋 Shutting down EventFlow-AI...")
    MongoDB().close()

@app.get("/")
async def root():
    return {
        "service": "EventFlow-AI",
        "version": "1.0.0",
        "status": "operational",
        "features": ["prospecting", "research", "messaging", "scoring"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": asyncio.get_event_loop().time()}

if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True
    )
