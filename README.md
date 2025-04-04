# AlgoTrading

Un système de trading algorithmique pour analyser les marchés financiers et exécuter des stratégies de trading automatisées.

## Fonctionnalités

- Analyse technique des données de marché
- Backtesting de stratégies de trading
- Exécution automatisée des ordres
- Visualisation des performances

## Installation

Assurez-vous d'avoir Python 3.13+ installé, puis exécutez :

```bash
# Cloner le dépôt
git clone https://github.com/votre-utilisateur/AlgoTrading.git
cd AlgoTrading

# Créer et activer l'environnement virtuel
python -m venv venv
# Sur Windows
.\venv\Scripts\activate.bat
# Sur Unix/MacOS
# source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Installer les hooks pre-commit
pre-commit install
```

## Structure du projet

```
AlgoTrading/
├── algotrading/          # Package principal
├── data/                 # Données et datasets
├── notebooks/            # Jupyter notebooks pour l'analyse
├── tests/                # Tests unitaires et d'intégration
├── .github/              # Configuration GitHub Actions
├── .pre-commit-config.yaml  # Configuration pre-commit
├── requirements.txt      # Dépendances du projet
└── README.md             # Ce fichier
```

## Développement

Pour contribuer au projet :

1. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nom-fonctionnalite`)
2. Committez vos changements (`git commit -am 'Ajout de fonctionnalité'`)
3. Poussez la branche (`git push origin feature/nom-fonctionnalite`)
4. Créez une Pull Request

## Tests

Pour exécuter les tests :

```bash
pytest
```

Pour vérifier la couverture de code :

```bash
pytest --cov=algotrading
```

## Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
