"""
Basic example of using EventFlow AI
"""

from src.eventflow_ai import EventFlowAI

def main():
    # Initialize AI agent
    ai = EventFlowAI()
    
    # Define event
    event = {
        "name": "AI & SaaS Summit 2024",
        "price": 4999,
        "date": "15-16 June 2024"
    }
    
    # Run campaign
    results = ai.run_campaign("conference")
    
    # Print results
    print(f"\n📊 Campaign Results:")
    print(f"   Prospects Found: {results['prospects_found']}")
    print(f"   Qualified Leads: {len(results['qualified_leads'])}")
    print(f"   Top Leads: {', '.join(results['qualified_leads'][:3])}")

if __name__ == "__main__":
    main()
