"""
Tax Loss Harvesting Service
Identifies and executes tax-efficient selling strategies
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta, date
from dataclasses import asdict
import uuid

from models.entities import TaxHarvest
from models.similarity_engine import SimilarityEngine
from services.ibkr_client import IBKRClient

class TaxHarvestService:
    """Tax loss harvesting service"""
    
    def __init__(self, ibkr_client: IBKRClient):
        self.ibkr = ibkr_client
        self.similarity_engine = SimilarityEngine()
        self.tax_harvests = {}
        self.tax_rate = 0.25  # 25% tax rate
        
        # Initialize demo opportunities
        self._initialize_demo_opportunities()
    
    def _initialize_demo_opportunities(self):
        """Create demo tax harvest opportunities"""
        opportunities = [
            ("TSLA", 30, 250.0, 245.0, date(2024, 1, 15)),
            ("NFLX", 20, 400.0, 380.0, date(2024, 2, 1)),
        ]
        
        for symbol, shares, purchase_price, current_price, purchase_date in opportunities:
            loss_amount = (purchase_price - current_price) * shares
            tax_savings = loss_amount * self.tax_rate
            wash_sale_date = purchase_date + timedelta(days=30)
            
            harvest = TaxHarvest(
                id=str(uuid.uuid4()),
                portfolio_id="portfolio_1",
                symbol=symbol,
                shares=shares,
                purchase_price=purchase_price,
                current_price=current_price,
                loss_amount=loss_amount,
                tax_savings=tax_savings,
                purchase_date=purchase_date,
                status="identified",
                wash_sale_date=wash_sale_date
            )
            self.tax_harvests[harvest.id] = harvest
    
    async def get_tax_harvesting_data(self, user_id: str) -> Dict:
        """Get tax harvesting opportunities"""
        harvests = list(self.tax_harvests.values())
        
        total_savings = sum(h.tax_savings for h in harvests if h.status == "identified")
        
        return {
            "tax_harvests": [asdict(h) for h in harvests],
            "total_potential_savings": total_savings,
            "current_year_harvested": 0.0
        }
    
    async def execute_tax_harvest(self, harvest_id: str) -> Dict:
        """Execute a tax harvest"""
        if harvest_id not in self.tax_harvests:
            return {"error": "Tax harvest not found"}
        
        harvest = self.tax_harvests[harvest_id]
        
        # Execute sell order
        market_data = await self.ibkr.get_market_data(harvest.symbol)
        
        # Update status
        harvest.status = "executed"
        harvest.updated_date = datetime.now()
        
        # Find replacement securities
        replacements = await self._find_replacement_securities(harvest.symbol)
        
        return {
            "success": True,
            "harvest": asdict(harvest),
            "replacement_suggestions": replacements
        }
    
    async def _find_replacement_securities(self, symbol: str) -> List[Dict]:
        """Find similar securities for replacement"""
        # Mock replacement suggestions
        replacements = [
            {
                "symbol": f"{symbol}_ALT1",
                "similarity_score": 0.92,
                "reason": "High correlation, same sector"
            },
            {
                "symbol": f"{symbol}_ALT2",
                "similarity_score": 0.88,
                "reason": "Similar volatility and beta"
            }
        ]
        return replacements
    
    async def identify_opportunities(self, portfolio_id: str) -> List[TaxHarvest]:
        """Identify new tax loss harvesting opportunities"""
        # TODO: Implement opportunity identification logic
        return list(self.tax_harvests.values())

# Export
__all__ = ["TaxHarvestService"]
