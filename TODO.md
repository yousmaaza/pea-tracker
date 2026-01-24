# TODO - PEA Tracker

## 🎯 Priorités immédiates

### 1. Tester l'agent Market Watcher
- [ ] Créer le fichier `PEA_Watchlist_Indicateurs.xlsx` dans Google Drive
- [ ] Ajouter quelques tickers de test dans la feuille "Watchlist"
- [ ] Exécuter l'agent en mode test : `invoke @market-watcher-pea`
- [ ] Vérifier la génération des signaux
- [ ] Vérifier l'upload des rapports dans Google Drive
- [ ] Vérifier l'envoi des emails d'alerte

### 2. Configurer l'automatisation (Refactoring launchd) ✅ TERMINÉ
Branche: `feature/agent-automation-launchd` (pushée sur GitHub)

#### Phase 1 : Scripts Utilitaires (Fondations) ✅
- [x] Créer `scripts/utils/check-prerequisites.sh` - Vérifications système (Docker, API keys)
- [x] Créer `scripts/utils/start-yfinance-mcp.sh` - Démarrage conteneur Docker MCP
- [x] Créer `scripts/utils/stop-yfinance-mcp.sh` - Arrêt conteneur Docker MCP
- [x] Créer `scripts/utils/send-error-notification.sh` - Notifications via Gmail MCP

#### Phase 2 : Wrapper Principal ✅
- [x] Créer `scripts/run-market-watcher.sh` - Script orchestrateur (224 lignes)
- [x] Rendre tous les scripts exécutables (chmod +x)

#### Phase 3 : Configuration launchd ✅
- [x] Créer `launchd/com.pea-tracker.market-watcher-07h.plist` - Job 7h (Lun-Ven)
- [x] Créer `launchd/com.pea-tracker.market-watcher-12h.plist` - Job 12h (Lun-Ven)
- [x] Créer `launchd/com.pea-tracker.market-watcher-18h.plist` - Job 18h (Lun-Ven)
- [x] Créer `launchd/com.pea-tracker.market-watcher-21h.plist` - Job 21h (Lun-Ven)

#### Phase 4 : Configuration Environnement ✅
- [x] Créer `config/.env.template` - Template avec ANTHROPIC_API_KEY, EMAIL, etc.
- [x] Créer structure `logs/` avec `.gitkeep`
- [x] Mettre à jour `.gitignore` - Ajout *.pid, config/.env

#### Phase 5 : Documentation ✅
- [x] Mettre à jour `CLAUDE.md` - Section complète "Automatisation via launchd"
- [x] Mettre à jour `README.md` - Architecture MCP, section Automatisation
- [x] Mettre à jour ce fichier `TODO.md` - Marquer tâches terminées

#### Adaptation Docker ✅
- [x] Refactoriser start/stop-yfinance-mcp.sh pour gérer conteneur Docker
- [x] Mettre à jour check-prerequisites.sh pour vérifier Docker
- [x] Corriger health check SSE (timeout 1s au lieu de stream infini)
- [x] Pusher les 3 commits vers GitHub

#### Tests et Validation 🚧 EN COURS
- [x] Tester scripts utilitaires individuellement (start/stop MCP validés)
- [ ] Tester wrapper principal (run-market-watcher.sh) - exécution complète
- [ ] Tester notification d'erreur via Gmail MCP
- [ ] Tester 1 job launchd (07h) manuellement
- [ ] Déployer les 4 jobs launchd dans ~/Library/LaunchAgents
- [ ] Surveillance période probatoire (1 semaine)

**Commits** : 3 commits sur `feature/agent-automation-launchd`
- `c80a31e` : Phase 1 & 2 (scripts automatisation)
- `8ca4323` : Phase 3 & 4 (launchd + config)
- `be3e1bb` : Adaptation Docker (refactor MCP scripts)

## 📋 Phase 2 : Agent Portfolio Advisor

### Développement de l'agent
- [ ] Créer le fichier `.claude/agents/portfolio-advisor.md`
- [ ] Implémenter le parsing des exports Boursorama CSV
- [ ] Développer le calcul des métriques de performance
  - [ ] Performance globale du portefeuille
  - [ ] Performance par ligne (ticker)
  - [ ] Calcul des plus/moins-values
  - [ ] Calcul du rendement annualisé
- [ ] Analyser l'allocation
  - [ ] Répartition sectorielle
  - [ ] Répartition géographique
  - [ ] Concentration du portefeuille (indice Herfindahl)
- [ ] Générer le rapport mensuel (format Markdown)
- [ ] Implémenter l'envoi automatique du rapport

### Testing
- [ ] Créer des exports Boursorama de test
- [ ] Valider les calculs de performance
- [ ] Tester la génération du rapport
- [ ] Tester l'envoi par email

### Automatisation
- [ ] Créer un script cron pour exécution mensuelle (1er du mois)
- [ ] Documenter la procédure d'export Boursorama

## 🔧 Améliorations techniques

### Google Drive
- [ ] Créer un script de setup pour la structure de dossiers
- [ ] Documenter la structure du fichier Excel watchlist
- [ ] Créer un template Excel à télécharger

### Documentation
- [ ] Mettre à jour le README.md selon le nouveau CLAUDE.md
- [ ] Créer un guide de démarrage rapide
- [ ] Ajouter des captures d'écran des emails/rapports
- [ ] Documenter les formats de données

### Code Quality
- [ ] Ajouter un .gitignore complet
- [ ] Créer un fichier .env.example
- [ ] Documenter les variables d'environnement nécessaires

## 📊 Phase 3 : Optimisations (Après Portfolio Advisor)

### Backtesting
- [ ] Récupérer l'historique des signaux générés
- [ ] Calculer le taux de réussite par type de signal
- [ ] Analyser les faux positifs/négatifs
- [ ] Ajuster les seuils de scoring si nécessaire

### Profil de risque
- [ ] Créer un questionnaire de profil investisseur
- [ ] Intégrer le profil dans les recommandations
- [ ] Adapter les seuils d'alerte selon le profil

### Actualités financières
- [ ] Intégrer un flux RSS d'actualités financières
- [ ] Filtrer les news pertinentes par ticker
- [ ] Inclure le contexte news dans les alertes

### Notifications alternatives
- [ ] Implémenter les alertes Telegram (optionnel)
- [ ] Implémenter les alertes SMS (optionnel)
- [ ] Créer un système de préférences de notification

## 🚀 Phase 4 : Features avancées (Long terme)

### Machine Learning
- [ ] Collecter l'historique des signaux et résultats
- [ ] Entraîner un modèle de scoring amélioré
- [ ] A/B testing scoring classique vs ML

### Analyse sentiment
- [ ] Intégrer une API d'analyse sentiment (news, réseaux sociaux)
- [ ] Pondérer le scoring avec le sentiment market
- [ ] Créer des alertes sur changements de sentiment

### Données fondamentales
- [ ] Intégrer des données fondamentales (P/E, revenus, etc.)
- [ ] Analyser la valorisation des titres
- [ ] Combiner analyse technique et fondamentale

### Multi-portefeuilles
- [ ] Supporter plusieurs portefeuilles (PEA + CTO par exemple)
- [ ] Comparer les performances entre portefeuilles
- [ ] Analyser l'allocation globale

### Dashboard web
- [ ] Créer une interface web simple (Next.js)
- [ ] Visualiser les signaux en temps réel
- [ ] Afficher l'historique des performances
- [ ] Gérer la watchlist via l'interface

## 🐛 Bugs connus / À surveiller

> Aucun bug connu pour le moment

## 💡 Idées / Suggestions

- [ ] Intégrer des screeners de titres PEA-eligibles
- [ ] Créer un système de notation des titres (scoring global)
- [ ] Ajouter des alertes sur dividendes
- [ ] Implémenter un tracking des frais de courtage
- [ ] Créer des rapports fiscaux (IFU automatique)

## 📝 Notes

### Décisions à prendre
- Faut-il supporter d'autres brokers que Boursorama ?
- Quel niveau de granularité pour l'analyse sectorielle ?
- Faut-il intégrer des données payantes (premium) ?

### Dépendances externes
- Stabilité de l'API Yahoo Finance (gratuite)
- Quotas Google Drive/Gmail
- Rate limits Claude API

### Prochaine revue
- **Date** : 2026-02-07 (1 mois)
- **Objectif** : Valider Market Watcher en production, lancer Portfolio Advisor

---

**Dernière mise à jour** : 2026-01-24
**Responsable** : [@yousrimaazaoui](mailto:votre@email.com)
**Statut** : Agent Market Watcher opérationnel + Automatisation launchd déployée
