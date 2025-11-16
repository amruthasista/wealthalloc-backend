"""
LSTM Autoencoder Enhanced WealthAlloc System
Based on Nature paper: s41599-025-04412-y
Adds advanced correlation extraction and network analysis
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import networkx as nx
from datetime import datetime, timedelta

# ==================== LSTM AUTOENCODER (FROM PAPER) ====================

class LSTMAutoencoder:
    """
    LSTM Autoencoder for extracting stock correlations
    Based on Nature paper methodology
    """
    
    def __init__(self, sequence_length: int = 60, encoding_dim: int = 32):
        self.sequence_length = sequence_length
        self.encoding_dim = encoding_dim
        self.encoder = None
        self.decoder = None
        self.autoencoder = None
        self.correlation_matrix = None
        
    def build_model(self, n_features: int):
        """Build LSTM Autoencoder architecture"""
        
        # Encoder
        encoder_inputs = keras.Input(shape=(self.sequence_length, n_features))
        
        # Encoder layers
        x = layers.LSTM(128, return_sequences=True)(encoder_inputs)
        x = layers.Dropout(0.2)(x)
        x = layers.LSTM(64, return_sequences=True)(x)
        x = layers.Dropout(0.2)(x)
        encoded = layers.LSTM(self.encoding_dim, return_sequences=False, name='encoded')(x)
        
        self.encoder = keras.Model(encoder_inputs, encoded, name='encoder')
        
        # Decoder
        decoder_inputs = keras.Input(shape=(self.encoding_dim,))
        x = layers.RepeatVector(self.sequence_length)(decoder_inputs)
        x = layers.LSTM(self.encoding_dim, return_sequences=True)(x)
        x = layers.Dropout(0.2)(x)
        x = layers.LSTM(64, return_sequences=True)(x)
        x = layers.Dropout(0.2)(x)
        x = layers.LSTM(128, return_sequences=True)(x)
        decoded = layers.TimeDistributed(layers.Dense(n_features))(x)
        
        self.decoder = keras.Model(decoder_inputs, decoded, name='decoder')
        
        # Autoencoder (Encoder + Decoder)
        autoencoder_outputs = self.decoder(self.encoder(encoder_inputs))
        self.autoencoder = keras.Model(encoder_inputs, autoencoder_outputs, name='autoencoder')
        
        self.autoencoder.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        return self.autoencoder
    
    def train(self, stock_returns: np.ndarray, epochs: int = 100, batch_size: int = 32):
        """
        Train autoencoder on normalized stock returns
        stock_returns: shape (n_samples, n_stocks)
        """
        # Normalize returns
        normalized_returns = (stock_returns - stock_returns.mean(axis=0)) / stock_returns.std(axis=0)
        
        # Create sequences
        X = []
        for i in range(len(normalized_returns) - self.sequence_length):
            X.append(normalized_returns[i:i + self.sequence_length])
        X = np.array(X)
        
        # Build model if not exists
        if self.autoencoder is None:
            self.build_model(n_features=stock_returns.shape[1])
        
        # Train (autoencoder learns to reconstruct input)
        history = self.autoencoder.fit(
            X, X,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            verbose=0
        )
        
        # Extract correlation matrix from encoder weights
        self._extract_correlation_matrix()
        
        return history
    
    def _extract_correlation_matrix(self):
        """
        Extract correlation matrix from LSTM weights
        As described in the Nature paper
        """
        # Get encoder LSTM layer weights
        lstm_layer = self.encoder.layers[1]  # First LSTM layer
        weights = lstm_layer.get_weights()
        
        # Weight matrix contains correlations
        # W_input shape: (n_features, 4 * units) for LSTM
        W_input = weights[0]
        
        # Extract correlation by computing dot product
        # This captures how stocks influence each other through the LSTM
        correlation = np.dot(W_input, W_input.T)
        
        # Normalize to [-1, 1] range
        correlation = correlation / (np.linalg.norm(W_input, axis=1, keepdims=True) @ 
                                     np.linalg.norm(W_input, axis=1, keepdims=True).T)
        
        self.correlation_matrix = correlation
        
        return correlation
    
    def get_stock_correlations(self, stock_idx: int, top_k: int = 10) -> List[Tuple[int, float]]:
        """Get most correlated stocks to a given stock"""
        if self.correlation_matrix is None:
            raise ValueError("Model must be trained first")
        
        correlations = self.correlation_matrix[stock_idx]
        
        # Get top K correlations (excluding self)
        top_indices = np.argsort(correlations)[::-1]
        top_indices = [idx for idx in top_indices if idx != stock_idx][:top_k]
        
        return [(int(idx), float(correlations[idx])) for idx in top_indices]

