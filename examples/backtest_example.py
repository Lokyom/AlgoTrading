#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemple de backtest d'une stratégie de trading.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Ajout du répertoire parent au chemin de recherche des modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from algotrading.data_loader import DataLoader
from algotrading.indicators import TechnicalIndicators
from algotrading.strategy import MovingAverageCrossover, RSIStrategy


def generate_sample_data(output_file: str, periods: int = 1000):
    """
    Génère des données de prix aléatoires avec une tendance.
    
    Args:
        output_file: Chemin du fichier de sortie.
        periods: Nombre de périodes à générer.
    """
    print("Génération de données de test...")
    
    # Créer des dates
    dates = pd.date_range(start='2020-01-01', periods=periods)
    
    # Simuler un prix avec une tendance et des cycles
    time = np.arange(periods)
    trend = 0.1 * time  # Tendance haussière
    cycle1 = 10 * np.sin(time / 100)  # Cycle long
    cycle2 = 5 * np.sin(time / 20)  # Cycle moyen
    noise = np.random.normal(0, 5, periods)  # Bruit aléatoire
    
    # Combinaison des composantes
    close_prices = 100 + trend + cycle1 + cycle2 + noise
    
    # Création des autres colonnes de prix
    data = {
        'date': dates,
        'Open': close_prices - np.random.uniform(0, 2, periods),
        'High': close_prices + np.random.uniform(0, 2, periods),
        'Low': close_prices - np.random.uniform(0, 2, periods),
        'Close': close_prices,
        'Volume': np.random.randint(1000, 10000, periods)
    }
    
    # Création du DataFrame
    df = pd.DataFrame(data)
    
    # Enregistrement des données
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    
    print(f"Données générées et enregistrées dans {output_file}")
    return df


def run_backtest():
    """Exécute un backtest sur des données générées."""
    # Définir le fichier de données
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    data_file = os.path.join(data_dir, 'sample_prices.csv')
    
    # Générer les données si elles n'existent pas
    if not os.path.exists(data_file):
        df_raw = generate_sample_data(data_file)
    else:
        # Charger les données
        loader = DataLoader()
        df_raw = loader.load_csv('sample_prices.csv')
    
    # Préparer les données
    df = loader.prepare_price_data(df_raw)
    
    # Ajouter les indicateurs techniques
    df = TechnicalIndicators.add_all_indicators(df)
    
    # Initialiser les stratégies
    ma_strategy = MovingAverageCrossover(fast_window=20, slow_window=50)
    rsi_strategy = RSIStrategy(window=14, overbought=70, oversold=30)
    
    # Exécuter les backtests
    print("\nExécution du backtest avec la stratégie de croisement de moyennes mobiles...")
    ma_results = ma_strategy.backtest(df, initial_capital=10000.0, commission=0.001)
    
    print("Exécution du backtest avec la stratégie RSI...")
    rsi_results = rsi_strategy.backtest(df, initial_capital=10000.0, commission=0.001)
    
    # Calculer les métriques
    ma_metrics = ma_strategy.calculate_metrics(ma_results)
    rsi_metrics = rsi_strategy.calculate_metrics(rsi_results)
    
    # Afficher les résultats
    print("\nRésultats pour la stratégie de croisement de moyennes mobiles:")
    for key, value in ma_metrics.items():
        print(f"{key}: {value:.4f}")
    
    print("\nRésultats pour la stratégie RSI:")
    for key, value in rsi_metrics.items():
        print(f"{key}: {value:.4f}")
    
    # Visualiser les résultats
    visualize_results(df, ma_results, rsi_results)


def visualize_results(df, ma_results, rsi_results):
    """
    Visualise les résultats des backtests.
    
    Args:
        df: DataFrame contenant les données de prix et les indicateurs.
        ma_results: Résultats du backtest de la stratégie de moyennes mobiles.
        rsi_results: Résultats du backtest de la stratégie RSI.
    """
    print("\nCréation des graphiques...")
    
    # Configuration des graphiques
    sns.set(style="darkgrid")
    plt.figure(figsize=(14, 10))
    
    # Graphique des prix et des moyennes mobiles
    plt.subplot(3, 1, 1)
    plt.plot(df.index, df['Close'], label='Prix de clôture')
    plt.plot(df.index, df['SMA20'], label='SMA 20')
    plt.plot(df.index, df['SMA50'], label='SMA 50')
    plt.title('Prix et moyennes mobiles')
    plt.legend()
    
    # Graphique du RSI
    plt.subplot(3, 1, 2)
    plt.plot(df.index, df['RSI'], label='RSI')
    plt.axhline(y=70, color='r', linestyle='-', alpha=0.3)
    plt.axhline(y=30, color='g', linestyle='-', alpha=0.3)
    plt.title('RSI')
    plt.legend()
    
    # Graphique des performances des stratégies
    plt.subplot(3, 1, 3)
    plt.plot(ma_results.index, ma_results['Capital'], label='Stratégie MA')
    plt.plot(rsi_results.index, rsi_results['Capital'], label='Stratégie RSI')
    plt.title('Performance des stratégies')
    plt.legend()
    
    # Ajuster la mise en page
    plt.tight_layout()
    
    # Enregistrer le graphique
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'backtest_results.png')
    plt.savefig(output_file)
    
    print(f"Graphique enregistré dans {output_file}")
    
    # Afficher le graphique
    plt.show()


if __name__ == '__main__':
    run_backtest() 