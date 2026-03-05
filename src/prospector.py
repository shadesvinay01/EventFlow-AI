"""
EventFlow AI - Prospector Module
Handles LinkedIn prospecting and lead discovery
"""

import random
from typing import Dict, List, Optional
from datetime import datetime

class Prospector:
    """
    Prospector class responsible for finding and filtering prospects.
    Integrates with LinkedIn API for real prospecting.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the prospector.
        
        Args:
            config: Configuration dictionary with API keys and settings
        """
        self.config = config or {}
        self.use_mock = not (self.config.get('linkedin_credentials', {}).get('email'))
        
        if self.use_mock:
            print("   📊 Using mock prospect data (no LinkedIn API)")
            self._load_mock_prospects()
        else:
            print("   🔗 LinkedIn API configured for real prospecting")
            self._init_linkedin_api()
    
    def _load_mock_prospects(self):
        """Load mock Indian prospect data for testing"""
        self.mock_prospects = [
            {
                "id": "P1001",
                "name": "Rahul Sharma",
                "title": "CEO",
                "company": "TechStart India",
                "industry": "SaaS",
                "location": "Mumbai",
                "email": "rahul@techstart.in",
                "phone": "+91 98765 43210",
                "company_size": "50-200",
                "revenue": "₹5Cr",
                "engagement_score": 85,
                "linkedin_url": "https://linkedin.com/in/rahulsharma",
                "pain_points": ["High customer acquisition cost", "Need better lead generation"],
                "interests": ["AI", "Growth", "Fundraising"]
            },
            {
                "id": "P1002",
                "name": "Priya Patel",
                "title": "Founder",
                "company": "AI Solutions",
                "industry": "AI/ML",
                "location": "Bangalore",
                "email": "priya@aisolutions.in",
                "phone": "+91 98765 43211",
                "company_size": "10-50",
                "revenue": "₹2Cr",
                "engagement_score": 90,
                "linkedin_url": "https://linkedin.com/in/priyapatel",
                "pain_points": ["Need more clients", "Building brand awareness"],
                "interests": ["Machine Learning", "Startups", "Venture Capital"]
            },
            {
                "id": "P1003",
                "name": "Amit Kumar",
                "title": "VP Sales",
                "company": "GrowthCorp",
                "industry": "Enterprise SaaS",
                "location": "Delhi NCR",
                "email": "amit@growthcorp.in",
                "phone": "+91 98765 43212",
                "company_size": "200-500",
                "revenue": "₹20Cr",
                "engagement_score": 75,
                "linkedin_url": "https://linkedin.com/in/amitkumar",
                "pain_points": ["Sales team missing targets", "Low conversion rates"],
                "interests": ["Sales methodology", "Team building", "Revenue growth"]
            },
            {
                "id": "P1004",
                "name": "Neha Singh",
                "title": "Director",
                "company": "InnovateLabs",
                "industry": "Technology",
                "location": "Pune",
                "email": "neha@innovatelabs.in",
                "phone": "+91 98765 43213",
                "company_size": "100-250",
                "revenue": "₹15Cr",
                "engagement_score": 80,
                "linkedin_url": "https://linkedin.com/in/nehasingh",
                "pain_points": ["Innovation stagnation", "Talent retention"],
                "interests": ["Innovation", "Leadership", "Digital transformation"]
            },
            {
                "id": "P1005",
                "name": "Vikram Reddy",
                "title": "CTO",
                "company": "CloudNative",
                "industry": "Cloud Computing",
                "location": "Hyderabad",
                "email": "vikram@cloudnative.in",
                "phone": "+91 98765 43214",
                "company_size": "50-150",
                "revenue": "₹8Cr",
                "engagement_score": 70,
                "linkedin_url": "https://linkedin.com/in/vikramreddy",
                "pain_points": ["Technical debt", "Scaling infrastructure"],
                "interests": ["Cloud architecture", "DevOps", "Kubernetes"]
            },
            {
                "id": "P1006",
                "name": "Anjali Mehta",
                "title": "Marketing Head",
                "company": "BrandBoost",
                "industry": "Marketing",
                "location": "Mumbai",
                "email": "anjali@brandboost.in",
                "phone": "+91 98765 43215",
                "company_size": "30-100",
                "revenue": "₹3Cr",
                "engagement_score": 65,
                "linkedin_url": "https://linkedin.com/in/anjalimehta",
                "pain_points": ["ROI measurement", "Lead quality issues"],
                "interests": ["Digital marketing", "Brand strategy", "Content"]
            },
            {
                "id": "P1007",
                "name": "Suresh Iyer",
                "title": "Product Manager",
                "company": "FinTech Innovations",
                "industry": "FinTech",
                "location": "Bangalore",
                "email": "suresh@fintech.in",
                "phone": "+91 98765 43216",
                "company_size": "100-300",
                "revenue": "₹12Cr",
                "engagement_score": 72,
                "linkedin_url": "https://linkedin.com/in/sureshiyer",
                "pain_points": ["Product-market fit", "User adoption"],
                "interests": ["FinTech", "Product strategy", "UX"]
            },
            {
                "id": "P1008",
                "name": "Deepa Krishnan",
                "title": "HR Director",
                "company": "PeopleFirst",
                "industry": "HR Tech",
                "location": "Chennai",
                "email": "deepa@peoplefirst.in",
                "phone": "+91 98765 43217",
                "company_size": "50-150",
                "revenue": "₹4Cr",
                "engagement_score": 68,
                "linkedin_url": "https://linkedin.com/in/deepakrishnan",
                "pain_points": ["Talent acquisition", "Employee retention"],
                "interests": ["HR tech", "Culture", "Recruitment"]
            },
            {
                "id": "P1009",
                "name": "Rajesh Gupta",
                "title": "CEO",
                "company": "WebX Solutions",
                "industry": "Technology",
                "location": "Gurgaon",
                "email": "rajesh@webx.in",
                "phone": "+91 98765 43218",
                "company_size": "20-80",
                "revenue": "₹2.5Cr",
                "engagement_score": 78,
                "linkedin_url": "https://linkedin.com/in/rajeshgupta",
                "pain_points": ["Scaling challenges", "Finding investors"],
                "interests": ["Web development", "Startups", "Growth"]
            },
            {
                "id": "P1010",
                "name": "Kavita Krishnan",
                "title": "Founder",
                "company": "DataMatic",
                "industry": "AI/ML",
                "location": "Chennai",
                "email": "kavita@datamatic.in",
                "phone": "+91 98765 43219",
                "company_size": "15-50",
                "revenue": "₹1.5Cr",
                "engagement_score": 82,
                "linkedin_url": "https://linkedin.com/in/kavitakrishnan",
                "pain_points": ["Product development", "Market validation"],
                "interests": ["Data science", "AI", "Analytics"]
            }
        ]
    
    def _init_linkedin_api(self):
        """Initialize LinkedIn API client"""
        try:
            from linkedin_api import Linkedin
            creds = self.config.get('linkedin_credentials', {})
            self.api = Linkedin(creds.get('email'), creds.get('password'))
            print("   ✅ LinkedIn API initialized")
        except ImportError:
            print("   ⚠️ linkedin-api package not installed. Using mock data.")
            self.use_mock = True
            self._load_mock_prospects()
        except Exception as e:
            print(f"   ⚠️ LinkedIn API error: {e}. Using mock data.")
            self.use_mock = True
            self._load_mock_prospects()
    
    def find_prospects(self, criteria: Dict) -> List[Dict]:
        """
        Find prospects matching given criteria.
        
        Args:
            criteria: Dictionary with filters (industry, location, titles, min_score)
        
        Returns:
            List of prospect dictionaries
        """
        if self.use_mock:
            return self._mock_search(criteria)
        else:
            return self._linkedin_search(criteria)
    
    def _mock_search(self, criteria: Dict) -> List[Dict]:
        """Search using mock data"""
        matches = []
        
        for prospect in self.mock_prospects:
            score = 0
            reasons = []
            
            # Match by industry
            if criteria.get('industry') and prospect['industry'] in criteria['industry']:
                score += 30
                reasons.append(f"Industry: {prospect['industry']}")
            
            # Match by location
            if criteria.get('location') and prospect['location'] in criteria['location']:
                score += 20
                reasons.append(f"Location: {prospect['location']}")
            
            # Match by title
            if criteria.get('titles'):
                if any(title in prospect['title'] for title in criteria['titles']):
                    score += 25
                    reasons.append(f"Title: {prospect['title']}")
            
            # Match by company size
            if criteria.get('company_size') and prospect['company_size'] in criteria['company_size']:
                score += 15
                reasons.append(f"Company size: {prospect['company_size']}")
            
            # Engagement bonus
            score += prospect['engagement_score'] * 0.1
            
            prospect['match_score'] = round(min(score, 100), 1)
            prospect['match_reasons'] = reasons
            
            if score >= criteria.get('min_score', 50):
                matches.append(prospect.copy())
        
        # Sort by match score
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        return matches
    
    def _linkedin_search(self, criteria: Dict) -> List[Dict]:
        """Real LinkedIn search"""
        prospects = []
        try:
            # Build search keywords
            keywords = " ".join(criteria.get('industry', []))
            
            # Search LinkedIn
            results = self.api.search_people(
                keywords=keywords,
                location_name=criteria.get('location', ['India'])[0],
                limit=criteria.get('limit', 50)
            )
            
            for person in results:
                profile = self.api.get_profile(person['urn_id'])
                
                prospect = {
                    'id': f"LI_{person['urn_id']}",
                    'name': f"{profile.get('firstName', '')} {profile.get('lastName', '')}",
                    'title': profile.get('headline', ''),
                    'company': profile.get('experience', [{}])[0].get('companyName', ''),
                    'location': profile.get('locationName', ''),
                    'linkedin_url': f"https://linkedin.com/in/{person['public_id']}",
                    'engagement_score': random.randint(60, 95),
                    'source': 'linkedin'
                }
                
                # Calculate match score
                score = 70  # Base score
                if any(ind in prospect['title'] for ind in criteria.get('industry', [])):
                    score += 15
                
                prospect['match_score'] = min(score, 100)
                prospects.append(prospect)
            
        except Exception as e:
            print(f"   ⚠️ LinkedIn search failed: {e}")
            prospects = self._mock_search(criteria)
        
        return prospects
    
    def enrich_prospect(self, prospect: Dict) -> Dict:
        """
        Enrich prospect data with additional information.
        
        Args:
            prospect: Basic prospect information
        
        Returns:
            Enriched prospect with company data and pain points
        """
        # In production, this would call company data APIs
        # For now, return with mock enrichment
        prospect['company_data'] = {
            'size': prospect.get('company_size', '50-200'),
            'revenue': prospect.get('revenue', '₹5Cr'),
            'recent_news': [
                'Launched new product',
                'Hiring in multiple departments',
                'Expanding to new markets'
            ]
        }
        
        # Add pain points based on role
        if 'CEO' in prospect['title'] or 'Founder' in prospect['title']:
            prospect['pain_points'] = [
                'Customer acquisition cost too high',
                'Need better lead generation',
                'Fundraising challenges'
            ]
        elif 'Sales' in prospect['title']:
            prospect['pain_points'] = [
                'Sales team missing targets',
                'Low conversion rates',
                'Need better sales training'
            ]
        elif 'Marketing' in prospect['title']:
            prospect['pain_points'] = [
                'ROI measurement unclear',
                'Lead quality issues',
                'Content not generating leads'
            ]
        elif 'CTO' in prospect['title'] or 'Technical' in prospect['title']:
            prospect['pain_points'] = [
                'Technical debt slowing development',
                'Cloud costs increasing',
                'Scaling infrastructure'
            ]
        else:
            prospect['pain_points'] = [
                'Need better event marketing',
                'Building brand awareness',
                'Finding right partners'
            ]
        
        return prospect
