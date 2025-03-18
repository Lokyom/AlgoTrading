"""
Tests pour le module de chargement de données.
"""
import os
import pytest
import pandas as pd
import numpy as np
from algotrading.data_loader import DataLoader


@pytest.fixture
def sample_data_csv(tmp_path):
    """Crée un fichier CSV de test dans un répertoire temporaire."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Créer des données de test
    dates = pd.date_range(start='2023-01-01', periods=10)
    data = {
        'date': dates,
        'Open': np.random.randn(10) * 10 + 100,
        'High': np.random.randn(10) * 10 + 105,
        'Low': np.random.randn(10) * 10 + 95,
        'Close': np.random.randn(10) * 10 + 100,
        'Volume': np.random.randint(1000, 10000, 10)
    }
    df = pd.DataFrame(data)
    
    # Écrire dans un fichier
    csv_path = data_dir / "test_data.csv"
    df.to_csv(csv_path, index=False)
    
    return str(data_dir), "test_data.csv", df


def test_load_csv(sample_data_csv):
    """Teste le chargement d'un fichier CSV."""
    data_dir, filename, original_df = sample_data_csv
    
    # Instancier le DataLoader avec le répertoire temporaire
    loader = DataLoader(data_dir=data_dir)
    
    # Charger les données
    loaded_df = loader.load_csv(filename)
    
    # Vérifier que les données chargées correspondent aux données originales
    assert len(loaded_df) == len(original_df)
    assert set(loaded_df.columns) == set(original_df.columns)
    
    # Vérifier que la colonne date a été convertie en datetime
    assert pd.api.types.is_datetime64_any_dtype(loaded_df['date'])


def test_prepare_price_data(sample_data_csv):
    """Teste la préparation des données de prix."""
    data_dir, filename, original_df = sample_data_csv
    
    # Instancier le DataLoader avec le répertoire temporaire
    loader = DataLoader(data_dir=data_dir)
    
    # Charger et préparer les données
    loaded_df = loader.load_csv(filename)
    prepared_df = loader.prepare_price_data(loaded_df)
    
    # Vérifier que l'index est maintenant la colonne date
    assert prepared_df.index.name == 'date'
    
    # Vérifier que les colonnes ont été correctement renommées
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        assert col in prepared_df.columns


def test_file_not_found():
    """Teste la levée d'exception quand le fichier n'existe pas."""
    loader = DataLoader()
    
    with pytest.raises(FileNotFoundError):
        loader.load_csv("fichier_inexistant.csv")


def test_column_validation():
    """Teste la validation des colonnes dans prepare_price_data."""
    # Créer un DataFrame avec des colonnes manquantes
    df = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=5),
        'Open': np.random.randn(5),
        'Close': np.random.randn(5)
    })
    
    loader = DataLoader()
    
    # Utiliser les colonnes par défaut (devrait lever une exception)
    with pytest.raises(ValueError):
        loader.prepare_price_data(df)
    
    # Spécifier seulement les colonnes disponibles
    custom_cols = {
        'open': 'Open',
        'close': 'Close'
    }
    
    # Devrait toujours lever une exception car toutes les colonnes requises ne sont pas spécifiées
    with pytest.raises(ValueError):
        loader.prepare_price_data(df, ohlcv_cols=custom_cols) 