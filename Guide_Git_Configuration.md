# Guide de Configuration Git pour le Projet AlgoTrading

## Introduction à Git

Git est un système de contrôle de version qui permet de suivre les modifications apportées à votre code au fil du temps. Il vous aide à collaborer, à suivre l'historique de vos modifications et à revenir à des versions antérieures si nécessaire. Pour notre projet AlgoTrading, Git sera essentiel pour gérer le code source et suivre l'évolution des stratégies de trading.

## Pourquoi utiliser Git pour notre projet AlgoTrading?

- **Suivi des modifications**: Chaque stratégie de trading et chaque composant du système sera versionné
- **Sauvegarde**: Votre code est sauvegardé dans un dépôt distant, évitant la perte de données
- **Isolation du développement**: Les nouvelles fonctionnalités ou stratégies peuvent être développées dans des branches séparées
- **Documentation implicite**: L'historique des commits raconte l'histoire du développement
- **Intégration avec les outils**: Git s'intègre facilement avec les outils de CI/CD et de test

## Installation de Git

### Sous Windows

1. Téléchargez l'installateur Git depuis [git-scm.com](https://git-scm.com/download/win)
2. Exécutez l'installateur et suivez les instructions
3. Choisissez les options par défaut à moins que vous ayez des préférences spécifiques
4. À l'étape "Adjusting your PATH environment", sélectionnez "Git from the command line and also from 3rd-party software"
5. Pour l'option "Configuring the line ending conversions", choisissez "Checkout Windows-style, commit Unix-style line endings"
6. Terminez l'installation

### Vérification de l'installation

Pour vérifier que Git est correctement installé, ouvrez PowerShell ou Command Prompt et tapez:

```
git --version
```

Vous devriez voir la version de Git installée, par exemple: `git version 2.35.1.windows.1`

## Configuration initiale de Git

### Configuration de votre identité

Git a besoin de savoir qui vous êtes pour associer vos commits à votre identité. Configurez votre nom et email:

```
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"
```

### Configuration de l'éditeur de texte

Par défaut, Git utilise l'éditeur système pour les messages de commit. Vous pouvez le changer pour un éditeur plus convivial comme VS Code:

```
git config --global core.editor "code --wait"
```

### Vérification de votre configuration

Pour voir toutes vos configurations Git:

```
git config --list
```

## Création du dépôt pour le projet AlgoTrading

### Initialisation d'un nouveau dépôt local

1. Créez un dossier pour votre projet (si ce n'est pas déjà fait):
   ```
   mkdir AlgoTrading
   cd AlgoTrading
   ```

2. Initialisez un dépôt Git dans ce dossier:
   ```
   git init
   ```

### Configuration du dépôt distant (GitHub)

1. Créez un compte sur [GitHub](https://github.com/) si vous n'en avez pas déjà un

2. Créez un nouveau dépôt sur GitHub:
   - Cliquez sur le bouton "+" en haut à droite, puis "New repository"
   - Nommez-le "AlgoTrading"
   - Laissez-le public si vous n'avez pas besoin de confidentialité, sinon choisissez privé
   - Ne cochez pas "Initialize this repository with a README"
   - Cliquez sur "Create repository"

3. Liez votre dépôt local au dépôt distant:
   ```
   git remote add origin https://github.com/votre-nom-utilisateur/AlgoTrading.git
   ```

## Structure initiale du projet

Nous allons créer une structure de base pour notre projet:

1. Créez un fichier README.md:
   ```
   echo "# Projet AlgoTrading" > README.md
   ```

2. Créez un fichier `.gitignore` pour éviter de versionner des fichiers inutiles:
   ```
   # Fichiers Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python
   env/
   build/
   develop-eggs/
   dist/
   downloads/
   eggs/
   .eggs/
   lib/
   lib64/
   parts/
   sdist/
   var/
   *.egg-info/
   .installed.cfg
   *.egg

   # Environnements virtuels
   venv/
   ENV/
   env/

   # Fichiers de configuration locale
   .env
   config.local.ini

   # Dossiers spécifiques à l'IDE
   .idea/
   .vscode/
   *.swp
   *.swo

   # Fichiers de log
   *.log
   logs/

   # Fichiers de base de données
   *.db
   *.sqlite3

   # Clés API et secrets
   *_key.txt
   *_secret.txt
   api_keys.json
   secrets.json
   ```

3. Ajoutez les premiers fichiers au suivi de Git:
   ```
   git add README.md .gitignore
   ```

4. Faites votre premier commit:
   ```
   git commit -m "Initialisation du projet AlgoTrading"
   ```

5. Poussez les modifications vers GitHub:
   ```
   git push -u origin master
   ```
   (Ou `git push -u origin main` si votre branche principale s'appelle "main")

## Travailler avec Git au quotidien

### Flux de travail de base

1. **Vérifiez l'état** de votre dépôt:
   ```
   git status
   ```

2. **Récupérez** les dernières modifications (si vous travaillez avec d'autres personnes):
   ```
   git pull
   ```

3. **Créez une branche** pour une nouvelle fonctionnalité:
   ```
   git checkout -b nouvelle-fonctionnalite
   ```

4. **Faites des modifications** à vos fichiers

5. **Ajoutez** les fichiers modifiés:
   ```
   git add fichier1.py fichier2.py
   ```
   Ou pour ajouter tous les fichiers modifiés:
   ```
   git add .
   ```

6. **Validez** vos modifications:
   ```
   git commit -m "Description de vos modifications"
   ```

7. **Poussez** vos modifications vers GitHub:
   ```
   git push -u origin nouvelle-fonctionnalite
   ```

8. Si nécessaire, **fusionnez** votre branche avec la branche principale:
   ```
   git checkout master
   git merge nouvelle-fonctionnalite
   git push
   ```

### Stratégie de branchement recommandée pour AlgoTrading

Pour notre projet AlgoTrading, nous adopterons une stratégie de branchement simple:

- **master/main**: Branche principale avec code stable et fonctionnel
- **develop**: Branche de développement pour intégrer les nouvelles fonctionnalités
- **feature/xxx**: Branches pour développer de nouvelles fonctionnalités (ex: feature/connecteur-binance)
- **strategy/xxx**: Branches pour développer de nouvelles stratégies de trading
- **bugfix/xxx**: Branches pour corriger des bugs

### Bonnes pratiques pour les commits

- Faites des commits **petits et fréquents** plutôt que de grands commits occasionnels
- Écrivez des **messages de commit clairs et descriptifs**
- Commencez par un verbe à l'impératif: "Ajoute", "Corrige", "Implémente", etc.
- Si possible, référencez des issues ou tâches dans vos messages de commit
- Exemple: "Ajoute le connecteur API pour Binance"

## Git Hook pour l'intégration continue

Pour s'assurer que le code respecte nos normes, nous pouvons configurer un git hook pre-commit qui exécute les tests avant chaque commit:

1. Créez un fichier `.git/hooks/pre-commit`:
   ```bash
   #!/bin/sh
   
   echo "Exécution des tests unitaires..."
   python -m unittest discover -s tests
   
   if [ $? -ne 0 ]; then
       echo "Les tests ont échoué. Commit annulé."
       exit 1
   fi
   
   echo "Vérification du style PEP8..."
   flake8 .
   
   if [ $? -ne 0 ]; then
       echo "Le code ne respecte pas les normes PEP8. Commit annulé."
       exit 1
   fi
   
   exit 0
   ```

2. Rendez le script exécutable:
   ```
   chmod +x .git/hooks/pre-commit
   ```

## Conclusion

Vous avez maintenant configuré Git pour votre projet AlgoTrading! Voici un résumé des commandes les plus utiles:

- `git status` : Voir l'état de vos fichiers
- `git add fichier` : Ajouter un fichier au suivi
- `git commit -m "message"` : Valider les modifications
- `git push` : Envoyer les modifications au dépôt distant
- `git pull` : Récupérer les modifications du dépôt distant
- `git checkout -b branche` : Créer et passer à une nouvelle branche
- `git checkout branche` : Passer à une branche existante
- `git merge branche` : Fusionner une branche dans la branche actuelle
- `git log` : Voir l'historique des commits

Pour approfondir vos connaissances sur Git, je recommande ces ressources:
- [Pro Git Book](https://git-scm.com/book/fr/v2) (gratuit et en français)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

N'hésitez pas à consulter ce guide à chaque fois que vous avez besoin de vous rappeler une commande Git. Bonne programmation! 