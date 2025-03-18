# Guide de configuration de l'Intégration Continue et de l'Environnement Python

## 1. Environnement Virtuel Python

### Qu'est-ce qu'un environnement virtuel Python ?

Un environnement virtuel Python est un espace isolé où vous pouvez installer des packages Python et leurs dépendances sans affecter l'installation Python principale de votre système ou d'autres environnements virtuels. C'est essentiel pour :

- **Éviter les conflits de dépendances** entre différents projets
- **Assurer la reproductibilité** de votre environnement de développement
- **Faciliter le déploiement** en listant clairement toutes les dépendances
- **Maintenir votre projet propre** en isolant ses besoins spécifiques

### Installation et configuration de l'environnement virtuel

#### 1. Installation du package virtualenv (si nécessaire)

```bash
pip install virtualenv
```

#### 2. Création de l'environnement virtuel

Dans le dossier racine de votre projet AlgoTrading :

```bash
# Option 1 : Avec virtualenv
virtualenv venv

# Option 2 : Avec le module venv intégré à Python (Python 3.3+)
python -m venv venv
```

#### 3. Activation de l'environnement virtuel

**Sous Windows (PowerShell) :**
```bash
.\venv\Scripts\Activate.ps1
```

**Sous Windows (Cmd) :**
```bash
venv\Scripts\activate.bat
```

**Sous macOS/Linux :**
```bash
source venv/bin/activate
```

Une fois activé, vous verrez le nom de l'environnement virtuel `(venv)` au début de votre ligne de commande.

#### 4. Installation des dépendances initiales

```bash
pip install numpy pandas matplotlib scikit-learn pytest flake8 black jupyter
```

#### 5. Création du fichier requirements.txt

Ce fichier liste toutes les dépendances du projet :

```bash
pip freeze > requirements.txt
```

### Bonnes pratiques pour l'environnement virtuel

- **Toujours activer** l'environnement virtuel avant de travailler sur le projet
- **Mettre à jour régulièrement** le fichier requirements.txt quand vous installez de nouveaux packages
- **Ne jamais versionner** le dossier venv dans Git (déjà inclus dans notre .gitignore)
- **Documenter** les étapes d'installation pour d'autres développeurs

## 2. Intégration Continue (CI)

### Qu'est-ce que l'intégration continue ?

L'intégration continue (CI) est une pratique de développement qui consiste à intégrer régulièrement les modifications de code dans un dépôt partagé, puis à exécuter automatiquement des tests pour détecter rapidement les problèmes. Pour notre projet AlgoTrading, la CI nous permettra de :

- **Exécuter automatiquement les tests** à chaque push
- **Vérifier le style du code** selon les conventions établies
- **Mesurer la couverture de tests**
- **Détecter les problèmes tôt** dans le cycle de développement
- **Maintenir la qualité du code** de façon constante

### Configuration de GitHub Actions pour l'intégration continue

Nous utiliserons GitHub Actions pour configurer notre pipeline CI car il s'intègre directement à notre dépôt GitHub.

#### 1. Création du dossier pour les workflows

```bash
mkdir -p .github/workflows
```

#### 2. Création du fichier de configuration CI

Créez un fichier `.github/workflows/python-tests.yml` :

```yaml
name: Python Tests

on:
  push:
    branches: [ master, main, develop ]
  pull_request:
    branches: [ master, main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install pytest flake8 pytest-cov
    
    - name: Lint with flake8
      run: |
        # Arrêt en cas d'erreurs de syntaxe ou de variables non définies
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # Avertissements comme erreurs
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Test with pytest
      run: |
        pytest --cov=./ --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

### 3. Configuration des tests locaux pour préparer l'intégration continue

#### Structure des tests

Créez une structure de dossiers pour vos tests :

```
AlgoTrading/
├── algotrading/
│   ├── __init__.py
│   ├── data/
│   ├── strategies/
│   └── ...
├── tests/
│   ├── __init__.py
│   ├── test_data.py
│   ├── test_strategies.py
│   └── ...
└── ...
```

#### Création d'un test simple pour vérifier la configuration

Créez le fichier `tests/__init__.py` (vide) et le fichier `tests/test_setup.py` :

```python
def test_environment_setup():
    """Test simple pour vérifier que l'environnement de test fonctionne."""
    assert True
```

### 4. Intégration avec les hooks Git locaux

Pour garantir que les tests et vérifications sont également exécutés localement avant chaque commit, nous pouvons utiliser pre-commit :

#### Installation de pre-commit

```bash
pip install pre-commit
```

#### Configuration de pre-commit

Créez un fichier `.pre-commit-config.yaml` à la racine du projet :

```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
        args: ['--max-line-length=127']

-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black
        args: ['--line-length=127']
```

#### Installation des hooks Git

```bash
pre-commit install
```

## 3. Structure initiale du projet Python

Pour bien démarrer votre projet AlgoTrading, nous allons créer une structure de base :

```
AlgoTrading/
├── algotrading/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── connectors/
│   │   └── processors/
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── indicators/
│   │   └── models/
│   ├── backtesting/
│   │   ├── __init__.py
│   │   └── engine.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   └── test_setup.py
├── notebooks/
├── docs/
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── .gitignore
├── .pre-commit-config.yaml
├── README.md
├── requirements.txt
└── setup.py
```

## 4. Mise en œuvre

Maintenant que nous avons expliqué les concepts et préparé les fichiers de configuration, exécutons les commandes nécessaires pour configurer votre environnement de développement.

### Étapes de mise en œuvre

1. Créez l'environnement virtuel Python
2. Activez l'environnement virtuel
3. Installez les dépendances initiales
4. Créez la structure de base du projet
5. Configurez l'intégration continue avec GitHub Actions
6. Mettez en place pre-commit pour les vérifications locales
7. Validez la configuration en exécutant un test simple

### Avantages de cette configuration

- **Isolation** : Votre projet a ses propres dépendances, évitant les conflits
- **Qualité du code** : Les vérifications automatiques maintiennent des standards élevés
- **Détection précoce des problèmes** : Les tests échouant rapidement vous font gagner du temps
- **Reproductibilité** : N'importe qui peut recréer exactement votre environnement
- **Professionnalisme** : Cette approche suit les meilleures pratiques de l'industrie

En suivant ces étapes, vous aurez un environnement de développement solide et professionnel pour votre projet AlgoTrading, avec une intégration continue et un environnement Python bien configurés. 