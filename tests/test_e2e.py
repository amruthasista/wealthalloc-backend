"""
End-to-End Integration Tests
"""

import pytest
import httpx
import asyncio
from datetime import datetime

BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_complete_trading_flow():
    """Test complete trading workflow"""
    async with httpx.AsyncClient() as client:
        # 1. Get portfolio
        response = await client.get(f"{BASE_URL}/api/v1/portfolio")
        assert response.status_code == 200
        portfolio_data = response.json()
        portfolio_id = portfolio_data["portfolio"]["id"]
        
        # 2. Create a trade
        trade_data = {
            "portfolio_id": portfolio_id,
            "symbol": "AAPL",
            "trade_type": "buy",
            "order_type": "market",
            "shares": 10
        }
        response = await client.post(f"{BASE_URL}/api/v1/trade", json=trade_data)
        assert response.status_code == 200
        trade_result = response.json()
        assert "trade" in trade_result
        
        # 3. Check trade history
        response = await client.get(f"{BASE_URL}/api/v1/trade-history?limit=10")
        assert response.status_code == 200
        history = response.json()
        assert "trades" in history

@pytest.mark.asyncio
async def test_tax_harvest_flow():
    """Test tax loss harvesting workflow"""
    async with httpx.AsyncClient() as client:
        # 1. Get tax opportunities
        response = await client.get(f"{BASE_URL}/api/v1/tax-harvesting")
        assert response.status_code == 200
        data = response.json()
        assert "tax_harvests" in data
        
        if len(data["tax_harvests"]) > 0:
            harvest_id = data["tax_harvests"][0]["id"]
            
            # 2. Execute harvest
            execute_data = {"harvest_id": harvest_id}
            response = await client.post(
                f"{BASE_URL}/api/v1/tax-harvesting/execute",
                json=execute_data
            )
            assert response.status_code == 200

@pytest.mark.asyncio
async def test_recommendation_workflow():
    """Test AI recommendation workflow"""
    async with httpx.AsyncClient() as client:
        # 1. Get recommendations
        response = await client.get(f"{BASE_URL}/api/v1/recommendations")
        assert response.status_code == 200
        data = response.json()
        assert "recommendations" in data
        
        if len(data["recommendations"]) > 0:
            rec_id = data["recommendations"][0]["id"]
            
            # 2. Update recommendation status
            update_data = {"status": "acted_upon"}
            response = await client.put(
                f"{BASE_URL}/api/v1/recommendations/{rec_id}",
                json=update_data
            )
            assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
