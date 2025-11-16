"""
WealthAlloc Backend - Main FastAPI Application
Perfectly matched to Base44 frontend entities
IBKR integration + 500M+ user scalability
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import models and services
from models.entities import Portfolio, Holding, Trade, AIRecommendation, TaxHarvest, ExternalAccount, EducationalVideo, User
from services.ibkr_client import IBKRClient
from services.portfolio_service import PortfolioService
from services.tax_harvest_service import TaxHarvestService
from services.ai_recommendations import AIRecommendationEngine

# Initialize FastAPI app
app = FastAPI(
    title="WealthAlloc API",
    version="1.0.0",
    docs_url="/api/docs",
    description="AI-Powered Portfolio Management with IBKR Integration"
)

# CORS for Base44 frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure with env variable in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services (will be done in startup event)
ibkr_client = None
portfolio_service = None
tax_harvest_service = None
ai_recommendation_engine = None

@app.on_event("startup")
async def startup():
    """Initialize all services on startup"""
    global ibkr_client, portfolio_service, tax_harvest_service, ai_recommendation_engine
    
    print("[STARTUP] Initializing WealthAlloc Backend...")
    
    # Initialize IBKR client
    ibkr_client = IBKRClient(
        host=os.getenv("IBKR_HOST", "127.0.0.1"),
        port=int(os.getenv("IBKR_PORT", 7497)),
        client_id=int(os.getenv("IBKR_CLIENT_ID", 1))
    )
    await ibkr_client.connect()
    
    # Initialize services
    portfolio_service = PortfolioService(ibkr_client)
    tax_harvest_service = TaxHarvestService(ibkr_client)
    ai_recommendation_engine = AIRecommendationEngine()
    
    print("[STARTUP] ✓ All services initialized successfully")

# ===== Request/Response Models =====

class TradeRequest(BaseModel):
    portfolio_id: str
    symbol: str
    trade_type: str  # buy, sell
    order_type: str  # market, limit, stop
    shares: float
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None

class RecommendationUpdate(BaseModel):
    status: str  # acted_upon, dismissed, expired

class TaxHarvestExecute(BaseModel):
    harvest_id: str

class ProfileUpdate(BaseModel):
    phone: Optional[str] = None
    risk_tolerance: Optional[str] = None
    investment_experience: Optional[str] = None
    annual_income: Optional[float] = None

# ===== Authentication =====

async def get_current_user_id() -> str:
    """Get current user ID from JWT token"""
    # TODO: Implement JWT token verification
    return "user_1"  # Demo user for MVP

# ===== API Endpoints =====

@app.get("/api/v1/dashboard")
async def get_dashboard(user_id: str = Depends(get_current_user_id)):
    """Dashboard data for Dashboard.jsx"""
    return await portfolio_service.get_dashboard_data(user_id)

@app.get("/api/v1/portfolio")
async def get_portfolio(user_id: str = Depends(get_current_user_id)):
    """Portfolio data for Portfolio.jsx"""
    return await portfolio_service.get_portfolio_data(user_id)

@app.get("/api/v1/recommendations")
async def get_recommendations(user_id: str = Depends(get_current_user_id)):
    """AI recommendations for AIRecommendations.jsx"""
    return await ai_recommendation_engine.get_recommendations(user_id)

@app.put("/api/v1/recommendations/{rec_id}")
async def update_recommendation(
    rec_id: str,
    update: RecommendationUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """Update recommendation status"""
    return await ai_recommendation_engine.update_recommendation_status(rec_id, update.status)

@app.get("/api/v1/tax-harvesting")
async def get_tax_harvesting(user_id: str = Depends(get_current_user_id)):
    """Tax harvesting data for TaxHarvesting.jsx"""
    return await tax_harvest_service.get_tax_harvesting_data(user_id)

@app.post("/api/v1/tax-harvesting/execute")
async def execute_tax_harvest(
    data: TaxHarvestExecute,
    user_id: str = Depends(get_current_user_id)
):
    """Execute tax harvest"""
    return await tax_harvest_service.execute_tax_harvest(data.harvest_id)

@app.post("/api/v1/trade")
async def create_trade(
    trade: TradeRequest,
    user_id: str = Depends(get_current_user_id)
):
    """Create trade for Trade.jsx"""
    return await portfolio_service.create_trade(trade.dict())

@app.get("/api/v1/trade-history")
async def get_trade_history(
    limit: int = Query(100, le=500),
    user_id: str = Depends(get_current_user_id)
):
    """Trade history for TradeHistory.jsx"""
    return await portfolio_service.get_trade_history(user_id, limit)

@app.get("/api/v1/external-accounts")
async def get_external_accounts(user_id: str = Depends(get_current_user_id)):
    """External accounts for ExternalAccounts.jsx"""
    return await portfolio_service.get_external_accounts(user_id)

@app.get("/api/v1/educational-videos")
async def get_educational_videos(
    category: Optional[str] = Query(None),
    user_id: str = Depends(get_current_user_id)
):
    """Educational videos for Education.jsx"""
    return await portfolio_service.get_educational_videos(category)

@app.get("/api/v1/profile")
async def get_profile(user_id: str = Depends(get_current_user_id)):
    """User profile for Profile.jsx"""
    return await portfolio_service.get_user_profile(user_id)

@app.put("/api/v1/profile")
async def update_profile(
    update: ProfileUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """Update user profile"""
    return await portfolio_service.update_user_profile(user_id, update.dict(exclude_none=True))

@app.get("/api/v1/market-data/{symbol}")
async def get_market_data(symbol: str):
    """Get real-time market data from IBKR"""
    return await ibkr_client.get_market_data(symbol)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "ibkr_connected": ibkr_client.connected if ibkr_client else False
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true",
        workers=int(os.getenv("WORKERS", 4))
    )
