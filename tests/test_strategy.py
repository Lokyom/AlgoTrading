"""
Tests pour le module des stratégies de trading.
"""
import pytest
import pandas as pd
import numpy as np
from algotrading.strategy import Strategy, MovingAverageCrossover, RSIStrategy, Position


@pytest.fixture
def sample_price_data():
    """Crée un DataFrame de test avec des données de prix."""
    # Créer des données de test avec une tendance claire pour les tests
    dates = pd.date_range(start='2023-01-01', periods=100)
    
    # Simuler une tendance haussière suivie d'une tendance baissière
    price_trend = np.concatenate([
        np.linspace(100, 150, 50),  # Tendance haussière
        np.linspace(150, 100, 50)   # Tendance baissière
    ])
    
    # Ajouter un peu de bruit
    price_with_noise = price_trend + np.random.normal(0, 2, 100)
    
    data = {
        'Open': price_with_noise - np.random.uniform(0, 1, 100),
        'High': price_with_noise + np.random.uniform(0, 1, 100),
        'Low': price_with_noise - np.random.uniform(0, 1, 100),
        'Close': price_with_noise,
        'Volume': np.random.randint(1000, 10000, 100)
    }
    
    df = pd.DataFrame(data, index=dates)
    return df


def test_moving_average_crossover(sample_price_data):
    """Teste la stratégie de croisement de moyennes mobiles."""
    df = sample_price_data
    
    # Instancier la stratégie
    strategy = MovingAverageCrossover(fast_window=10, slow_window=30)
    
    # Générer les signaux
    signals = strategy.generate_signals(df)
    
    # Vérifier que les signaux sont une série pandas
    assert isinstance(signals, pd.Series)
    
    # Vérifier que les signaux sont -1, 0 ou 1
    assert set(signals.unique()).issubset({-1, 0, 1})
    
    # Vérifier que les signaux changent au moins une fois (étant donné notre tendance simulée)
    assert len(signals[signals != 0]) > 0


def test_rsi_strategy(sample_price_data):
    """Teste la stratégie RSI."""
    df = sample_price_data
    
    # Ajouter le RSI au DataFrame
    from algotrading.indicators import TechnicalIndicators
    df['RSI'] = TechnicalIndicators.rsi(df, 'Close', 14)
    
    # Instancier la stratégie
    strategy = RSIStrategy(window=14, overbought=70, oversold=30)
    
    # Générer les signaux
    signals = strategy.generate_signals(df)
    
    # Vérifier que les signaux sont une série pandas
    assert isinstance(signals, pd.Series)
    
    # Vérifier que les signaux sont -1, 0 ou 1
    assert set(signals.unique()).issubset({-1, 0, 1})


def test_backtest(sample_price_data):
    """Teste la fonction de backtest."""
    df = sample_price_data
    
    # Instancier la stratégie
    strategy = MovingAverageCrossover(fast_window=10, slow_window=30)
    
    # Exécuter le backtest
    results = strategy.backtest(df, initial_capital=10000.0, commission=0.001)
    
    # Vérifier que les résultats sont un DataFrame
    assert isinstance(results, pd.DataFrame)
    
    # Vérifier que les colonnes nécessaires sont présentes
    required_columns = ['Signal', 'Price', 'Position', 'Returns', 
                         'Strategy_Returns', 'Capital', 'Trade', 
                         'Commission', 'Cummax', 'Drawdown']
    
    for col in required_columns:
        assert col in results.columns
    
    # Vérifier que le capital est calculé correctement
    assert not results['Capital'].isna().any()
    
    # Vérifier que le capital initial est correct
    assert results['Capital'].iloc[0] == 10000.0


def test_metrics_calculation(sample_price_data):
    """Teste le calcul des métriques de performance."""
    df = sample_price_data
    
    # Instancier la stratégie
    strategy = MovingAverageCrossover(fast_window=10, slow_window=30)
    
    # Exécuter le backtest
    results = strategy.backtest(df)
    
    # Calculer les métriques
    metrics = strategy.calculate_metrics(results)
    
    # Vérifier que les métriques sont un dictionnaire
    assert isinstance(metrics, dict)
    
    # Vérifier que les métriques nécessaires sont présentes
    required_metrics = ['total_return', 'annual_return', 'annual_volatility',
                         'sharpe_ratio', 'max_drawdown', 'n_trades', 'win_rate']
    
    for metric in required_metrics:
        assert metric in metrics
    
    # Vérifier que les valeurs sont raisonnables
    assert isinstance(metrics['total_return'], float)
    assert isinstance(metrics['annual_return'], float)
    assert isinstance(metrics['annual_volatility'], float)
    assert isinstance(metrics['sharpe_ratio'], float)
    assert isinstance(metrics['max_drawdown'], float)
    assert isinstance(metrics['n_trades'], float)
    assert isinstance(metrics['win_rate'], float)
    
    # Vérifier les bornes pour certaines métriques
    assert metrics['max_drawdown'] <= 0
    assert 0 <= metrics['win_rate'] <= 1


def test_multiple_strategies_comparison(sample_price_data):
    """Teste la comparaison de plusieurs stratégies."""
    df = sample_price_data
    
    # Instancier plusieurs stratégies
    ma_strategy = MovingAverageCrossover(fast_window=10, slow_window=30)
    rsi_strategy = RSIStrategy(window=14, overbought=70, oversold=30)
    
    # Exécuter les backtests
    ma_results = ma_strategy.backtest(df)
    rsi_results = rsi_strategy.backtest(df)
    
    # Calculer les métriques
    ma_metrics = ma_strategy.calculate_metrics(ma_results)
    rsi_metrics = rsi_strategy.calculate_metrics(rsi_results)
    
    # Vérifier que les deux stratégies renvoient des métriques
    assert isinstance(ma_metrics, dict)
    assert isinstance(rsi_metrics, dict)
    
    # Vérifier que les résultats sont comparables (mêmes métriques)
    assert set(ma_metrics.keys()) == set(rsi_metrics.keys()) 