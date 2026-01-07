# Changelog - PEA Tracker

## [1.1.0] - 2026-01-07

### Ajouté
- **Utilitaire pip-mode** : Nouvelle fonctionnalité pour basculer entre PyPI standard et Nexus
  - Script shell `scripts/pip-mode.sh` avec 3 modes (nexus, standard, status)
  - Commande Claude Code `/pip-mode` pour utilisation interactive
  - Documentation complète dans `docs/pip-mode-guide.md`
  - Section dédiée dans le README.md

### Fichiers créés
- `.claude/commands/pip-mode.md` - Définition de la commande Claude
- `scripts/pip-mode.sh` - Script shell principal (exécutable)
- `docs/pip-mode-guide.md` - Guide d'utilisation détaillé

### Fichiers modifiés
- `README.md` - Ajout section "Configuration pip (Nexus/PyPI)"

### Détails techniques
- Gestion des variables d'environnement `PIP_INDEX_URL` et `PIP_TRUSTED_HOST`
- Support des URLs Nexus personnalisées
- Validation et gestion d'erreurs
- Messages formatés avec emojis pour meilleure UX
- Compatibles bash et zsh

### Workflows recommandés
1. Mode standard pour développement initial
2. Création d'environnement virtuel Python
3. Installation des dépendances selon le mode choisi
4. Basculement flexible entre les modes selon les besoins

## [1.0.0] - 2026-01-07

### Initial Release
- Architecture MCP-native avec Claude Code
- Agent Market Watcher opérationnel
- Documentation complète du projet
- Configuration serveurs MCP (Google Drive, Gmail, Yahoo Finance)
- Structure de dossiers Google Drive établie

---

**Format** : [Semantic Versioning 2.0.0](https://semver.org/)
**Convention** : [Keep a Changelog](https://keepachangelog.com/)
