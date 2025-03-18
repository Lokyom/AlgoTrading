"""
Tests pour le module des indicateurs techniques.
"""
import pytest
import pandas as pd
import numpy as np
from algotrading.indicators import TechnicalIndicators


@pytest.fixture
def sample_price_data():
    """Crée un DataFrame de test avec des données de prix."""
    # Créer des données de test
    dates = pd.date_range(start='2023-01-01', periods=100)
    
    # Simulation d'une série de prix avec une tendance
    close_prices = np.linspace(100, 150, 100) + np.random.normal(0, 5, 100)
    
    data = {
        'Open': close_prices - np.random.uniform(0, 2, 100),
        'High': close_prices + np.random.uniform(0, 2, 100),
        'Low': close_prices - np.random.uniform(0, 2, 100),
        'Close': close_prices,
        'Volume': np.random.randint(1000, 10000, 100)
    }
    
    df = pd.DataFrame(data, index=dates)
    return df


def test_sma(sample_price_data):
    """Teste le calcul de la moyenne mobile simple."""
    df = sample_price_data
    
    # Calculer SMA avec différentes périodes
    sma20 = TechnicalIndicators.sma(df, 'Close', 20)
    sma50 = TechnicalIndicators.sma(df, 'Close', 50)
    
    # Vérifier que les longueurs sont correctes
    assert len(sma20) == len(df)
    assert len(sma50) == len(df)
    
    # Vérifier que les 19 premières valeurs de SMA20 sont NaN
    assert sma20.iloc[:19].isna().all()
    
    # Vérifier que la SMA20 a des valeurs non-NaN à partir de l'index 19
    assert not sma20.iloc[19:].isna().any()
    
    # Vérifier que les 49 premières valeurs de SMA50 sont NaN
    assert sma50.iloc[:49].isna().all()
    
    # Vérifier manuellement une valeur de SMA
    manual_sma20 = df['Close'].iloc[0:20].mean()
    assert np.isclose(sma20.iloc[19], manual_sma20)


def test_ema(sample_price_data):
    """Teste le calcul de la moyenne mobile exponentielle."""
    df = sample_price_data
    
    # Calculer EMA avec différentes périodes
    ema20 = TechnicalIndicators.ema(df, 'Close', 20)
    
    # Vérifier que la longueur est correcte
    assert len(ema20) == len(df)
    
    # Vérifier que l'EMA est une série de nombres à virgule flottante
    assert pd.api.types.is_float_dtype(ema20)
    
    # Vérifier que les valeurs sont cohérentes (l'EMA ne dépasse pas les valeurs extrêmes)
    assert ema20.max() <= df['Close'].max() * 1.05  # 5% de marge pour tenir compte des fluctuations
    assert ema20.min() >= df['Close'].min() * 0.95  # 5% de marge


def test_rsi(sample_price_data):
    """Teste le calcul du RSI."""
    df = sample_price_data
    
    # Calculer RSI
    rsi = TechnicalIndicators.rsi(df, 'Close', 14)
    
    # Vérifier que la longueur est correcte
    assert len(rsi) == len(df)
    
    # Vérifier que les 14 premières valeurs sont NaN
    assert rsi.iloc[:14].isna().all()
    
    # Vérifier que le RSI est entre 0 et 100
    valid_rsi = rsi.iloc[14:]
    assert valid_rsi.min() >= 0
    assert valid_rsi.max() <= 100


def test_macd(sample_price_data):
    """Teste le calcul du MACD."""
    df = sample_price_data
    
    # Calculer MACD
    macd_df = TechnicalIndicators.macd(df, 'Close')
    
    # Vérifier que le DataFrame contient les bonnes colonnes
    assert set(macd_df.columns) == {'MACD', 'Signal', 'Histogram'}
    
    # Vérifier que les longueurs sont correctes
    assert len(macd_df) == len(df)
    
    # Vérifier que l'histogramme est égal à MACD - Signal
    calculated_histogram = macd_df['MACD'] - macd_df['Signal']
    pd.testing.assert_series_equal(macd_df['Histogram'], calculated_histogram, check_names=False)


def test_bollinger_bands(sample_price_data):
    """Teste le calcul des bandes de Bollinger."""
    df = sample_price_data
    
    # Calculer les bandes de Bollinger
    bb_df = TechnicalIndicators.bollinger_bands(df, 'Close', 20, 2.0)
    
    # Vérifier que le DataFrame contient les bonnes colonnes
    assert set(bb_df.columns) == {'Middle', 'Upper', 'Lower'}
    
    # Vérifier que les longueurs sont correctes
    assert len(bb_df) == len(df)
    
    # Vérifier que la bande supérieure est toujours au-dessus de la bande médiane
    valid_bb = bb_df.iloc[19:]
    assert (valid_bb['Upper'] >= valid_bb['Middle']).all()
    
    # Vérifier que la bande inférieure est toujours en dessous de la bande médiane
    assert (valid_bb['Lower'] <= valid_bb['Middle']).all()
    
    # Vérifier que la bande médiane est égale à la SMA
    sma20 = TechnicalIndicators.sma(df, 'Close', 20)
    pd.testing.assert_series_equal(bb_df['Middle'], sma20, check_names=False)


def test_add_all_indicators(sample_price_data):
    """Teste l'ajout de tous les indicateurs au DataFrame."""
    df = sample_price_data
    
    # Ajouter tous les indicateurs
    result = TechnicalIndicators.add_all_indicators(df, 'Close')
    
    # Vérifier que toutes les colonnes attendues sont présentes
    expected_columns = [
        'Open', 'High', 'Low', 'Close', 'Volume',
        'SMA20', 'SMA50', 'SMA200', 'EMA20', 'EMA50',
        'RSI', 'MACD', 'MACD_Signal', 'MACD_Histogram',
        'BB_Middle', 'BB_Upper', 'BB_Lower'
    ]
    
    assert all(col in result.columns for col in expected_columns)
    
    # Vérifier que le DataFrame résultant a la même longueur que le DataFrame d'origine
    assert len(result) == len(df) 