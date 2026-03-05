"""
EventFlow AI - Configuration Module
Centralized configuration and constants
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Events Catalog
EVENTS = {
    "conference": {
        "name": "AI & SaaS Growth Summit 2024",
        "price": 4999,
        "early_bird": 3999,
        "date": "15-16 June 2024",
        "venue": "Mumbai Convention Center, Bandra Kurla Complex",
        "capacity": 1000,
        "speakers": [
            "Kunal Shah - CRED Founder",
            "Girish Mathrubootham - Freshworks CEO",
            "Nithin Kamath - Zerodha Founder",
            "Falguni Nayar - Nykaa Founder"
        ],
        "topics": [
            "Scaling SaaS in India",
            "AI-powered growth strategies",
            "Fundraising in 2024",
            "Building unicorn culture"
        ],
        "target_industries": ["SaaS", "AI/ML", "Technology", "FinTech"],
        "value_prop": "India's biggest SaaS & AI conference with 50+ successful founders sharing actionable insights"
    },
    "workshop": {
        "name": "Growth Hacking Masterclass",
        "price": 9999,
        "early_bird": 7999,
        "date": "22-23 June 2024",
        "venue": "Bangalore International Tech Park",
        "capacity": 200,
        "speakers": [
            "Anand Rajaraman - Walmart Labs",
            "Kunal Shah - CRED",
            "Tanmay Bhat - Content creator"
        ],
        "topics": [
            "Viral marketing strategies",
            "Conversion rate optimization",
            "Retention hacks",
            "Referral programs"
        ],
        "target_industries": ["SaaS", "Technology", "Marketing", "E-commerce"],
        "value_prop": "Hands-on workshop: Double your revenue in 90 days using proven growth frameworks"
    },
    "mastermind": {
        "name": "CEO Peer Group (12-Month Program)",
        "price": 49999,
        "early_bird": 44999,
        "date": "Starts July 2024 (Monthly for 12 months)",
        "venue": "Multiple cities (Mumbai, Bangalore, Delhi)",
        "capacity": 50,
        "speakers": [
            "Deep Kalra - MakeMyTrip Founder",
            "Bhavish Aggarwal - Ola Founder",
            "Ritesh Agarwal - OYO Founder"
        ],
        "topics": [
            "Quarterly strategy sessions",
            "1:1 mentoring",
            "Peer problem solving",
            "Investor connections"
        ],
        "target_industries": ["SaaS", "Enterprise SaaS", "FinTech"],
        "value_prop": "Exclusive 12-month program for founders scaling from ₹10Cr to ₹100Cr revenue"
    },
    "networking": {
        "name": "Startup Founders Connect",
        "price": 999,
        "early_bird": 699,
        "date": "5 June 2024",
        "venue": "Delhi NCR (Cyber Hub, Gurgaon)",
        "capacity": 300,
        "speakers": [
            "Local founders & VCs",
            "Industry experts"
        ],
        "topics": [
            "Speed networking",
            "Investor meet & greet",
            "Founder stories",
            "Partnership opportunities"
        ],
        "target_industries": ["SaaS", "Technology", "FinTech", "Marketing", "E-commerce"],
        "value_prop": "Connect with 200+ founders, investors, and mentors in an evening of meaningful conversations"
    },
    "ai_workshop": {
        "name": "AI Implementation for Business Leaders",
        "price": 14999,
        "early_bird": 11999,
        "date": "10-11 July 2024",
        "venue": "Hyderabad HITEC City",
        "capacity": 150,
        "speakers": [
            "AI researchers from IITs",
            "Startup CTOs",
            "Industry practitioners"
        ],
        "topics": [
            "AI strategy for your business",
            "Implementation roadmap",
            "Cost vs ROI analysis",
            "Case studies"
        ],
        "target_industries": ["AI/ML", "Technology", "SaaS", "FinTech"],
        "value_prop": "Learn how to implement AI in your business without wasting crores on failed experiments"
    }
}

# API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL', '')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD', '')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
RAZORPAY_KEY = os.getenv('RAZORPAY_KEY', '')
RAZORPAY_SECRET = os.getenv('RAZORPAY_SECRET', '')

# Pricing Plans
PRICING = {
    "starter": {
        "price": 9999,
        "prospects": 500,
        "features": ["Basic prospecting", "Email outreach", "Basic analytics"]
    },
    "pro": {
        "price": 24999,
        "prospects": 2000,
        "features": ["AI personalization", "Multi-channel", "Revenue tracking", "Priority support"]
    },
    "enterprise": {
        "price": "Custom",
        "prospects": "Unlimited",
        "features": ["API access", "Dedicated manager", "Custom integration", "White-label"]
    }
}

# Campaign Defaults
CAMPAIGN_DEFAULTS = {
    "min_score": 60,
    "max_prospects": 100,
    "followup_days": [1, 3, 7, 14],
    "budget": 50000
}
