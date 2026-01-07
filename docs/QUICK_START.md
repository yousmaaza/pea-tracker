# Quick Start Guide - PEA Tracker

Guide de démarrage rapide pour commencer à utiliser PEA Tracker avec pip-mode.

## Installation initiale

### 1. Configuration pip-mode (recommandé)

```bash
# Option A : Installation automatique dans votre shell
./scripts/install-pip-mode.sh

# Option B : Utilisation directe
./scripts/pip-mode.sh status
```

### 2. Vérification de l'installation

```bash
# Tester que tout fonctionne
./scripts/test-pip-mode.sh

# Vérifier la configuration actuelle
./scripts/pip-mode.sh status
```

## Utilisation quotidienne

### Mode développement (PyPI standard)

```bash
# 1. Basculer en mode standard
./scripts/pip-mode.sh standard

# 2. Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer les agents
claude-code agent run market-watcher-pea
```

### Mode production (Nexus)

```bash
# 1. Basculer en mode Nexus
./scripts/pip-mode.sh nexus

# 2. Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

## Commandes Claude Code

### Via la commande /pip-mode

```bash
# Dans Claude Code
/pip-mode status
/pip-mode standard
/pip-mode nexus
```

### Workflow complet avec Claude Code

```bash
# 1. Démarrer Claude Code
claude-code

# 2. Configurer pip
/pip-mode standard

# 3. Lancer un agent
invoke @market-watcher-pea
```

## Commandes courantes

### Vérification

```bash
# Status pip actuel
./scripts/pip-mode.sh status

# Vérifier les variables d'environnement
echo $PIP_INDEX_URL
echo $PIP_TRUSTED_HOST

# Lister les packages installés
pip list
```

### Basculement de mode

```bash
# PyPI standard (public)
./scripts/pip-mode.sh standard

# Nexus (interne)
./scripts/pip-mode.sh nexus
```

### Dépannage

```bash
# Tester l'installation
./scripts/test-pip-mode.sh

# Réinstaller pip-mode
./scripts/install-pip-mode.sh

# Vérifier le script
cat scripts/pip-mode.sh
```

## Environnements virtuels Python

### Création

```bash
# Python 3 standard
python3 -m venv venv

# Spécifier une version
python3.11 -m venv venv
```

### Activation

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Désactivation

```bash
deactivate
```

## Workflow recommandé

### Nouveau projet

```bash
# 1. Configuration pip
./scripts/pip-mode.sh standard
./scripts/pip-mode.sh status

# 2. Environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installation des dépendances
pip install --upgrade pip
pip install -r requirements.txt

# 4. Vérification
pip list
python --version
```

### Développement quotidien

```bash
# 1. Activer l'environnement
source venv/bin/activate

# 2. Vérifier le mode pip
./scripts/pip-mode.sh status

# 3. Installer de nouveaux packages
pip install package-name

# 4. Sauvegarder les dépendances
pip freeze > requirements.txt
```

### Mise à jour des dépendances

```bash
# 1. Activer l'environnement
source venv/bin/activate

# 2. Mettre à jour pip
pip install --upgrade pip

# 3. Mettre à jour les packages
pip install --upgrade -r requirements.txt

# 4. Sauvegarder
pip freeze > requirements.txt
```

## Intégration avec les agents

### Market Watcher

```bash
# 1. Préparer l'environnement
./scripts/pip-mode.sh standard
source venv/bin/activate

# 2. Lancer l'agent
claude-code agent run market-watcher-pea
```

### Portfolio Advisor (à venir)

```bash
# 1. Préparer l'environnement
./scripts/pip-mode.sh standard
source venv/bin/activate

# 2. Lancer l'agent
claude-code agent run portfolio-advisor
```

## Automatisation

### Cron job pour Market Watcher

```bash
# Éditer crontab
crontab -e

# Ajouter cette ligne (exécution quotidienne à 8h)
0 8 * * 1-5 cd /path/to/claude-project && ./scripts/pip-mode.sh standard && source venv/bin/activate && claude-code agent run market-watcher-pea
```

### Script d'automatisation

```bash
#!/bin/bash
# run-market-watcher.sh

set -e

# Configuration
./scripts/pip-mode.sh standard

# Environnement
source venv/bin/activate

# Exécution
claude-code agent run market-watcher-pea
```

## Troubleshooting rapide

### Problème : pip installe depuis le mauvais dépôt

```bash
# Vérifier la configuration
./scripts/pip-mode.sh status

# Réinitialiser
./scripts/pip-mode.sh standard

# Vérifier
pip config list
```

### Problème : Erreur SSL avec Nexus

```bash
# S'assurer que le mode Nexus est activé
./scripts/pip-mode.sh nexus

# Vérifier la variable
echo $PIP_TRUSTED_HOST
```

### Problème : Commande pip-mode non trouvée

```bash
# Option 1 : Utiliser le chemin complet
./scripts/pip-mode.sh status

# Option 2 : Réinstaller
./scripts/install-pip-mode.sh

# Option 3 : Recharger le shell
source ~/.zshrc  # ou source ~/.bashrc
```

### Problème : Environnement virtuel corrompu

```bash
# Supprimer l'environnement
rm -rf venv

# Recréer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Ressources

### Documentation
- [Guide complet pip-mode](./pip-mode-guide.md)
- [Architecture MCP](./architecture/mcp-integration.md)
- [Guide d'installation](./SETUP_GUIDE.md)
- [CLAUDE.md](../CLAUDE.md) - Documentation projet complète

### Scripts
- `scripts/pip-mode.sh` - Script principal
- `scripts/install-pip-mode.sh` - Installation automatique
- `scripts/test-pip-mode.sh` - Suite de tests

### Commandes Claude
- `.claude/commands/pip-mode.md` - Définition de la commande

## Support

### Vérification santé du système

```bash
# Python
python3 --version
which python3

# pip
pip --version
which pip

# Environnement virtuel
which python  # doit pointer vers venv/bin/python

# pip-mode
./scripts/test-pip-mode.sh
```

### Logs et debug

```bash
# Verbose pip
pip install --verbose package-name

# Debug pip
pip install --debug package-name

# Afficher la config pip
pip config list
pip config debug
```

---

**Version** : 1.0.0
**Dernière mise à jour** : 2026-01-07
**Pour plus de détails** : Voir [pip-mode-guide.md](./pip-mode-guide.md)
