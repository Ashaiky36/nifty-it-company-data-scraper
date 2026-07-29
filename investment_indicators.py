# investment_indicators.py
"""
Investment Decision Indicators for NIFTY IT Stocks
"""

import pandas as pd
import numpy as np

class InvestmentIndicators:
    """Calculate investment indicators for IT companies"""
    
    @staticmethod
    def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate all investment indicators"""
        df = df.copy()
        
        # 1. Growth Indicators
        df['Revenue_Growth'] = df['Annual Revenue (Cr)'].pct_change() * 100
        
        # 2. Profitability Indicators
        df['Net_Margin'] = (df['Annual Profit (Cr)'] / df['Annual Revenue (Cr)']) * 100
        
        # 3. Scale Indicators
        df['Revenue_per_Client'] = df['Annual Revenue (Cr)'] / df['Total Clients']
        
        # 4. Deal Momentum
        df['Deal_to_Revenue_Ratio'] = (df['Deal Wins'] / (df['Annual Revenue (Cr)'] / 100)) * 100
        
        # 5. Client Concentration Risk
        df['Client_Concentration_Risk'] = df['Client Concentration'].str.extract(r'(\d+)').astype(float) / 100
        
        # 6. Composite Score (Weighted)
        df['Growth_Score'] = pd.qcut(df['Revenue_Growth'].rank(pct=True), 5, labels=False) + 1
        df['Profit_Score'] = pd.qcut(df['Net_Margin'].rank(pct=True), 5, labels=False) + 1
        df['Scale_Score'] = pd.qcut(df['Annual Revenue (Cr)'].rank(pct=True), 5, labels=False) + 1
        df['Deal_Score'] = pd.qcut(df['Deal_to_Revenue_Ratio'].rank(pct=True), 5, labels=False) + 1
        
        df['Investment_Score'] = (
            df['Growth_Score'] * 0.30 +
            df['Profit_Score'] * 0.25 +
            df['Scale_Score'] * 0.25 +
            df['Deal_Score'] * 0.20
        )
        
        # 7. Investment Recommendation
        def get_recommendation(score):
            if score >= 4.5:
                return 'Strong Buy'
            elif score >= 3.5:
                return 'Buy'
            elif score >= 2.5:
                return 'Hold'
            elif score >= 1.5:
                return 'Sell'
            else:
                return 'Strong Sell'
        
        df['Recommendation'] = df['Investment_Score'].apply(get_recommendation)
        
        # 8. Risk Level
        def get_risk(row):
            risk = 0
            if row.get('Client_Concentration_Risk', 0) > 0.20:
                risk += 1
            if row.get('Revenue_Growth', 0) < 5:
                risk += 1
            if row.get('Net_Margin', 0) < 15:
                risk += 1
            if row.get('Deal_to_Revenue_Ratio', 0) < 50:
                risk += 1
            
            if risk <= 1:
                return 'Low'
            elif risk <= 2:
                return 'Medium'
            elif risk <= 3:
                return 'High'
            else:
                return 'Very High'
        
        df['Risk_Level'] = df.apply(get_risk, axis=1)
        
        return df