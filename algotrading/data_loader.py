"""
Module pour charger et préparer les données financières.
"""
import os
import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Union, Tuple


class DataLoader:
    """Classe pour charger et préparer les données financières."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialise le chargeur de données.
        
        Args:
            data_dir: Répertoire contenant les fichiers de données.
        """
        self.data_dir = data_dir
        
    def load_csv(self, filename: str) -> pd.DataFrame:
        """
        Charge les données à partir d'un fichier CSV.
        
        Args:
            filename: Nom du fichier dans le répertoire de données.
            
        Returns:
            DataFrame contenant les données chargées.
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas.
        """
        file_path = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")
            
        df = pd.read_csv(file_path)
        
        # Conversion des dates si une colonne de date est détectée
        date_columns = [col for col in df.columns if 'date' in col.lower()]
        for col in date_columns:
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass
                
        return df
    
    def prepare_price_data(self, df: pd.DataFrame, 
                          date_col: str = 'date',
                          ohlcv_cols: Optional[Dict[str, str]] = None) -> pd.DataFrame:
        """
        Prépare les données de prix pour l'analyse.
        
        Args:
            df: DataFrame contenant les données brutes.
            date_col: Nom de la colonne contenant les dates.
            ohlcv_cols: Dictionnaire mappant les types de colonnes aux noms de colonnes.
                        Doit contenir les clés 'open', 'high', 'low', 'close', 'volume'.
                        
        Returns:
            DataFrame préparé pour l'analyse.
        """
        # Colonnes par défaut si non spécifiées
        if ohlcv_cols is None:
            ohlcv_cols = {
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume'
            }
            
        # Vérifier que toutes les colonnes existent
        for col_type, col_name in ohlcv_cols.items():
            if col_name not in df.columns:
                raise ValueError(f"La colonne {col_name} pour {col_type} n'existe pas dans le DataFrame.")
                
        # Définir l'index comme la colonne de date
        if date_col in df.columns:
            df = df.set_index(date_col)
            
        # Renommer les colonnes pour standardisation
        rename_dict = {v: k.capitalize() for k, v in ohlcv_cols.items()}
        df = df.rename(columns=rename_dict)
        
        # Trier par date
        df = df.sort_index()
        
        return df 