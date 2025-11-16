"""
Models Package
Contains entity models, LSTM autoencoder, and similarity engine
"""

from .entities import (
    Portfolio,
    Holding,
    Trade,
    AIRecommendation,
    TaxHarvest,
    ExternalAccount,
    EducationalVideo,
    User
)
from .lstm_autoencoder import LSTMAutoencoder
from .similarity_engine import SimilarityEngine, AssetSimilarity

__all__ = [
    "Portfolio",
    "Holding",
    "Trade",
    "AIRecommendation",
    "TaxHarvest",
    "ExternalAccount",
    "EducationalVideo",
    "User",
    "LSTMAutoencoder",
    "SimilarityEngine",
    "AssetSimilarity"
]
