"""
EventFlow AI - Utilities Module
Helper functions for data processing, export, and formatting
"""

import json
import csv
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
import os

class Utils:
    """Utility functions for EventFlow AI"""
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """
        Format amount in Indian currency format.
        
        Args:
            amount: Amount in rupees
        
        Returns:
            Formatted string (e.g., ₹1,23,456)
        """
        if amount >= 10000000:  # 1 Crore
            return f"₹{amount/10000000:.2f}Cr"
        elif amount >= 100000:  # 1 Lakh
            return f"₹{amount/100000:.2f}L"
        else:
            return f"₹{amount:,.0f}"
    
    @staticmethod
    def calculate_roi(revenue: float, cost: float) -> float:
        """
        Calculate ROI percentage.
        
        Args:
            revenue: Total revenue
            cost: Total cost
        
        Returns:
            ROI percentage
        """
        if cost == 0:
            return 0
        return ((revenue - cost) / cost) * 100
    
    @staticmethod
    def parse_revenue(revenue_str: str) -> float:
        """
        Parse Indian revenue string to float.
        
        Args:
            revenue_str: Revenue string (e.g., "₹5Cr", "₹10L")
        
        Returns:
            Revenue in rupees as float
        """
        revenue_str = revenue_str.replace('₹', '').strip()
        
        if 'Cr' in revenue_str:
            return float(revenue_str.replace('Cr', '')) * 10000000
        elif 'L' in revenue_str:
            return float(revenue_str.replace('L', '')) * 100000
        else:
            try:
                return float(revenue_str)
            except:
                return 0.0
    
    @staticmethod
    def export_to_excel(data: Dict, filename: Optional[str] = None) -> str:
        """
        Export data to Excel file.
        
        Args:
            data: Dictionary with data to export
            filename: Output filename (optional)
        
        Returns:
            Path to created file
        """
        if not filename:
            filename = f"eventflow_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        # Convert to DataFrame
        df = pd.DataFrame([data]) if isinstance(data, dict) else pd.DataFrame(data)
        
        # Save to Excel
        df.to_excel(filename, index=False)
        print(f"✅ Data exported to {filename}")
        
        return filename
    
    @staticmethod
    def export_to_csv(data: List[Dict], filename: Optional[str] = None) -> str:
        """
        Export data to CSV file.
        
        Args:
            data: List of dictionaries to export
            filename: Output filename (optional)
        
        Returns:
            Path to created file
        """
        if not filename:
            filename = f"eventflow_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        if not data:
            return filename
        
        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"✅ Data exported to {filename}")
        return filename
    
    @staticmethod
    def save_to_json(data: Any, filename: Optional[str] = None) -> str:
        """
        Save data to JSON file.
        
        Args:
            data: Data to save
            filename: Output filename (optional)
        
        Returns:
            Path to created file
        """
        if not filename:
            filename = f"eventflow_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"✅ Data saved to {filename}")
        return filename
    
    @staticmethod
    def load_from_json(filename: str) -> Any:
        """
        Load data from JSON file.
        
        Args:
            filename: JSON file to load
        
        Returns:
            Loaded data
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
            return None
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in file: {filename}")
            return None

class ROICalculator:
    """ROI calculation utilities"""
    
    def __init__(self):
        self.total_revenue = 0
        self.total_cost = 0
    
    def calculate(self, tickets: int, ticket_price: int, 
                  campaign_cost: int = 50000) -> Dict:
        """
        Calculate ROI for a campaign.
        
        Args:
            tickets: Number of tickets sold
            ticket_price: Price per ticket
            campaign_cost: Total campaign cost
        
        Returns:
            Dictionary with ROI metrics
        """
        revenue = tickets * ticket_price
        profit = revenue - campaign_cost
        roi_percentage = Utils.calculate_roi(revenue, campaign_cost)
        
        self.total_revenue += revenue
        self.total_cost += campaign_cost
        
        return {
            "tickets_sold": tickets,
            "ticket_price": ticket_price,
            "revenue": revenue,
            "campaign_cost": campaign_cost,
            "profit": profit,
            "roi_percentage": round(roi_percentage, 1),
            "roi_multiple": round(profit / campaign_cost, 1) if campaign_cost > 0 else 0,
            "formatted_revenue": Utils.format_currency(revenue)
        }
    
    def get_summary(self) -> Dict:
        """
        Get overall ROI summary.
        
        Returns:
            Dictionary with total metrics
        """
        total_profit = self.total_revenue - self.total_cost
        overall_roi = Utils.calculate_roi(self.total_revenue, self.total_cost)
        
        return {
            "total_revenue": self.total_revenue,
            "total_cost": self.total_cost,
            "total_profit": total_profit,
            "overall_roi": round(overall_roi, 1),
            "roi_multiple": round(total_profit / self.total_cost, 1) if self.total_cost > 0 else 0,
            "formatted_revenue": Utils.format_currency(self.total_revenue)
        }

class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder for datetime objects"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
