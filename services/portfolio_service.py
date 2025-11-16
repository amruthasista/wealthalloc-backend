"""
Portfolio Service
Business logic for portfolio management
"""

import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta, date
from dataclasses import asdict
import uuid

from models.entities import Portfolio, Holding, Trade, ExternalAccount, EducationalVideo, User
from services.ibkr_client import IBKRClient

class PortfolioService:
    """Portfolio management service"""
    
    def __init__(self, ibkr_client: IBKRClient):
        self.ibkr = ibkr_client
        # Mock database - replace with real database in production
        self.portfolios = {}
        self.holdings = {}
        self.trades = {}
        self.users = {}
        self.external_accounts = {}
        self.videos = {}
        
        # Initialize demo data
        self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize demo data for testing"""
        # Create demo user
        user = User(
            id="user_1",
            email="demo@wealthalloc.com",
            full_name="Demo User",
            risk_tolerance="moderate",
            investment_experience="intermediate",
            annual_income=150000.0
        )
        self.users[user.id] = user
        
        # Create demo portfolio
        portfolio = Portfolio(
            id="portfolio_1",
            user_id="user_1",
            name="My Portfolio",
            total_value=100000.0,
            total_gain_loss=10000.0,
            total_gain_loss_percent=11.11,
            cash_balance=5000.0,
            risk_score=55.0,
            risk_tolerance="moderate"
        )
        self.portfolios[portfolio.id] = portfolio
        
        # Create demo holdings
        holdings_data = [
            ("AAPL", "Apple Inc.", 100, 150.0, 175.0, "Technology"),
            ("GOOGL", "Alphabet Inc.", 50, 2800.0, 2900.0, "Technology"),
            ("MSFT", "Microsoft Corp.", 75, 380.0, 400.0, "Technology"),
            ("TSLA", "Tesla Inc.", 30, 250.0, 245.0, "Automotive"),
            ("JPM", "JPMorgan Chase", 40, 145.0, 155.0, "Financial"),
        ]
        
        for symbol, name, shares, avg_cost, current_price, sector in holdings_data:
            total_value = shares * current_price
            total_cost = shares * avg_cost
            gain_loss = total_value - total_cost
            gain_loss_pct = (gain_loss / total_cost) * 100
            
            holding = Holding(
                id=str(uuid.uuid4()),
                portfolio_id=portfolio.id,
                symbol=symbol,
                company_name=name,
                shares=shares,
                average_cost=avg_cost,
                current_price=current_price,
                total_value=total_value,
                total_gain_loss=gain_loss,
                total_gain_loss_percent=gain_loss_pct,
                sector=sector,
                asset_class="stocks"
            )
            self.holdings[holding.id] = holding
        
        # Create educational videos
        videos_data = [
            ("Getting Started with Investing", "Learn the basics", 600, "beginner"),
            ("Understanding Tax Loss Harvesting", "Save on taxes", 900, "intermediate"),
            ("Advanced Portfolio Strategies", "Expert techniques", 1200, "advanced"),
        ]
        
        for title, desc, duration, level in videos_data:
            video = EducationalVideo(
                title=title,
                description=desc,
                duration=duration,
                category=level,
                difficulty_level=level,
                views=1000
            )
            self.videos[video.id] = video
    
    async def get_dashboard_data(self, user_id: str) -> Dict:
        """Get dashboard data"""
        # Get user portfolio
        portfolio = None
        for p in self.portfolios.values():
            if p.user_id == user_id:
                portfolio = p
                break
        
        if not portfolio:
            return {"error": "Portfolio not found"}
        
        # Get holdings
        holdings = [h for h in self.holdings.values() if h.portfolio_id == portfolio.id]
        
        # Calculate allocation
        allocation = {}
        for holding in holdings:
            sector = holding.sector or "Other"
            if sector not in allocation:
                allocation[sector] = 0.0
            allocation[sector] += holding.total_value
        
        return {
            "portfolio": asdict(portfolio),
            "holdings": [asdict(h) for h in holdings[:5]],
            "allocation": allocation,
            "recent_activity": [],
            "total_tax_savings": 2500.0
        }
    
    async def get_portfolio_data(self, user_id: str) -> Dict:
        """Get complete portfolio data"""
        portfolio = None
        for p in self.portfolios.values():
            if p.user_id == user_id:
                portfolio = p
                break
        
        if not portfolio:
            return {"error": "Portfolio not found"}
        
        holdings = [h for h in self.holdings.values() if h.portfolio_id == portfolio.id]
        
        return {
            "portfolio": asdict(portfolio),
            "holdings": [asdict(h) for h in holdings]
        }
    
    async def create_trade(self, trade_data: Dict) -> Dict:
        """Create a new trade"""
        # Get current price from IBKR
        market_data = await self.ibkr.get_market_data(trade_data["symbol"])
        price = market_data["last"]
        
        trade = Trade(
            portfolio_id=trade_data["portfolio_id"],
            symbol=trade_data["symbol"],
            trade_type=trade_data["trade_type"],
            order_type=trade_data["order_type"],
            shares=trade_data["shares"],
            price=price,
            limit_price=trade_data.get("limit_price"),
            stop_price=trade_data.get("stop_price"),
            total_amount=price * trade_data["shares"],
            status="pending"
        )
        
        # Place order with IBKR
        order_id = await self.ibkr.place_order(trade)
        trade.status = "executed"
        trade.executed_at = datetime.now()
        
        self.trades[trade.id] = trade
        
        return {"trade": asdict(trade), "order_id": order_id}
    
    async def get_trade_history(self, user_id: str, limit: int = 100) -> Dict:
        """Get trade history"""
        # Get user's portfolio
        portfolio = None
        for p in self.portfolios.values():
            if p.user_id == user_id:
                portfolio = p
                break
        
        if not portfolio:
            return {"trades": []}
        
        trades = [
            t for t in self.trades.values()
            if t.portfolio_id == portfolio.id
        ]
        trades.sort(key=lambda x: x.created_date, reverse=True)
        
        return {"trades": [asdict(t) for t in trades[:limit]]}
    
    async def get_external_accounts(self, user_id: str) -> Dict:
        """Get external accounts"""
        accounts = [
            a for a in self.external_accounts.values()
            if a.user_id == user_id
        ]
        return {"accounts": [asdict(a) for a in accounts]}
    
    async def get_educational_videos(self, category: str = None) -> Dict:
        """Get educational videos"""
        videos = list(self.videos.values())
        
        if category:
            videos = [v for v in videos if v.category == category]
        
        return {"videos": [asdict(v) for v in videos]}
    
    async def get_user_profile(self, user_id: str) -> Dict:
        """Get user profile"""
        if user_id in self.users:
            return asdict(self.users[user_id])
        return {"error": "User not found"}
    
    async def update_user_profile(self, user_id: str, updates: Dict) -> Dict:
        """Update user profile"""
        if user_id in self.users:
            user = self.users[user_id]
            for key, value in updates.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            user.updated_date = datetime.now()
            return {"success": True, "user": asdict(user)}
        return {"error": "User not found"}

# Export
__all__ = ["PortfolioService"]
