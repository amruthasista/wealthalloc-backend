"""
Entity Model Tests
"""

import pytest
from datetime import datetime, date
import sys
sys.path.insert(0, '..')

from models.entities import Portfolio, Holding, Trade, AIRecommendation, TaxHarvest

# ==================== UNIT TESTS ====================

class TestEntities:
    """Test all Base44 entity models"""
    
    def test_portfolio_entity(self):
        """Test Portfolio entity creation"""
        from main import Portfolio
        
        portfolio = Portfolio(
            name="Test Portfolio",
            total_value=50000.0,
            total_gain_loss=5000.0,
            total_gain_loss_percent=11.11,
            cash_balance=5000.0,
            risk_score=55.0,
            risk_tolerance="moderate"
        )
        
        assert portfolio.name == "Test Portfolio"
        assert portfolio.total_value == 50000.0
        assert portfolio.risk_tolerance in ["conservative", "moderate", "aggressive"]
        assert portfolio.id is not None
        print("✓ Portfolio entity test passed")
    
    def test_holding_entity(self):
        """Test Holding entity creation"""
        from main import Holding
        
        holding = Holding(
            portfolio_id="portfolio_1",
            symbol="AAPL",
            company_name="Apple Inc.",
            shares=100,
            average_cost=150.0,
            current_price=175.0,
            total_value=17500.0,
            sector="Technology",
            asset_class="stocks"
        )
        
        assert holding.symbol == "AAPL"
        assert holding.shares == 100
        assert holding.asset_class in ["stocks", "etf", "bonds", "cash", "alternatives"]
        print("✓ Holding entity test passed")
    
    def test_trade_entity(self):
        """Test Trade entity creation"""
        from main import Trade
        
        trade = Trade(
            portfolio_id="portfolio_1",
            symbol="MSFT",
            trade_type="buy",
            order_type="market",
            shares=50,
            status="pending"
        )
        
        assert trade.trade_type in ["buy", "sell"]
        assert trade.order_type in ["market", "limit", "stop"]
        assert trade.status in ["pending", "executed", "cancelled", "failed"]
        print("✓ Trade entity test passed")
    
    def test_ai_recommendation_entity(self):
        """Test AIRecommendation entity"""
        from main import AIRecommendation
        
        rec = AIRecommendation(
            user_id="user_1",
            title="Buy Opportunity",
            description="Strong buy signal detected",
            recommendation_type="buy",
            symbol="GOOGL",
            confidence_score=85.0,
            priority="high",
            status="active"
        )
        
        assert rec.recommendation_type in ["buy", "sell", "rebalance", "alert", "opportunity"]
        assert rec.priority in ["low", "medium", "high", "urgent"]
        assert rec.confidence_score >= 0 and rec.confidence_score <= 100
        print("✓ AI Recommendation entity test passed")
    
    def test_tax_harvest_entity(self):
        """Test TaxHarvest entity"""
        from main import TaxHarvest
        
        harvest = TaxHarvest(
            portfolio_id="portfolio_1",
            symbol="TSLA",
            shares=10,
            purchase_price=800.0,
            current_price=600.0,
            loss_amount=2000.0,
            tax_savings=500.0,
            status="identified"
        )
        
        assert harvest.status in ["identified", "pending", "executed", "expired"]
        assert harvest.loss_amount > 0
        assert harvest.tax_savings > 0
        print("✓ Tax Harvest entity test passed")

# ==================== API INTEGRATION TESTS ====================

class TestAPIEndpoints:
    """Test all API endpoints"""
    
    @pytest.mark.asyncio
    async def test_health_check(self):
        """Test health check endpoint"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{TestConfig.API_BASE_URL}/health")
            assert response.status_code == 200
            data = response.json()
