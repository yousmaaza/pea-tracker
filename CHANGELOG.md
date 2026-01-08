# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

### Prévu
- Implémentation de l'agent Portfolio Advisor
- Parsing des exports Boursorama CSV
- Calcul des métriques de performance
- Génération des rapports mensuels

## [2.0.0] - 2026-01-08

### 🎉 Migration majeure vers architecture MCP-native

Cette version marque une refonte complète de l'architecture du projet, passant d'une approche n8n à une architecture MCP-native avec Claude Code.

### ✨ Ajouté
- **Architecture MCP-native** : Utilisation directe des serveurs MCP standards
- **Agent Market Watcher PEA** : Agent IA autonome pleinement fonctionnel
  - Surveillance quotidienne automatisée des marchés
  - Calcul d'indicateurs techniques (RSI, MACD, MA20/50/200)
  - Génération de signaux BUY/SELL/WATCH avec scoring de confiance
  - Sauvegarde des rapports sur Google Drive
  - Envoi automatique d'alertes email (score ≥ 60)
- **Serveurs MCP configurés** :
  - `@modelcontextprotocol/server-google-drive`
  - `@modelcontextprotocol/server-gmail`
  - `mcp-server-yfinance`
  - `@modelcontextprotocol/server-github`
  - `@modelcontextprotocol/server-filesystem`
- **Documentation complète** :
  - `CLAUDE.md` : Documentation détaillée du projet
  - `docs/architecture/mcp-integration.md` : Architecture MCP
  - `docs/mcp/yahoo-finance-integration.md` : Guide Yahoo Finance
  - `docs/agents/market-watcher-spec.md` : Spécifications Market Watcher
  - `docs/agents/portfolio-advisor-spec.md` : Spécifications Portfolio Advisor
  - `docs/ARCHITECTURE_DECISION.md` : Décisions d'architecture
  - `docs/SETUP_GUIDE.md` : Guide d'installation
- **Workflow Git documenté** : Instructions complètes pour commits/push réguliers
- **Structure Google Drive** : Dossiers organisés pour imports, rapports et données
- **README.md modernisé** : Refonte complète avec badges et documentation à jour
- **CHANGELOG.md** : Suivi des versions et évolutions du projet

### 🔧 Modifié
- **Coûts réduits** : De 25-60€/mois à 5-20€/mois (uniquement API Claude)
- **Simplification** : Suppression de l'infrastructure n8n
- **Fiabilité** : Moins de points de défaillance
- **Maintenance** : Plus besoin de serveur à maintenir

### ❌ Supprimé
- **n8n** : Suppression de l'orchestrateur (remplacé par MCP)
- **Infrastructure serveur** : Plus nécessaire avec l'architecture MCP
- **Base de données** : Stockage direct sur Google Drive
- **Scripts intermédiaires** : Accès direct aux données via MCP

### 🐛 Corrigé
- Documentation obsolète mise à jour
- Architecture simplifiée et plus fiable
- Réduction de la complexité technique

### 🔒 Sécurité
- Authentification OAuth pour Google services
- Clés API stockées dans variables d'environnement
- Communications chiffrées (HTTPS)
- Pas de stockage d'identifiants broker

## [1.0.0] - 2026-01-07

### ✨ Version initiale (architecture n8n)

Version initiale du projet avec architecture basée sur n8n (obsolète).

### Ajouté
- Structure de base du projet
- Spécifications des agents IA
  - Market Watcher (spécifications uniquement)
  - Portfolio Advisor (spécifications uniquement)
- Documentation initiale
- Configuration de base
- Templates Excel et rapports

### Caractéristiques
- **Architecture** : n8n + Claude API
- **Coûts** : 25-60€/mois
- **Statut** : Spécifications uniquement, pas d'implémentation

### Notes
Cette version a été rapidement remplacée par la version 2.0.0 avec architecture MCP-native plus moderne et économique.

---

## Types de changements

Ce changelog utilise les catégories suivantes :

- **✨ Ajouté** : Nouvelles fonctionnalités
- **🔧 Modifié** : Modifications de fonctionnalités existantes
- **❌ Supprimé** : Fonctionnalités supprimées
- **🐛 Corrigé** : Corrections de bugs
- **🔒 Sécurité** : Améliorations de sécurité
- **📚 Documentation** : Modifications de documentation uniquement
- **⚡ Performance** : Améliorations de performance
- **🎨 Style** : Modifications de style/formatage

## Liens

- [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)
- [Semantic Versioning](https://semver.org/lang/fr/)
- [Repository GitHub](https://github.com/yousmaaza/pea-tracker)

---

**Note** : Les versions antérieures à 2.0.0 utilisaient l'architecture n8n et sont maintenant obsolètes.
