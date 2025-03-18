"""
Module définissant les stratégies de trading.
"""
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Union, Tuple
from enum import Enum


class Position(Enum):
    """Enum représentant les positions possibles."""
    NONE = 0
    LONG = 1
    SHORT = -1


class Strategy(ABC):
    """Classe abstraite pour toutes les stratégies de trading."""
    
    def __init__(self, name: str):
        """
        Initialise une stratégie de trading.
        
        Args:
            name: Nom de la stratégie.
        """
        self.name = name
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Génère les signaux de trading.
        
        Args:
            data: DataFrame contenant les données de prix et les indicateurs.
            
        Returns:
            Série pandas contenant les signaux (-1 pour vendre, 0 pour ne rien faire, 1 pour acheter).
        """
        pass
    
    def backtest(self, data: pd.DataFrame, initial_capital: float = 10000.0,
                position_size: float = 1.0, commission: float = 0.0) -> pd.DataFrame:
        """
        Effectue un backtest de la stratégie.
        
        Args:
            data: DataFrame contenant les données de prix.
            initial_capital: Capital initial.
            position_size: Taille de la position (proportion du capital).
            commission: Commission par transaction (proportion).
            
        Returns:
            DataFrame contenant les résultats du backtest.
        """
        # Générer les signaux
        signals = self.generate_signals(data)
        
        # Créer un DataFrame pour les résultats
        results = pd.DataFrame(index=data.index)
        
        # Ajouter les signaux au DataFrame
        results['Signal'] = signals
        
        # Ajouter les prix au DataFrame
        results['Price'] = data['Close']
        
        # Calculer les positions (cumulative des signaux)
        results['Position'] = signals.cumsum().map({
            -1: Position.SHORT.value,
            0: Position.NONE.value,
            1: Position.LONG.value
        })
        
        # Calculer les rendements de la stratégie
        results['Returns'] = results['Price'].pct_change()
        
        # Calculer les rendements de la stratégie
        results['Strategy_Returns'] = results['Position'].shift(1) * results['Returns']
        
        # Calculer le capital
        results['Capital'] = initial_capital * (1 + results['Strategy_Returns']).cumprod()
        
        # Calculer les transactions
        results['Trade'] = results['Position'].diff().abs()
        
        # Calculer le coût des commissions
        results['Commission'] = results['Trade'] * results['Price'] * commission
        
        # Soustraire les commissions du capital
        if commission > 0:
            results['Capital'] = results['Capital'] - results['Commission'].cumsum()
        
        # Calculer le drawdown
        results['Cummax'] = results['Capital'].cummax()
        results['Drawdown'] = (results['Capital'] - results['Cummax']) / results['Cummax']
        
        return results
    
    def calculate_metrics(self, results: pd.DataFrame) -> Dict[str, float]:
        """
        Calcule les métriques de performance.
        
        Args:
            results: DataFrame contenant les résultats du backtest.
            
        Returns:
            Dictionnaire contenant les métriques de performance.
        """
        # Calculer le rendement total
        total_return = (results['Capital'].iloc[-1] / results['Capital'].iloc[0]) - 1
        
        # Calculer le rendement annualisé
        n_years = len(results) / 252  # Supposer 252 jours de trading par an
        annual_return = (1 + total_return) ** (1 / n_years) - 1
        
        # Calculer la volatilité annualisée
        annual_volatility = results['Strategy_Returns'].std() * np.sqrt(252)
        
        # Calculer le ratio de Sharpe (rendement / risque)
        sharpe_ratio = annual_return / annual_volatility if annual_volatility > 0 else 0
        
        # Calculer le drawdown maximum
        max_drawdown = results['Drawdown'].min()
        
        # Calculer le nombre de transactions
        n_trades = results['Trade'].sum()
        
        # Calculer le taux de réussite
        winning_trades = results[results['Strategy_Returns'] > 0]['Strategy_Returns'].count()
        losing_trades = results[results['Strategy_Returns'] < 0]['Strategy_Returns'].count()
        win_rate = winning_trades / (winning_trades + losing_trades) if (winning_trades + losing_trades) > 0 else 0
        
        # Retourner les métriques
        return {
            'total_return': total_return,
            'annual_return': annual_return,
            'annual_volatility': annual_volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'n_trades': n_trades,
            'win_rate': win_rate
        }


class MovingAverageCrossover(Strategy):
    """Stratégie de croisement de moyennes mobiles."""
    
    def __init__(self, fast_window: int = 20, slow_window: int = 50):
        """
        Initialise une stratégie de croisement de moyennes mobiles.
        
        Args:
            fast_window: Période de la moyenne mobile rapide.
            slow_window: Période de la moyenne mobile lente.
        """
        super().__init__(f"MA_Crossover_{fast_window}_{slow_window}")
        self.fast_window = fast_window
        self.slow_window = slow_window
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Génère les signaux de trading basés sur le croisement des moyennes mobiles.
        
        Args:
            data: DataFrame contenant les données de prix.
            
        Returns:
            Série pandas contenant les signaux (-1 pour vendre, 0 pour ne rien faire, 1 pour acheter).
        """
        # Calculer les moyennes mobiles
        fast_ma = data['Close'].rolling(window=self.fast_window).mean()
        slow_ma = data['Close'].rolling(window=self.slow_window).mean()
        
        # Initialiser les signaux à 0
        signals = pd.Series(0, index=data.index)
        
        # Générer les signaux de croisement
        signals[fast_ma > slow_ma] = 1  # Signal d'achat
        signals[fast_ma < slow_ma] = -1  # Signal de vente
        
        # Supprime les NaN
        signals = signals.fillna(0)
        
        # Convertir les positions en signaux (uniquement les changements)
        signals = signals.diff()
        signals = signals.fillna(0)
        
        return signals


class RSIStrategy(Strategy):
    """Stratégie basée sur l'indice de force relative (RSI)."""
    
    def __init__(self, window: int = 14, overbought: int = 70, oversold: int = 30):
        """
        Initialise une stratégie RSI.
        
        Args:
            window: Période du RSI.
            overbought: Niveau de surachat.
            oversold: Niveau de survente.
        """
        super().__init__(f"RSI_{window}_{oversold}_{overbought}")
        self.window = window
        self.overbought = overbought
        self.oversold = oversold
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Génère les signaux de trading basés sur le RSI.
        
        Args:
            data: DataFrame contenant les données de prix.
            
        Returns:
            Série pandas contenant les signaux (-1 pour vendre, 0 pour ne rien faire, 1 pour acheter).
        """
        from algotrading.indicators import TechnicalIndicators
        
        # Calculer le RSI si nécessaire
        if 'RSI' not in data.columns:
            rsi = TechnicalIndicators.rsi(data, 'Close', self.window)
        else:
            rsi = data['RSI']
            
        # Initialiser les signaux à 0
        signals = pd.Series(0, index=data.index)
        
        # Générer les signaux RSI
        signals[(rsi < self.oversold)] = 1  # Signal d'achat si RSI < oversold
        signals[(rsi > self.overbought)] = -1  # Signal de vente si RSI > overbought
        
        # Supprimer les NaN
        signals = signals.fillna(0)
        
        # Convertir les positions en signaux (uniquement les changements)
        previous_position = 0
        for i in range(len(signals)):
            current_signal = signals.iloc[i]
            
            # Si le signal est identique à la position précédente, ne rien faire
            if current_signal == previous_position:
                signals.iloc[i] = 0
            else:
                previous_position = current_signal
                
        return signals 