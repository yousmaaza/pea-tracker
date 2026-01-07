# Guide d'utilisation : pip-mode

## Vue d'ensemble

`pip-mode` est un utilitaire qui permet de basculer facilement entre le dépôt PyPI standard et le dépôt Nexus interne pour la gestion des packages Python.

## Installation

Le script est déjà disponible dans le projet :
```bash
scripts/pip-mode.sh
```

Pour l'utiliser globalement, ajoutez ceci à votre `~/.zshrc` ou `~/.bashrc` :

```bash
# Charger pip-mode
source /path/to/claude-project/scripts/pip-mode.sh

# Créer un alias pour faciliter l'utilisation
alias pip-mode='pip_mode'
```

Puis rechargez votre configuration :
```bash
source ~/.zshrc  # ou source ~/.bashrc
```

## Utilisation

### Commandes disponibles

#### 1. Vérifier la configuration actuelle

```bash
./scripts/pip-mode.sh status
```

Ou via Claude Code :
```bash
/pip-mode status
```

**Sortie exemple** :
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Configuration pip actuelle
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mode: PyPI standard
PIP_INDEX_URL: Non défini (utilise PyPI par défaut)
PIP_TRUSTED_HOST: Non défini
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 2. Basculer vers Nexus

```bash
./scripts/pip-mode.sh nexus
```

Ou via Claude Code :
```bash
/pip-mode nexus
```

**Sortie** :
```
✓ Mode Nexus activé
  Index URL: https://nexus-ext.cnt.zone.local/repository/cnt-pypi-public/simple
  Trusted Host: nexus-ext.cnt.zone.local
```

#### 3. Revenir au mode PyPI standard

```bash
./scripts/pip-mode.sh standard
```

Ou via Claude Code :
```bash
/pip-mode standard
```

**Sortie** :
```
✓ Mode PyPI standard activé
  Les variables PIP_INDEX_URL et PIP_TRUSTED_HOST ont été supprimées
```

## Workflows recommandés

### Workflow 1 : Développement avec PyPI standard

```bash
# 1. S'assurer d'être en mode standard
./scripts/pip-mode.sh standard

# 2. Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Vérifier l'installation
pip list
```

### Workflow 2 : Développement avec Nexus

```bash
# 1. Basculer vers Nexus
./scripts/pip-mode.sh nexus

# 2. Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances depuis Nexus
pip install package-from-nexus

# 4. Vérifier la configuration
./scripts/pip-mode.sh status
```

### Workflow 3 : Environnement hybride

```bash
# 1. Commencer en mode standard
./scripts/pip-mode.sh standard
python3 -m venv venv
source venv/bin/activate

# 2. Installer les packages publics
pip install pandas numpy matplotlib

# 3. Basculer vers Nexus pour packages internes
./scripts/pip-mode.sh nexus
pip install internal-package

# 4. Revenir en mode standard si besoin
./scripts/pip-mode.sh standard
```

## Intégration avec Claude Code

### Utilisation dans les agents

Lorsque vous créez un agent qui nécessite des packages Python, vous pouvez utiliser la commande `/pip-mode` directement dans vos prompts :

```markdown
# Agent example

Avant d'installer les dépendances Python :
1. Exécute /pip-mode standard
2. Crée l'environnement virtuel
3. Installe les packages requis
```

### Utilisation dans les hooks

Vous pouvez automatiser le basculement dans les hooks Claude Code :

```json
{
  "hooks": {
    "pre-python-install": {
      "command": "./scripts/pip-mode.sh standard",
      "description": "Bascule en mode PyPI standard avant l'installation"
    },
    "pre-nexus-install": {
      "command": "./scripts/pip-mode.sh nexus",
      "description": "Bascule en mode Nexus pour packages internes"
    }
  }
}
```

## Variables d'environnement

Le script gère automatiquement ces variables :

| Variable | Mode Standard | Mode Nexus |
|----------|---------------|------------|
| `PIP_INDEX_URL` | Non défini | `https://nexus-ext.cnt.zone.local/repository/cnt-pypi-public/simple` |
| `PIP_TRUSTED_HOST` | Non défini | `nexus-ext.cnt.zone.local` |
| `NEXUS_INDEX` | Défini (constante) | Défini (constante) |
| `NEXUS_HOST` | Défini (constante) | Défini (constante) |

## Fonctionnement technique

### Mode Nexus

Quand vous activez le mode Nexus :
1. `PIP_INDEX_URL` est défini sur l'URL Nexus
2. `PIP_TRUSTED_HOST` est défini sur le domaine Nexus
3. pip utilisera automatiquement ces paramètres pour toutes les installations

### Mode Standard

Quand vous activez le mode standard :
1. `PIP_INDEX_URL` est supprimé (unset)
2. `PIP_TRUSTED_HOST` est supprimé (unset)
3. pip revient aux paramètres par défaut (PyPI)

### Persistance

Les changements de configuration sont **persistants uniquement pour la session shell en cours**.

Pour une configuration permanente, utilisez un des fichiers de configuration pip :

**Option 1 : Configuration globale** (`~/.pip/pip.conf`)
```ini
[global]
index-url = https://nexus-ext.cnt.zone.local/repository/cnt-pypi-public/simple
trusted-host = nexus-ext.cnt.zone.local
```

**Option 2 : Configuration par projet** (`pip.conf` dans le projet)
```ini
[global]
index-url = https://nexus-ext.cnt.zone.local/repository/cnt-pypi-public/simple
trusted-host = nexus-ext.cnt.zone.local
```

## Dépannage

### Problème : Les changements ne sont pas appliqués

**Solution** : Sourcez le script au lieu de l'exécuter
```bash
# ❌ Mauvais
./scripts/pip-mode.sh nexus

# ✓ Bon
source scripts/pip-mode.sh
pip_mode nexus
```

### Problème : pip ignore les variables d'environnement

**Solution** : Vérifiez que les variables sont exportées
```bash
./scripts/pip-mode.sh status
echo $PIP_INDEX_URL
echo $PIP_TRUSTED_HOST
```

### Problème : Erreurs SSL avec Nexus

**Solution** : Vérifiez que `PIP_TRUSTED_HOST` est défini
```bash
./scripts/pip-mode.sh nexus
pip install --verbose package-name
```

### Problème : Commande non trouvée après installation

**Solution** : Rechargez votre configuration shell
```bash
source ~/.zshrc  # ou source ~/.bashrc
```

## Bonnes pratiques

1. **Toujours vérifier le mode actif** avant d'installer des packages
   ```bash
   ./scripts/pip-mode.sh status
   ```

2. **Documenter le mode requis** dans vos README et scripts
   ```bash
   # Ce projet nécessite le mode Nexus
   ./scripts/pip-mode.sh nexus
   ```

3. **Utiliser des environnements virtuels** pour isoler les dépendances
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Tester en mode standard** avant de passer en production
   ```bash
   ./scripts/pip-mode.sh standard
   pip install -r requirements.txt
   pytest
   ```

## Références

- [pip Configuration](https://pip.pypa.io/en/stable/topics/configuration/)
- [Nexus Repository Manager](https://help.sonatype.com/repomanager3)
- [Python Virtual Environments](https://docs.python.org/3/library/venv.html)

## Support

Pour toute question ou problème :
1. Vérifiez d'abord le statut : `./scripts/pip-mode.sh status`
2. Consultez ce guide
3. Contactez l'équipe infrastructure si le problème persiste

---

**Version** : 1.0.0
**Dernière mise à jour** : 2026-01-07
**Auteur** : PEA Tracker Team
