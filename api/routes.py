"""
API Routes
All API endpoints for WealthAlloc
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

api_router = APIRouter()

# Request/Response Models
class TradeRequest(BaseModel):
    portfolio_id: str
    symbol: str
    trade_type: str
    order_type: str
    shares: float
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None

class RecommendationUpdate(BaseModel):
    status: str

class TaxHarvestExecute(BaseModel):
    harvest_id: str

class ProfileUpdate(BaseModel):
    phone: Optional[str] = None
    risk_tolerance: Optional[str] = None
    investment_experience: Optional[str] = None
    annual_income: Optional[float] = None

# Authentication dependency (placeholder)
async def get_current_user_id() -> str:
    """Get current user ID from JWT token"""
    return "user_1"

# Routes are defined in main.py for now
# This file can be expanded to organize routes by domain

__all__ = ["api_router"]
