# Project Roadmap - PEA Tracker

Ce document contient la roadmap complète du projet PEA Tracker et doit être mis à jour à chaque nouvelle Pull Request de feature.

**Dernière mise à jour** : 2026-01-08
**Version actuelle** : 2.0.0

---

## 📊 Vue d'ensemble de l'avancement

| Phase | Statut | Progression | Date cible |
|-------|--------|-------------|------------|
| Phase 1 : Infrastructure MCP | ✅ Terminée | 100% | 2026-01-08 |
| Phase 2 : Portfolio Advisor | 🔄 En cours | 0% | Q1 2026 |
| Phase 3 : Optimisations | 📋 Planifiée | 0% | Q2 2026 |
| Phase 4 : Améliorations avancées | 🔮 Futur | 0% | Q3-Q4 2026 |

---

## Phase 1 : Infrastructure MCP ✅ TERMINÉE

**Objectif** : Mise en place de l'infrastructure MCP-native et implémentation du Market Watcher

**Statut global** : ✅ 100% (5/5 tâches complétées)

### Tâches complétées

- [x] **Configuration Claude Code**
  - Installation et configuration de Claude Code CLI
  - Configuration de l'API Anthropic
  - Date : 2026-01-07

- [x] **Installation serveurs MCP**
  - `@modelcontextprotocol/server-google-drive`
  - `@modelcontextprotocol/server-gmail`
  - `mcp-server-yfinance`
  - `@modelcontextprotocol/server-github`
  - `@modelcontextprotocol/server-filesystem`
  - Date : 2026-01-07

- [x] **Authentification Google Drive/Gmail**
  - Configuration OAuth pour Google Drive
  - Configuration OAuth pour Gmail
  - Génération des tokens d'accès
  - Date : 2026-01-07

- [x] **Structure Google Drive créée**
  - Dossier `PEA-Tracker/Imports/`
  - Dossier `PEA-Tracker/Reports/monthly/`
  - Dossier `PEA-Tracker/Reports/signals/`
  - Fichier `PEA_Watchlist_Indicateurs.xlsx`
  - Date : 2026-01-07

- [x] **Agent Market Watcher implémenté et opérationnel**
  - Fichier agent : `.claude/agents/market-watcher-pea.md`
  - Récupération watchlist depuis Google Drive
  - Collecte données Yahoo Finance
  - Calcul indicateurs techniques (RSI, MACD, MA)
  - Génération signaux BUY/SELL/WATCH
  - Système de scoring de confiance (0-100)
  - Sauvegarde rapports sur Google Drive
  - Envoi alertes email (score ≥ 60)
  - Date : 2026-01-08

### Livrables de la Phase 1

- ✅ Infrastructure MCP fonctionnelle
- ✅ Agent Market Watcher opérationnel
- ✅ Documentation complète (CLAUDE.md, README.md, CHANGELOG.md)
- ✅ Architecture MCP documentée
- ✅ Guide d'installation (docs/SETUP_GUIDE.md)
- ✅ Spécifications agents (docs/agents/)

---

## Phase 2 : Portfolio Advisor 🔄 EN COURS

**Objectif** : Implémenter l'agent Portfolio Advisor pour l'analyse mensuelle du portefeuille

**Statut global** : 🔄 0% (0/5 tâches complétées)

**Date de début prévue** : Q1 2026

### Tâches à réaliser

- [ ] **Implémenter l'agent Portfolio Advisor**
  - Créer le fichier `.claude/agents/portfolio-advisor.md`
  - Définir le workflow complet de l'agent
  - Intégrer avec les serveurs MCP existants
  - **Assigné à** : Non assigné
  - **Priorité** : Haute
  - **Estimation** : Pas d'estimation de temps

- [ ] **Parser les exports Boursorama (CSV)**
  - Analyser le format des exports Boursorama
  - Créer la logique de parsing CSV
  - Extraire les positions, prix, quantités
  - Gérer les différents formats CSV possibles
  - **Assigné à** : Non assigné
  - **Priorité** : Haute
  - **Estimation** : Pas d'estimation de temps
  - **Dépend de** : Implémentation agent

- [ ] **Calculer les métriques de performance**
  - Performance globale du portefeuille
  - Performance par ligne/position
  - Plus-values latentes et réalisées
  - Rendement annualisé
  - Volatilité du portefeuille
  - Ratio de Sharpe
  - **Assigné à** : Non assigné
  - **Priorité** : Haute
  - **Estimation** : Pas d'estimation de temps
  - **Dépend de** : Parser exports Boursorama

- [ ] **Générer les rapports mensuels**
  - Template de rapport Markdown
  - Synthèse des performances
  - Analyse d'allocation (secteurs, géographies)
  - Analyse de diversification
  - Recommandations de rééquilibrage
  - Graphiques et tableaux
  - **Assigné à** : Non assigné
  - **Priorité** : Moyenne
  - **Estimation** : Pas d'estimation de temps
  - **Dépend de** : Calculer métriques

- [ ] **Automatiser l'envoi des rapports**
  - Configuration envoi email via Gmail MCP
  - Format HTML des emails
  - Pièces jointes (rapports PDF)
  - Planification mensuelle (1er du mois)
  - **Assigné à** : Non assigné
  - **Priorité** : Moyenne
  - **Estimation** : Pas d'estimation de temps
  - **Dépend de** : Générer rapports

### Livrables attendus Phase 2

- Agent Portfolio Advisor opérationnel
- Parser Boursorama fonctionnel
- Système de calcul de métriques
- Templates de rapports
- Automatisation mensuelle
- Documentation mise à jour

---

## Phase 3 : Optimisations 📋 PLANIFIÉE

**Objectif** : Optimiser et améliorer les agents existants

**Statut global** : 📋 0% (0/5 tâches planifiées)

**Date de début prévue** : Q2 2026

### Tâches planifiées

- [ ] **Backtesting des signaux Market Watcher**
  - Collecter historique des signaux générés
  - Comparer avec évolution réelle des cours
  - Calculer taux de réussite par type de signal
  - Ajuster les seuils et le scoring
  - Créer dashboard de performance
  - **Priorité** : Haute
  - **Valeur métier** : Améliorer fiabilité des signaux

- [ ] **Profil de risque personnalisé**
  - Questionnaire profil investisseur
  - Calcul score de risque (1-10)
  - Adaptation des recommandations
  - Alertes personnalisées selon profil
  - **Priorité** : Moyenne
  - **Valeur métier** : Personnalisation des conseils

- [ ] **Intégration actualités financières (RSS/API)**
  - Intégrer flux RSS financiers (Boursorama, Les Échos, etc.)
  - Parser les actualités liées aux titres en watchlist
  - Analyse sentiment avec IA
  - Intégrer dans les rapports Market Watcher
  - **Priorité** : Moyenne
  - **Valeur métier** : Contexte supplémentaire pour décisions

- [ ] **Dashboard web simple (optionnel)**
  - Interface web simple pour visualiser les données
  - Graphiques de performance
  - Historique des signaux
  - Configuration watchlist
  - Technologies : React + Tailwind CSS
  - **Priorité** : Basse
  - **Valeur métier** : Meilleure visualisation

- [ ] **Alertes Telegram/SMS (optionnel)**
  - Intégration Telegram Bot API
  - Intégration service SMS (Twilio)
  - Configuration préférences notifications
  - Alertes temps réel
  - **Priorité** : Basse
  - **Valeur métier** : Notifications instantanées

### Livrables attendus Phase 3

- Système de backtesting opérationnel
- Profil de risque intégré
- Actualités financières dans les rapports
- Dashboard web (optionnel)
- Notifications multi-canaux (optionnel)

---

## Phase 4 : Améliorations avancées 🔮 FUTUR

**Objectif** : Fonctionnalités avancées et intelligence artificielle poussée

**Statut global** : 🔮 0% (0/4 tâches futures)

**Date de début prévue** : Q3-Q4 2026

### Idées futures

- [ ] **Machine Learning pour scoring amélioré**
  - Entraîner modèle ML sur historique signaux
  - Prédiction probabilité de réussite
  - Features : indicateurs techniques + sentiment + actualités
  - Amélioration continue du modèle
  - **Complexité** : Élevée
  - **ROI potentiel** : Très élevé

- [ ] **Analyse sentiment market (NLP)**
  - Scraping forums financiers
  - Analyse sentiment Twitter/X
  - Analyse rapports annuels avec NLP
  - Score de sentiment par titre
  - **Complexité** : Élevée
  - **ROI potentiel** : Élevé

- [ ] **Intégration données fondamentales**
  - API données fondamentales (P/E, P/B, dividendes)
  - Analyse valorisation
  - Screening fondamental
  - Combinaison analyse technique + fondamentale
  - **Complexité** : Moyenne
  - **ROI potentiel** : Élevé

- [ ] **Support multi-portefeuilles**
  - Gestion de plusieurs PEA
  - Gestion PEA + CTO
  - Vue consolidée
  - Recommandations cross-portefeuilles
  - **Complexité** : Moyenne
  - **ROI potentiel** : Moyen

### Livrables attendus Phase 4

- Modèle ML de scoring
- Système d'analyse sentiment
- Intégration données fondamentales
- Support multi-portefeuilles

---

## 🎯 Priorités actuelles

### Court terme (Sprint actuel)

1. **Documenter le projet** ✅ FAIT
   - README.md modernisé
   - CHANGELOG.md créé
   - Workflow Git documenté
   - Project_Roadmap.md créé

2. **Tester Market Watcher en conditions réelles**
   - Exécuter quotidiennement pendant 1 semaine
   - Analyser la qualité des signaux
   - Ajuster les seuils si nécessaire

3. **Préparer Phase 2**
   - Collecter exemples d'exports Boursorama
   - Définir format exact du parsing
   - Lister les métriques à calculer

### Moyen terme (Prochains sprints)

1. Implémenter Portfolio Advisor (Phase 2)
2. Créer système de backtesting (Phase 3)
3. Intégrer profil de risque (Phase 3)

---

## 📝 Process de mise à jour

### Quand mettre à jour cette roadmap

- ✅ À chaque PR de nouvelle feature mergée
- ✅ À la fin de chaque sprint
- ✅ Quand une tâche change de statut
- ✅ Quand les priorités changent
- ✅ Quand de nouvelles idées émergent

### Comment mettre à jour

1. **Nouvelle feature complétée** :
   ```markdown
   - [x] **Nom de la feature**
     - Description
     - Date : YYYY-MM-DD
     - PR : #numero
   ```

2. **Nouvelle tâche ajoutée** :
   ```markdown
   - [ ] **Nom de la tâche**
     - Description détaillée
     - **Assigné à** : Nom ou "Non assigné"
     - **Priorité** : Haute/Moyenne/Basse
     - **Estimation** : Pas d'estimation
     - **Dépend de** : Autres tâches si applicable
   ```

3. **Changement de priorité** :
   - Mettre à jour le champ **Priorité**
   - Réorganiser les tâches si nécessaire
   - Expliquer le changement dans le commit

4. **Tâche en cours** :
   - Changer le statut de 📋 Planifiée à 🔄 En cours
   - Ajouter date de début
   - Assigner à un développeur

### Template de commit pour mise à jour roadmap

```bash
git commit -m "docs: mise à jour roadmap - [description du changement]

- Tâche X marquée comme complétée (PR #123)
- Nouvelle tâche Y ajoutée en Phase 3
- Priorité de Z changée de Moyenne à Haute
"
```

---

## 📊 Métriques et KPIs

### Métriques de développement

- **Tâches complétées** : 5/14 (35.7%)
- **Phases terminées** : 1/4 (25%)
- **Vélocité** : Phase 1 complétée en 2 jours

### Objectifs 2026

- ✅ Q1 : Phase 1 terminée (Market Watcher opérationnel)
- 🎯 Q1 : Phase 2 terminée (Portfolio Advisor opérationnel)
- 🎯 Q2 : Phase 3 avancée (Backtesting + Profil de risque)
- 🎯 Q3-Q4 : Phase 4 démarrée (ML + NLP)

---

## 🤝 Contribution

Pour contribuer à la roadmap :

1. Ouvrir une issue pour proposer une nouvelle feature
2. Discuter avec l'équipe de la priorité
3. Ajouter la tâche dans la phase appropriée
4. Créer une PR avec la mise à jour de la roadmap

---

## 📚 Références

- [CLAUDE.md](../CLAUDE.md) - Documentation complète du projet
- [README.md](../README.md) - Guide d'utilisation
- [CHANGELOG.md](../CHANGELOG.md) - Historique des versions
- [docs/agents/](./agents/) - Spécifications des agents

---

**Maintenu par** : Équipe PEA Tracker
**Dernière révision** : 2026-01-08
**Prochaine révision prévue** : Fin Phase 2
