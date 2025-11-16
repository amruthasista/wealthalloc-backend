"""
Similarity Engine - Hybrid Approach
Combines multiple similarity metrics for asset comparison
Used for tax loss harvesting and portfolio optimization
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from dataclasses import dataclass

@dataclass
class AssetSimilarity:
    """Asset similarity result"""
    symbol: str
    similarity_score: float
    correlation: float
    sector_match: bool
    reasons: List[str]

class SimilarityEngine:
    """
    Hybrid similarity engine for comparing assets
    
    Uses multiple metrics:
    - Price correlation
    - Returns correlation  
    - Sector similarity
    - Volatility similarity
    - Beta similarity
    """
    
    def __init__(
        self,
        correlation_weight: float = 0.35,
        returns_weight: float = 0.25,
        sector_weight: float = 0.20,
        volatility_weight: float = 0.10,
        beta_weight: float = 0.10
    ):
        """
        Initialize Similarity Engine
        
        Args:
            correlation_weight: Weight for price correlation
            returns_weight: Weight for returns correlation
            sector_weight: Weight for sector similarity
            volatility_weight: Weight for volatility similarity
            beta_weight: Weight for beta similarity
        """
        self.weights = {
            "correlation": correlation_weight,
            "returns": returns_weight,
            "sector": sector_weight,
            "volatility": volatility_weight,
            "beta": beta_weight
        }
        
        # Validate weights sum to 1.0
        total_weight = sum(self.weights.values())
        if not np.isclose(total_weight, 1.0):
            raise ValueError(f"Weights must sum to 1.0, got {total_weight}")
        
        self.price_data = {}
        self.asset_metadata = {}
        
    def add_asset_data(
        self,
        symbol: str,
        prices: pd.Series,
        sector: str = None,
        beta: float = 1.0
    ):
        """Add asset data for similarity calculation"""
        self.price_data[symbol] = prices
        self.asset_metadata[symbol] = {
            "sector": sector,
            "beta": beta
        }
    
    def calculate_price_correlation(
        self,
        symbol1: str,
        symbol2: str
    ) -> float:
        """Calculate price correlation between two assets"""
        if symbol1 not in self.price_data or symbol2 not in self.price_data:
            return 0.0
        
        prices1 = self.price_data[symbol1]
        prices2 = self.price_data[symbol2]
        
        # Align indices
        common_idx = prices1.index.intersection(prices2.index)
        if len(common_idx) < 2:
            return 0.0
        
        return float(prices1.loc[common_idx].corr(prices2.loc[common_idx]))
    
    def calculate_returns_correlation(
        self,
        symbol1: str,
        symbol2: str
    ) -> float:
        """Calculate returns correlation"""
        if symbol1 not in self.price_data or symbol2 not in self.price_data:
            return 0.0
        
        prices1 = self.price_data[symbol1]
        prices2 = self.price_data[symbol2]
        
        # Calculate returns
        returns1 = prices1.pct_change().dropna()
        returns2 = prices2.pct_change().dropna()
        
        # Align indices
        common_idx = returns1.index.intersection(returns2.index)
        if len(common_idx) < 2:
            return 0.0
        
        return float(returns1.loc[common_idx].corr(returns2.loc[common_idx]))
    
    def calculate_sector_similarity(
        self,
        symbol1: str,
        symbol2: str
    ) -> float:
        """Calculate sector similarity (1.0 if same sector, 0.0 otherwise)"""
        if symbol1 not in self.asset_metadata or symbol2 not in self.asset_metadata:
            return 0.0
        
        sector1 = self.asset_metadata[symbol1].get("sector")
        sector2 = self.asset_metadata[symbol2].get("sector")
        
        if sector1 is None or sector2 is None:
            return 0.0
        
        return 1.0 if sector1 == sector2 else 0.0
    
    def calculate_volatility_similarity(
        self,
        symbol1: str,
        symbol2: str
    ) -> float:
        """Calculate volatility similarity"""
        if symbol1 not in self.price_data or symbol2 not in self.price_data:
            return 0.0
        
        returns1 = self.price_data[symbol1].pct_change().dropna()
        returns2 = self.price_data[symbol2].pct_change().dropna()
        
        vol1 = returns1.std()
        vol2 = returns2.std()
        
        if vol1 == 0 or vol2 == 0:
            return 0.0
        
        # Similarity = 1 - |vol1 - vol2| / max(vol1, vol2)
        similarity = 1.0 - abs(vol1 - vol2) / max(vol1, vol2)
        return max(0.0, similarity)
    
    def calculate_beta_similarity(
        self,
        symbol1: str,
        symbol2: str
    ) -> float:
        """Calculate beta similarity"""
        if symbol1 not in self.asset_metadata or symbol2 not in self.asset_metadata:
            return 0.0
        
        beta1 = self.asset_metadata[symbol1].get("beta", 1.0)
        beta2 = self.asset_metadata[symbol2].get("beta", 1.0)
        
        # Similarity = 1 - |beta1 - beta2| / max(|beta1|, |beta2|)
        max_beta = max(abs(beta1), abs(beta2))
        if max_beta == 0:
            return 1.0
        
        similarity = 1.0 - abs(beta1 - beta2) / max_beta
        return max(0.0, similarity)
    
    def calculate_overall_similarity(
        self,
        symbol1: str,
        symbol2: str
    ) -> Tuple[float, Dict[str, float]]:
        """
        Calculate overall similarity score using weighted combination
        
        Returns:
            Tuple of (overall_score, component_scores)
        """
        components = {
            "correlation": self.calculate_price_correlation(symbol1, symbol2),
            "returns": self.calculate_returns_correlation(symbol1, symbol2),
            "sector": self.calculate_sector_similarity(symbol1, symbol2),
            "volatility": self.calculate_volatility_similarity(symbol1, symbol2),
            "beta": self.calculate_beta_similarity(symbol1, symbol2)
        }
        
        # Calculate weighted sum
        overall_score = sum(
            components[key] * self.weights[key]
            for key in self.weights.keys()
        )
        
        return overall_score, components
    
    def find_similar_assets(
        self,
        target_symbol: str,
        candidate_symbols: List[str],
        min_similarity: float = 0.7,
        top_k: int = 5
    ) -> List[AssetSimilarity]:
        """
        Find most similar assets to target
        
        Args:
            target_symbol: Symbol to find replacements for
            candidate_symbols: List of candidate symbols
            min_similarity: Minimum similarity threshold
            top_k: Number of top matches to return
            
        Returns:
            List of AssetSimilarity objects
        """
        results = []
        
        for candidate in candidate_symbols:
            if candidate == target_symbol:
                continue
            
            overall_score, components = self.calculate_overall_similarity(
                target_symbol, candidate
            )
            
            if overall_score < min_similarity:
                continue
            
            # Build reasons list
            reasons = []
            if components["correlation"] > 0.8:
                reasons.append(f"High price correlation ({components['correlation']:.2%})")
            if components["returns"] > 0.8:
                reasons.append(f"High returns correlation ({components['returns']:.2%})")
            if components["sector"] == 1.0:
                reasons.append("Same sector")
            if components["volatility"] > 0.8:
                reasons.append("Similar volatility")
            if components["beta"] > 0.8:
                reasons.append("Similar beta")
            
            results.append(AssetSimilarity(
                symbol=candidate,
                similarity_score=overall_score,
                correlation=components["correlation"],
                sector_match=components["sector"] == 1.0,
                reasons=reasons
            ))
        
        # Sort by similarity score
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        
        return results[:top_k]
    
    def batch_similarity_matrix(
        self,
        symbols: List[str]
    ) -> pd.DataFrame:
        """
        Calculate similarity matrix for all symbol pairs
        
        Returns:
            DataFrame with similarity scores
        """
        n = len(symbols)
        matrix = np.zeros((n, n))
        
        for i, sym1 in enumerate(symbols):
            for j, sym2 in enumerate(symbols):
                if i == j:
                    matrix[i, j] = 1.0
                else:
                    score, _ = self.calculate_overall_similarity(sym1, sym2)
                    matrix[i, j] = score
        
        return pd.DataFrame(matrix, index=symbols, columns=symbols)

# Export
__all__ = ["SimilarityEngine", "AssetSimilarity"]
