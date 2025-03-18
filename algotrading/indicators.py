"""
Module pour calculer différents indicateurs techniques sur les données financières.
"""
import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Union, Tuple


class TechnicalIndicators:
    """Classe pour calculer les indicateurs techniques sur un DataFrame de prix."""
    
    @staticmethod
    def sma(data: pd.DataFrame, column: str = 'Close', window: int = 20) -> pd.Series:
        """
        Calcule la moyenne mobile simple (SMA).
        
        Args:
            data: DataFrame contenant les données de prix.
            column: Nom de la colonne à utiliser pour le calcul.
            window: Période de la moyenne mobile.
            
        Returns:
            Série pandas contenant la SMA.
        """
        return data[column].rolling(window=window).mean()
    
    @staticmethod
    def ema(data: pd.DataFrame, column: str = 'Close', window: int = 20) -> pd.Series:
        """
        Calcule la moyenne mobile exponentielle (EMA).
        
        Args:
            data: DataFrame contenant les données de prix.
            column: Nom de la colonne à utiliser pour le calcul.
            window: Période de la moyenne mobile.
            
        Returns:
            Série pandas contenant l'EMA.
        """
        return data[column].ewm(span=window, adjust=False).mean()
    
    @staticmethod
    def rsi(data: pd.DataFrame, column: str = 'Close', window: int = 14) -> pd.Series:
        """
        Calcule l'indice de force relative (RSI).
        
        Args:
            data: DataFrame contenant les données de prix.
            column: Nom de la colonne à utiliser pour le calcul.
            window: Période du RSI.
            
        Returns:
            Série pandas contenant le RSI.
        """
        # Calculer les variations de prix
        delta = data[column].diff()
        
        # Séparer les gains et les pertes
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        # Calculer la moyenne mobile des gains et des pertes
        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()
        
        # Calculer le RS (Relative Strength)
        rs = avg_gain / avg_loss
        
        # Calculer le RSI
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def macd(data: pd.DataFrame, column: str = 'Close', 
             fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> pd.DataFrame:
        """
        Calcule le MACD (Moving Average Convergence Divergence).
        
        Args:
            data: DataFrame contenant les données de prix.
            column: Nom de la colonne à utiliser pour le calcul.
            fast_period: Période de l'EMA rapide.
            slow_period: Période de l'EMA lente.
            signal_period: Période de l'EMA du signal.
            
        Returns:
            DataFrame contenant les colonnes 'MACD', 'Signal' et 'Histogram'.
        """
        # Calculer les EMA rapide et lente
        fast_ema = TechnicalIndicators.ema(data, column, fast_period)
        slow_ema = TechnicalIndicators.ema(data, column, slow_period)
        
        # Calculer le MACD
        macd_line = fast_ema - slow_ema
        
        # Calculer la ligne de signal
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        
        # Calculer l'histogramme
        histogram = macd_line - signal_line
        
        # Créer un DataFrame avec les résultats
        result = pd.DataFrame({
            'MACD': macd_line,
            'Signal': signal_line,
            'Histogram': histogram
        })
        
        return result
    
    @staticmethod
    def bollinger_bands(data: pd.DataFrame, column: str = 'Close', 
                        window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
        """
        Calcule les bandes de Bollinger.
        
        Args:
            data: DataFrame contenant les données de prix.
            column: Nom de la colonne à utiliser pour le calcul.
            window: Période de la moyenne mobile.
            num_std: Nombre d'écarts-types pour les bandes.
            
        Returns:
            DataFrame contenant les colonnes 'Middle', 'Upper', 'Lower'.
        """
        # Calculer la SMA pour la bande médiane
        middle_band = TechnicalIndicators.sma(data, column, window)
        
        # Calculer l'écart-type
        std = data[column].rolling(window=window).std()
        
        # Calculer les bandes supérieure et inférieure
        upper_band = middle_band + (std * num_std)
        lower_band = middle_band - (std * num_std)
        
        # Créer un DataFrame avec les résultats
        result = pd.DataFrame({
            'Middle': middle_band,
            'Upper': upper_band,
            'Lower': lower_band
        })
        
        return result
    
    @staticmethod
    def add_all_indicators(data: pd.DataFrame, column: str = 'Close') -> pd.DataFrame:
        """
        Ajoute tous les indicateurs techniques au DataFrame.
        
        Args:
            data: DataFrame contenant les données de prix.
            column: Nom de la colonne à utiliser pour le calcul des indicateurs.
            
        Returns:
            DataFrame avec tous les indicateurs ajoutés.
        """
        # Créer une copie du DataFrame pour éviter de modifier l'original
        result = data.copy()
        
        # Ajouter SMA à différentes périodes
        result['SMA20'] = TechnicalIndicators.sma(data, column, 20)
        result['SMA50'] = TechnicalIndicators.sma(data, column, 50)
        result['SMA200'] = TechnicalIndicators.sma(data, column, 200)
        
        # Ajouter EMA à différentes périodes
        result['EMA20'] = TechnicalIndicators.ema(data, column, 20)
        result['EMA50'] = TechnicalIndicators.ema(data, column, 50)
        
        # Ajouter RSI
        result['RSI'] = TechnicalIndicators.rsi(data, column)
        
        # Ajouter MACD
        macd_df = TechnicalIndicators.macd(data, column)
        result['MACD'] = macd_df['MACD']
        result['MACD_Signal'] = macd_df['Signal']
        result['MACD_Histogram'] = macd_df['Histogram']
        
        # Ajouter bandes de Bollinger
        bb_df = TechnicalIndicators.bollinger_bands(data, column)
        result['BB_Middle'] = bb_df['Middle']
        result['BB_Upper'] = bb_df['Upper']
        result['BB_Lower'] = bb_df['Lower']
        
        return result 