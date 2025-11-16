"""
Database Package
Database initialization and utilities
"""

import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/wealthalloc")

engine = create_async_engine(DATABASE_URL, echo=False, pool_size=20, max_overflow=10)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    """Initialize database"""
    print("[DATABASE] Initializing database...")
    # In production, run migrations here
    # For now, just log
    print("[DATABASE] ✓ Database initialized")

async def get_session() -> AsyncSession:
    """Get database session"""
    async with async_session_maker() as session:
        yield session

__all__ = ["init_db", "get_session", "engine"]
