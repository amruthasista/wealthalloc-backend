"""
API Endpoint Tests
"""

import pytest
import httpx
from datetime import datetime

BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_health_endpoint():
    """Test health check endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

@pytest.mark.asyncio
async def test_dashboard_endpoint():
    """Test dashboard endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert "portfolio" in data
        assert "holdings" in data

@pytest.mark.asyncio
async def test_portfolio_endpoint():
    """Test portfolio endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/portfolio")
        assert response.status_code == 200
        data = response.json()
        assert "portfolio" in data
        assert "holdings" in data

@pytest.mark.asyncio
async def test_recommendations_endpoint():
    """Test AI recommendations endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/recommendations")
        assert response.status_code == 200
        data = response.json()
        assert "recommendations" in data

@pytest.mark.asyncio
async def test_tax_harvesting_endpoint():
    """Test tax harvesting endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/tax-harvesting")
        assert response.status_code == 200
        data = response.json()
        assert "tax_harvests" in data

@pytest.mark.asyncio
async def test_profile_endpoint():
    """Test profile endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/profile")
        assert response.status_code == 200
        data = response.json()
        assert "email" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
