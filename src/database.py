"""
EventFlow AI - Database Module
SQLite database handler for storing prospects, campaigns, and messages
"""

import sqlite3
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

class Database:
    """
    SQLite database handler for EventFlow AI.
    Manages all data persistence including prospects, campaigns, and messages.
    """
    
    def __init__(self, db_path: str = "eventflow.db"):
        """
        Initialize database connection and create tables.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
        print(f"✅ Database initialized: {db_path}")
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise
    
    def create_tables(self):
        """Create all necessary tables if they don't exist"""
        try:
            # Prospects table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS prospects (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    title TEXT,
                    company TEXT,
                    industry TEXT,
                    location TEXT,
                    email TEXT,
                    phone TEXT,
                    company_size TEXT,
                    revenue TEXT,
                    engagement_score INTEGER,
                    source TEXT,
                    linkedin_url TEXT,
                    notes TEXT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                )
            """)
            
            # Create index on engagement_score for faster queries
            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_prospects_score 
                ON prospects(engagement_score DESC)
            """)
            
            # Campaigns table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS campaigns (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    event_type TEXT,
                    start_date TIMESTAMP,
                    end_date TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    budget REAL DEFAULT 50000,
                    target_audience TEXT,
                    results TEXT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                )
            """)
            
            # Messages table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    prospect_id TEXT,
                    campaign_id TEXT,
                    message TEXT,
                    channel TEXT DEFAULT 'email',
                    sent_at TIMESTAMP,
                    opened_at TIMESTAMP,
                    replied_at TIMESTAMP,
                    status TEXT DEFAULT 'sent',
                    response TEXT,
                    FOREIGN KEY (prospect_id) REFERENCES prospects(id),
                    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
                )
            """)
            
            # Create index on message status
            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_status 
                ON messages(status)
            """)
            
            # Conversations table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    prospect_id TEXT,
                    message_id TEXT,
                    sender TEXT,
                    content TEXT,
                    sentiment REAL,
                    intent TEXT,
                    timestamp TIMESTAMP,
                    FOREIGN KEY (prospect_id) REFERENCES prospects(id),
                    FOREIGN KEY (message_id) REFERENCES messages(id)
                )
            """)
            
            # Payments table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS payments (
                    id TEXT PRIMARY KEY,
                    prospect_id TEXT,
                    campaign_id TEXT,
                    amount REAL,
                    currency TEXT DEFAULT 'INR',
                    status TEXT DEFAULT 'pending',
                    payment_method TEXT,
                    transaction_id TEXT,
                    payment_link TEXT,
                    created_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (prospect_id) REFERENCES prospects(id),
                    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
                )
            """)
            
            # Analytics table for aggregated data
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS analytics (
                    id TEXT PRIMARY KEY,
                    date DATE,
                    metric_name TEXT,
                    metric_value REAL,
                    dimension TEXT,
                    timestamp TIMESTAMP
                )
            """)
            
            self.conn.commit()
            print("✅ All database tables created/verified")
            
        except Exception as e:
            print(f"❌ Table creation failed: {e}")
            raise
    
    def save_prospect(self, prospect: Dict) -> Optional[str]:
        """
        Save a prospect to database.
        
        Args:
            prospect: Dictionary containing prospect data
        
        Returns:
            Prospect ID if successful, None otherwise
        """
        try:
            # Generate ID if not provided
            prospect_id = prospect.get('id', f"P{int(time.time())}{random.randint(100,999)}")
            
            self.cursor.execute("""
                INSERT OR REPLACE INTO prospects 
                (id, name, title, company, industry, location, email, phone,
                 company_size, revenue, engagement_score, source, linkedin_url,
                 notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                prospect_id,
                prospect.get('name', ''),
                prospect.get('title', ''),
                prospect.get('company', ''),
                prospect.get('industry', ''),
                prospect.get('location', ''),
                prospect.get('email', ''),
                prospect.get('phone', ''),
                prospect.get('company_size', ''),
                prospect.get('revenue', ''),
                prospect.get('engagement_score', 50),
                prospect.get('source', 'manual'),
                prospect.get('linkedin_url', ''),
                prospect.get('notes', ''),
                datetime.now(),
                datetime.now()
            ))
            self.conn.commit()
            return prospect_id
            
        except Exception as e:
            print(f"❌ Error saving prospect: {e}")
            return None
    
    def save_campaign(self, campaign: Dict) -> Optional[str]:
        """
        Save campaign to database.
        
        Args:
            campaign: Dictionary containing campaign data
        
        Returns:
            Campaign ID if successful, None otherwise
        """
        try:
            campaign_id = campaign.get('id', f"CAMP{int(time.time())}")
            
            self.cursor.execute("""
                INSERT OR REPLACE INTO campaigns 
                (id, name, event_type, start_date, status, budget, 
                 target_audience, results, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                campaign_id,
                campaign.get('name', ''),
                campaign.get('event_type', ''),
                campaign.get('start_date', datetime.now()),
                campaign.get('status', 'active'),
                campaign.get('budget', 50000),
                json.dumps(campaign.get('target_audience', {})),
                json.dumps(campaign.get('results', {})),
                datetime.now(),
                datetime.now()
            ))
            self.conn.commit()
            return campaign_id
            
        except Exception as e:
            print(f"❌ Error saving campaign: {e}")
            return None
    
    def save_message(self, prospect_id: str, campaign_id: str, 
                    message: str, channel: str = 'email') -> Optional[str]:
        """
        Save sent message to database.
        
        Args:
            prospect_id: ID of the prospect
            campaign_id: ID of the campaign
            message: Message content
            channel: Communication channel
        
        Returns:
            Message ID if successful, None otherwise
        """
        try:
            msg_id = f"MSG{int(time.time())}{random.randint(100,999)}"
            
            self.cursor.execute("""
                INSERT INTO messages 
                (id, prospect_id, campaign_id, message, channel, sent_at, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (msg_id, prospect_id, campaign_id, message, channel, 
                  datetime.now(), 'sent'))
            
            self.conn.commit()
            return msg_id
            
        except Exception as e:
            print(f"❌ Error saving message: {e}")
            return None
    
    def save_payment(self, prospect_id: str, campaign_id: str, 
                    amount: float, payment_link: Optional[str] = None) -> Optional[str]:
        """
        Save payment record to database.
        
        Args:
            prospect_id: ID of the prospect
            campaign_id: ID of the campaign
            amount: Payment amount
            payment_link: Payment link URL
        
        Returns:
            Payment ID if successful, None otherwise
        """
        try:
            payment_id = f"PAY{int(time.time())}{random.randint(100,999)}"
            
            self.cursor.execute("""
                INSERT INTO payments 
                (id, prospect_id, campaign_id, amount, currency, status, 
                 payment_link, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (payment_id, prospect_id, campaign_id, amount, 'INR', 
                  'pending', payment_link, datetime.now()))
            
            self.conn.commit()
            return payment_id
            
        except Exception as e:
            print(f"❌ Error saving payment: {e}")
            return None
    
    def get_all_prospects(self, limit: int = 100) -> List[Tuple]:
        """
        Get all prospects from database.
        
        Args:
            limit: Maximum number of prospects to return
        
        Returns:
            List of prospect tuples
        """
        try:
            self.cursor.execute("""
                SELECT * FROM prospects 
                ORDER BY engagement_score DESC 
                LIMIT ?
            """, (limit,))
            return self.cursor.fetchall()
            
        except Exception as e:
            print(f"❌ Error getting prospects: {e}")
            return []
    
    def get_prospects_by_criteria(self, criteria: Dict) -> List[Tuple]:
        """
        Get prospects matching specific criteria.
        
        Args:
            criteria: Dictionary with filters (industry, location, min_score)
        
        Returns:
            List of matching prospect tuples
        """
        try:
            query = "SELECT * FROM prospects WHERE 1=1"
            params = []
            
            if 'industry' in criteria and criteria['industry']:
                placeholders = ','.join(['?' for _ in criteria['industry']])
                query += f" AND industry IN ({placeholders})"
                params.extend(criteria['industry'])
            
            if 'location' in criteria and criteria['location']:
                placeholders = ','.join(['?' for _ in criteria['location']])
                query += f" AND location IN ({placeholders})"
                params.extend(criteria['location'])
            
            if 'min_score' in criteria:
                query += " AND engagement_score >= ?"
                params.append(criteria['min_score'])
            
            query += " ORDER BY engagement_score DESC"
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
            
        except Exception as e:
            print(f"❌ Error filtering prospects: {e}")
            return []
    
    def get_campaign_stats(self, campaign_id: str) -> Dict:
        """
        Get statistics for a specific campaign.
        
        Args:
            campaign_id: ID of the campaign
        
        Returns:
            Dictionary with campaign statistics
        """
        try:
            self.cursor.execute("""
                SELECT 
                    COUNT(DISTINCT m.prospect_id) as total_contacted,
                    COUNT(CASE WHEN m.replied_at IS NOT NULL THEN 1 END) as total_replies,
                    COUNT(DISTINCT p.id) as total_prospects,
                    COALESCE(SUM(pay.amount), 0) as total_revenue,
                    COUNT(CASE WHEN pay.status = 'completed' THEN 1 END) as total_payments
                FROM campaigns c
                LEFT JOIN messages m ON c.id = m.campaign_id
                LEFT JOIN prospects p ON m.prospect_id = p.id
                LEFT JOIN payments pay ON p.id = pay.prospect_id AND pay.campaign_id = c.id
                WHERE c.id = ?
            """, (campaign_id,))
            
            result = self.cursor.fetchone()
            if result:
                return {
                    'total_contacted': result[0] or 0,
                    'total_replies': result[1] or 0,
                    'total_prospects': result[2] or 0,
                    'total_revenue': result[3] or 0,
                    'total_payments': result[4] or 0
                }
            return {}
            
        except Exception as e:
            print(f"❌ Error getting campaign stats: {e}")
            return {}
    
    def get_stats(self) -> Dict:
        """Get overall database statistics"""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM prospects")
            total_prospects = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM campaigns")
            total_campaigns = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM messages")
            total_messages = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM payments WHERE status='completed'")
            total_payments = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM payments WHERE status='completed'")
            total_revenue = self.cursor.fetchone()[0]
            
            return {
                'total_prospects': total_prospects,
                'total_campaigns': total_campaigns,
                'total_messages': total_messages,
                'total_payments': total_payments,
                'total_revenue': total_revenue
            }
            
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return {}
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✅ Database connection closed")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
