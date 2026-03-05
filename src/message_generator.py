"""
EventFlow AI - Message Generator Module
Creates personalized outreach messages for prospects
"""

import random
from typing import Dict, List, Optional
import json

class MessageGenerator:
    """
    Generates personalized outreach messages based on prospect data.
    Can use templates or GPT-4 for dynamic generation.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the message generator.
        
        Args:
            config: Configuration dictionary with API settings
        """
        self.config = config or {}
        self.use_openai = bool(self.config.get('openai_key'))
        self.templates_used = 0
        
        if self.use_openai:
            self._init_openai()
            print("   ✨ Using OpenAI for dynamic message generation")
        else:
            print("   📝 Using template-based messages")
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            import openai
            openai.api_key = self.config['openai_key']
            self.openai = openai
            print("   ✅ OpenAI initialized")
        except ImportError:
            print("   ⚠️ OpenAI package not installed. Using templates.")
            self.use_openai = False
    
    def generate(self, prospect: Dict, event_type: str) -> str:
        """
        Generate personalized message for a prospect.
        
        Args:
            prospect: Prospect dictionary with name, title, company, etc.
            event_type: Type of event (conference, workshop, etc.)
        
        Returns:
            Personalized message string
        """
        self.templates_used += 1
        
        # Get event details from config
        from .config import EVENTS
        event = EVENTS.get(event_type, EVENTS['conference'])
        
        if self.use_openai:
            return self._generate_ai_message(prospect, event)
        else:
            return self._generate_template_message(prospect, event)
    
    def _generate_ai_message(self, prospect: Dict, event: Dict) -> str:
        """Generate message using OpenAI GPT"""
        try:
            prompt = f"""
            Write a professional, personalized sales email to a business prospect.

            PROSPECT DETAILS:
            - Name: {prospect.get('name', 'there')}
            - Title: {prospect.get('title', 'Professional')}
            - Company: {prospect.get('company', 'their company')}
            - Industry: {prospect.get('industry', 'business')}
            - Pain Points: {', '.join(prospect.get('pain_points', ['business challenges']))[:200]}

            EVENT DETAILS:
            - Name: {event.get('name', 'our event')}
            - Date: {event.get('date', 'coming soon')}
            - Venue: {event.get('venue', 'location')}
            - Speakers: {', '.join(event.get('speakers', ['industry leaders']))[:200]}
            - Price: ₹{event.get('price', 0):,}

            RULES:
            1. Start with a personalized hook mentioning their role
            2. Reference their industry/pain points
            3. Connect event value to their challenges
            4. Include speaker names as social proof
            5. Clear, low-pressure call to action
            6. Professional but warm tone
            7. Max 200 words

            Write the email:
            """
            
            response = self.openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert B2B sales email writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"   ⚠️ OpenAI error: {e}. Using template.")
            return self._generate_template_message(prospect, event)
    
    def _generate_template_message(self, prospect: Dict, event: Dict) -> str:
        """Generate message using templates"""
        
        # Personalization elements
        name = prospect.get('name', 'there')
        title = prospect.get('title', 'leader')
        company = prospect.get('company', 'your company')
        industry = prospect.get('industry', 'business')
        pain_point = random.choice(prospect.get('pain_points', ['growth challenges']))
        
        speaker1 = event.get('speakers', ['industry leaders'])[0]
        speaker2 = event.get('speakers', ['successful founders'])[1] if len(event.get('speakers', [])) > 1 else 'successful founders'
        
        templates = [
            f"""Hi {name} 👋,

I noticed you're the {title} at {company} and your work in {industry} is impressive.

Given your focus on {industry}, I thought you'd be interested in our upcoming {event['name']} on {event['date']} at {event['venue']}.

We have amazing speakers like {speaker1} and {speaker2} sharing insights on challenges like:
• {pain_point}

Would you be open to learning more? I can share the complete agenda.

Ticket price: ₹{event['price']:,} (Early bird: ₹{event['early_bird']:,})

Best regards,
EventFlow AI Team""",

            f"""Hello {name},

I've been following {company}'s journey in the {industry} space, and I'm impressed by your growth.

As a {title}, you're probably dealing with {pain_point}. Our {event['name']} on {event['date']} brings together leaders who've solved exactly these challenges.

The event features:
• {speaker1} - sharing proven frameworks
• {speaker2} - insights on scaling
• 50+ industry leaders for networking

Early bird tickets at ₹{event['early_bird']:,} (Regular: ₹{event['price']:,})

Worth a 5-minute chat?

Thanks,
EventFlow AI""",

            f"""Hi {name},

I saw that {company} is doing amazing work in {industry} and thought you might be interested in our upcoming event.

At {event['name']} on {event['date']}, we're bringing together {industry} leaders to tackle challenges like:
• {pain_point}
• Scaling challenges
• Growth strategies

With speakers like {speaker1} and {speaker2}, it's going to be incredibly valuable.

Would you like to see if this aligns with your goals?

Ticket info: ₹{event['price']:,} (Early bird: ₹{event['early_bird']:,})

Cheers,
EventFlow AI"""
        ]
        
        return random.choice(templates)
    
    def generate_followup(self, prospect: Dict, event: Dict, 
                          previous_message: str, days_since: int) -> str:
        """
        Generate follow-up message.
        
        Args:
            prospect: Prospect information
            event: Event details
            previous_message: Previous message sent
            days_since: Days since last contact
        
        Returns:
            Follow-up message
        """
        templates = [
            f"""Hi {prospect['name']} 👋,

Just checking if you saw my previous email about {event['name']}.

We still have early bird tickets available at ₹{event['early_bird']:,} and I'd love to have you join us.

Would you like me to send the full agenda?

Best regards,
EventFlow AI""",

            f"""Hi {prospect['name']},

Following up on my previous email - wanted to make sure you didn't miss this opportunity.

{event['name']} is just {event['date']} away and we have some amazing speakers lined up including {event['speakers'][0]}.

Early bird pricing ends soon at ₹{event['early_bird']:,}.

Let me know if you have any questions!

Thanks,
EventFlow AI""",

            f"""Hi {prospect['name']},

Last chance for early bird tickets to {event['name']}! 

With speakers like {event['speakers'][0]} and {event['speakers'][1]}, this is going to be an incredible event for {prospect['industry']} leaders.

Secure your spot now at ₹{event['early_bird']:,} before prices go up.

Hope to see you there!

Cheers,
EventFlow AI"""
        ]
        
        return random.choice(templates)
    
    def get_stats(self) -> Dict:
        """Get message generation statistics"""
        return {
            'templates_used': self.templates_used,
            'using_openai': self.use_openai
        }
