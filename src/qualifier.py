"""
EventFlow AI - Lead Qualifier Module
Implements BANT framework for lead qualification
"""

import random
from typing import Dict, List, Optional

class Qualifier:
    """
    Qualifies leads using BANT (Budget, Authority, Need, Timeline) framework.
    Provides scoring and next-step recommendations.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the qualifier.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.qualified_leads = 0
        self.conversions = 0
        print("   ⭐ Lead qualifier ready")
    
    def qualify(self, prospect: Dict) -> Dict:
        """
        Qualify a lead using BANT framework.
        
        Args:
            prospect: Prospect dictionary with engagement_score, title, revenue, etc.
        
        Returns:
            Qualification result with scores and recommendations
        """
        # Calculate BANT scores
        bant = self._calculate_bant(prospect)
        overall_score = sum(bant.values()) / 4
        
        # Determine status and next actions
        result = self._determine_status(overall_score, prospect)
        result['bant_scores'] = bant
        
        self.qualified_leads += 1
        if result['status'] == 'HOT':
            self.conversions += 1
        
        return result
    
    def _calculate_bant(self, prospect: Dict) -> Dict:
        """Calculate individual BANT scores"""
        
        bant = {
            "Budget": 0,
            "Authority": 0,
            "Need": 0,
            "Timeline": 0
        }
        
        # Budget score based on company revenue
        revenue_str = prospect.get('revenue', '₹0')
        try:
            revenue_val = float(revenue_str.replace('₹', '').replace('Cr', ''))
            if revenue_val >= 10:
                bant["Budget"] = random.randint(85, 100)
            elif revenue_val >= 5:
                bant["Budget"] = random.randint(70, 90)
            elif revenue_val >= 2:
                bant["Budget"] = random.randint(50, 75)
            else:
                bant["Budget"] = random.randint(30, 55)
        except:
            bant["Budget"] = random.randint(50, 80)
        
        # Authority based on title
        title = prospect.get('title', '')
        if any(t in title for t in ['CEO', 'Founder', 'CTO', 'Owner', 'Director']):
            bant["Authority"] = random.randint(85, 100)
        elif any(t in title for t in ['VP', 'Head', 'Senior']):
            bant["Authority"] = random.randint(70, 90)
        elif any(t in title for t in ['Manager', 'Lead']):
            bant["Authority"] = random.randint(50, 75)
        else:
            bant["Authority"] = random.randint(30, 55)
        
        # Need based on engagement score and pain points
        engagement = prospect.get('engagement_score', 50)
        has_pain_points = len(prospect.get('pain_points', [])) > 0
        
        need_base = engagement
        if has_pain_points:
            need_base += 15
        
        bant["Need"] = random.randint(
            max(50, need_base - 10),
            min(100, need_base + 10)
        )
        
        # Timeline based on engagement and role
        if engagement > 80:
            bant["Timeline"] = random.randint(75, 95)
        elif engagement > 60:
            bant["Timeline"] = random.randint(50, 80)
        else:
            bant["Timeline"] = random.randint(30, 60)
        
        # Adjust timeline for decision-makers
        if bant["Authority"] > 80:
            bant["Timeline"] = min(100, bant["Timeline"] + 10)
        
        return bant
    
    def _determine_status(self, score: float, prospect: Dict) -> Dict:
        """
        Determine lead status based on overall score.
        
        Args:
            score: Overall BANT score
            prospect: Prospect information
        
        Returns:
            Dictionary with status and next actions
        """
        
        if score >= 80:
            return {
                "name": prospect.get('name', ''),
                "title": prospect.get('title', ''),
                "company": prospect.get('company', ''),
                "overall_score": round(score, 1),
                "status": "HOT",
                "status_emoji": "🔥",
                "next_action": "Send payment link & schedule call",
                "probability": "85-95%",
                "priority": 1,
                "followup_days": 1
            }
        elif score >= 65:
            return {
                "name": prospect.get('name', ''),
                "title": prospect.get('title', ''),
                "company": prospect.get('company', ''),
                "overall_score": round(score, 1),
                "status": "WARM",
                "status_emoji": "⭐",
                "next_action": "Schedule follow-up in 3 days",
                "probability": "50-70%",
                "priority": 2,
                "followup_days": 3
            }
        elif score >= 50:
            return {
                "name": prospect.get('name', ''),
                "title": prospect.get('title', ''),
                "company": prospect.get('company', ''),
                "overall_score": round(score, 1),
                "status": "COOL",
                "status_emoji": "🌱",
                "next_action": "Add to nurture sequence",
                "probability": "20-40%",
                "priority": 3,
                "followup_days": 7
            }
        else:
            return {
                "name": prospect.get('name', ''),
                "title": prospect.get('title', ''),
                "company": prospect.get('company', ''),
                "overall_score": round(score, 1),
                "status": "COLD",
                "status_emoji": "❄️",
                "next_action": "Newsletter & long-term nurture",
                "probability": "<10%",
                "priority": 4,
                "followup_days": 30
            }
    
    def batch_qualify(self, prospects: List[Dict]) -> List[Dict]:
        """
        Qualify multiple prospects at once.
        
        Args:
            prospects: List of prospect dictionaries
        
        Returns:
            List of qualification results
        """
        results = []
        for prospect in prospects:
            results.append(self.qualify(prospect))
        
        # Sort by score descending
        results.sort(key=lambda x: x['overall_score'], reverse=True)
        return results
    
    def get_recommendations(self, prospect: Dict) -> List[str]:
        """
        Get personalized recommendations for a prospect.
        
        Args:
            prospect: Prospect information
        
        Returns:
            List of recommendation strings
        """
        recommendations = []
        qualification = self.qualify(prospect)
        
        if qualification['status'] == 'HOT':
            recommendations.extend([
                "Send personalized payment link immediately",
                "Offer early bird discount",
                "Share speaker lineup and agenda",
                "Schedule a 15-min call to address questions"
            ])
        elif qualification['status'] == 'WARM':
            recommendations.extend([
                "Send case studies from similar companies",
                "Share testimonials from past attendees",
                "Offer to connect with current attendees",
                "Schedule follow-up in 3 days"
            ])
        elif qualification['status'] == 'COOL':
            recommendations.extend([
                "Add to email nurture sequence",
                "Share blog posts and valuable content",
                "Invite to free webinar",
                "Re-engage in 2 weeks"
            ])
        else:
            recommendations.extend([
                "Add to monthly newsletter",
                "Connect on LinkedIn",
                "Share occasional updates",
                "Re-evaluate in 3 months"
            ])
        
        return recommendations
    
    def get_stats(self) -> Dict:
        """Get qualification statistics"""
        return {
            'qualified_leads': self.qualified_leads,
            'conversions': self.conversions,
            'conversion_rate': (self.conversions / self.qualified_leads * 100) if self.qualified_leads > 0 else 0
        }
