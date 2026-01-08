# PEA Tracker - Suivi Intelligent de Portefeuille

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/yousmaaza/pea-tracker)
[![Architecture](https://img.shields.io/badge/architecture-MCP--native-green.svg)](https://modelcontextprotocol.io/)
[![Agent](https://img.shields.io/badge/Market%20Watcher-✅%20Opérationnel-brightgreen.svg)](.claude/agents/market-watcher-pea.md)

Plateforme intelligente de gestion de portefeuille PEA utilisant des agents IA autonomes Claude pour optimiser les décisions d'investissement sur les marchés européens.

## 🚀 Démarrage rapide

```bash
# 1. Cloner le projet
git clone https://github.com/yousmaaza/pea-tracker.git
cd pea-tracker

# 2. Installer Claude Code
npm install -g @anthropic-ai/claude-code

# 3. Configurer l'API Claude
export ANTHROPIC_API_KEY="your-api-key"

# 4. Lancer le Market Watcher
claude-code agent run market-watcher-pea
```

📖 **Documentation complète** : [CLAUDE.md](./CLAUDE.md)

## ✨ Fonctionnalités

### 🔍 Market Watcher PEA (✅ Opérationnel)

Agent IA autonome pour la surveillance quotidienne des marchés :

- ✅ Surveillance automatique de votre watchlist
- ✅ Calcul d'indicateurs techniques (RSI, MACD, MA)
- ✅ Génération de signaux BUY/SELL/WATCH avec scoring de confiance
- ✅ Rapports détaillés sauvegardés sur Google Drive
- ✅ Alertes email automatiques (score ≥ 60)

**Fréquence** : Quotidienne à 8h (automatisable via cron)

### 📊 Portfolio Advisor (🔜 À venir)

Agent IA pour l'analyse mensuelle du portefeuille :

- Calcul de performance globale et par ligne
- Analyse d'allocation sectorielle et géographique
- Recommandations de rééquilibrage
- Rapports mensuels détaillés

**Fréquence** : Mensuelle (1er du mois)

## 🏗️ Architecture

### Philosophie MCP-native

Architecture moderne sans infrastructure intermédiaire :

```
Boursorama → Export Excel → Google Drive ←→ Claude Agent (MCP) → Gmail
```

**Avantages** :
- ✅ Pas de serveur à maintenir
- ✅ Coûts réduits (5-20€/mois uniquement API Claude)
- ✅ Configuration minimale
- ✅ Fiabilité accrue

### Stack technique

**Environnement d'exécution**
- **Claude Code** : CLI pour exécuter les agents IA
- **Agents personnalisés** : Définis dans `.claude/agents/`
- **Exécution** : Manuelle via CLI ou automatisée via cron

**Serveurs MCP configurés**
- `@modelcontextprotocol/server-google-drive` : Accès Google Drive/Sheets
- `@modelcontextprotocol/server-gmail` : Envoi d'emails
- `mcp-server-yfinance` : Données boursières Yahoo Finance
- `@modelcontextprotocol/server-github` : Gestion du code source
- `@modelcontextprotocol/server-filesystem` : Accès système de fichiers

**Données et stockage**
- **Google Drive** : Stockage des exports, historiques et rapports
- **Yahoo Finance** : Données boursières en temps réel (gratuit)
- **Gmail** : Notifications et alertes

## 📁 Structure du projet

```
pea-tracker/
├── .claude/
│   ├── agents/
│   │   └── market-watcher-pea.md         # ✅ Agent Market Watcher
│   └── settings.local.json                # Configuration MCP (non versionné)
│
├── docs/
│   ├── agents/
│   │   ├── market-watcher-spec.md         # Spécifications Market Watcher
│   │   └── portfolio-advisor-spec.md      # Spécifications Portfolio Advisor
│   ├── architecture/
│   │   └── mcp-integration.md             # Documentation architecture MCP
│   ├── mcp/
│   │   └── yahoo-finance-integration.md   # Guide Yahoo Finance MCP
│   ├── ARCHITECTURE_DECISION.md           # Décisions architecture
│   └── SETUP_GUIDE.md                     # Guide d'installation détaillé
│
├── prompts/
│   ├── market-analysis.md                 # Prompt template Market Watcher
│   └── portfolio-review.md                # Prompt template Portfolio Advisor
│
├── CLAUDE.md                              # Documentation complète du projet
├── README.md                              # Ce fichier
├── CHANGELOG.md                           # Historique des versions
└── TODO.md                                # Liste des tâches à venir
```

## 🛠️ Installation

### Prérequis

| Élément | Description | Coût |
|---------|-------------|------|
| Claude Code | CLI tool Anthropic | Gratuit |
| Clé API Claude | API Anthropic | 5-20€/mois |
| Google Workspace | Drive + Gmail | Gratuit |
| MCP Servers | Serveurs MCP standards | Gratuit |
| Yahoo Finance | Via MCP | Gratuit |

**Total estimé** : **5-20€/mois** (uniquement l'API Claude)

### Installation pas à pas

#### 1. Installer Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

#### 2. Configurer l'API Claude

```bash
export ANTHROPIC_API_KEY="your-api-key"
```

#### 3. Cloner le projet

```bash
git clone https://github.com/yousmaaza/pea-tracker.git
cd pea-tracker
```

#### 4. Configurer les serveurs MCP

Éditer `.claude/settings.local.json` et ajouter les serveurs nécessaires.

Voir [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) pour les instructions détaillées.

#### 5. Configurer Google Drive

1. Créer la structure de dossiers :
   ```
   PEA-Tracker/
   ├── Imports/                           # Exports Boursorama
   ├── Reports/
   │   ├── monthly/                       # Rapports mensuels
   │   └── signals/                       # Alertes Market Watcher
   └── PEA_Watchlist_Indicateurs.xlsx    # Watchlist principale
   ```

2. Configurer l'authentification OAuth pour Google Drive et Gmail

#### 6. Configurer Gmail

Générer un mot de passe d'application et configurer le serveur MCP Gmail.

## 📖 Utilisation

### 1. Market Watcher - Surveillance quotidienne

**Lancement manuel** :
```bash
claude-code agent run market-watcher-pea
```

**Automatisation via cron** (recommandé) :
```bash
# Éditer crontab
crontab -e

# Ajouter cette ligne pour exécution quotidienne à 8h (jours ouvrés)
0 8 * * 1-5 cd /path/to/pea-tracker && claude-code agent run market-watcher-pea
```

**Ce que fait l'agent** :
1. ✅ Récupère la watchlist depuis Google Drive
2. ✅ Analyse les titres actifs avec Yahoo Finance
3. ✅ Calcule les indicateurs techniques (RSI, MACD, MA20/50/200)
4. ✅ Génère les signaux d'achat/vente avec scoring
5. ✅ Sauvegarde les rapports dans Google Drive
6. ✅ Envoie les alertes par email (score ≥ 60)

### 2. Export Boursorama

Pour alimenter le Portfolio Advisor (à venir) :

1. Se connecter à Boursorama
2. PEA → Télécharger les positions comptables (CSV)
3. Uploader dans `Google Drive/PEA-Tracker/Imports/`

### 3. Environnement Python (optionnel)

Pour les dépendances Python des agents :

```bash
# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Utiliser pip-mode standard
/pip-mode standard
```

## 📊 Signaux et indicateurs

### Types de signaux générés

- 🟢 **BUY** : Opportunité d'achat détectée (RSI < 30, MACD haussier, etc.)
- 🔴 **SELL** : Signal de vente (RSI > 70, divergence baissière, etc.)
- 🟡 **WATCH** : Surveillance recommandée (consolidation, signaux mixtes)

### Indicateurs techniques calculés

- **RSI (14 périodes)** : Détection de surachat/survente
- **MACD (12, 26, 9)** : Identification des tendances
- **Moyennes mobiles** : MA20, MA50, MA200 (support/résistance)
- **Volume ratio** : Confirmation des mouvements

### Scoring de confiance

Chaque signal est accompagné d'un **score de confiance (0-100)** basé sur :
- Convergence des indicateurs
- Force du signal
- Contexte de marché
- Volume de transactions

**Alertes email** : Envoyées uniquement pour les signaux ≥ 60

## 🔧 Configuration avancée

### Personnaliser la watchlist

Éditer le fichier `PEA_Watchlist_Indicateurs.xlsx` sur Google Drive :

**Feuille "Watchlist"** :
- Colonne A : Ticker (ex: MC.PA, AIR.PA)
- Colonne B : Nom de l'entreprise
- Colonne C : Statut (actif/inactif)

**Feuille "Indicateurs"** :
- Mise à jour automatique par l'agent
- Historique des calculs

**Feuille "Positions"** :
- Vos positions actuelles
- Prix d'achat, quantité, stop-loss

### Automatisation complète

**Crontab Linux/Mac** :
```bash
# Market Watcher tous les jours ouvrés à 8h
0 8 * * 1-5 cd /path/to/pea-tracker && claude-code agent run market-watcher-pea

# Portfolio Advisor le 1er de chaque mois à 9h (quand disponible)
# 0 9 1 * * cd /path/to/pea-tracker && claude-code agent run portfolio-advisor
```

**Task Scheduler Windows** :
Créer une tâche planifiée avec déclencheur quotidien.

## 🐛 Dépannage

### Les alertes ne sont pas envoyées

1. Vérifier la configuration Gmail MCP dans `.claude/settings.local.json`
2. Vérifier que des signaux avec score ≥ 60 ont été générés
3. Consulter les logs de l'agent
4. Tester l'envoi d'email manuellement

### Erreur d'accès Google Drive

1. Vérifier l'authentification OAuth
2. Vérifier les permissions du dossier PEA-Tracker
3. Régénérer le token si nécessaire

### Erreur Yahoo Finance

1. Vérifier le format des tickers (ex: MC.PA pour LVMH)
2. Vérifier la connexion internet
3. Attendre quelques minutes (rate limiting possible)

### L'agent ne trouve pas la watchlist

1. Vérifier le nom exact du fichier : `PEA_Watchlist_Indicateurs.xlsx`
2. Vérifier qu'il est dans le dossier `PEA-Tracker/` à la racine de Google Drive
3. Vérifier les permissions de lecture

## 🔒 Sécurité

- ✅ Clés API stockées dans variables d'environnement
- ✅ Authentification OAuth pour Google services
- ✅ Pas de stockage d'identifiants broker
- ✅ Communications chiffrées (HTTPS)
- ⚠️ Ne jamais commiter `.claude/settings.local.json` ou `.env`

**Fichiers à ne jamais versionner** :
```
.claude/settings.local.json
.env
credentials.json
token.json
```

## 🗺️ Roadmap

### Phase 1 : Infrastructure MCP ✅ TERMINÉE
- [x] Configuration Claude Code
- [x] Installation serveurs MCP
- [x] Authentification Google Drive/Gmail
- [x] Structure Google Drive
- [x] Agent Market Watcher implémenté et opérationnel

### Phase 2 : Portfolio Advisor 🔄 EN COURS
- [ ] Implémenter l'agent Portfolio Advisor
- [ ] Parser les exports Boursorama (CSV)
- [ ] Calculer les métriques de performance
- [ ] Générer les rapports mensuels
- [ ] Automatiser l'envoi des rapports

### Phase 3 : Optimisations 📋 PLANIFIÉE
- [ ] Backtesting des signaux Market Watcher
- [ ] Profil de risque personnalisé
- [ ] Intégration actualités financières (RSS/API)
- [ ] Dashboard web simple (optionnel)
- [ ] Alertes Telegram/SMS (optionnel)

### Phase 4 : Améliorations avancées 🔮 FUTUR
- [ ] Machine Learning pour scoring amélioré
- [ ] Analyse sentiment market (NLP)
- [ ] Intégration données fondamentales
- [ ] Support multi-portefeuilles

## 🤝 Contribution

### Workflow Git

Le projet utilise un workflow Git strict avec commits et push réguliers.

**Convention de commits** :
- `feat:` - Nouvelle fonctionnalité
- `fix:` - Correction de bug
- `docs:` - Documentation uniquement
- `refactor:` - Refactoring
- `test:` - Ajout de tests

Voir [CLAUDE.md - Workflow Git](CLAUDE.md#workflow-de-développement-et-gestion-git) pour les détails complets.

### Proposer une amélioration

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commiter vos changements (`git commit -m 'feat: ajout AmazingFeature'`)
4. Pusher vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### Signaler un bug

Ouvrir une issue avec :
- Description claire du problème
- Étapes pour reproduire
- Logs d'erreur (sans clés API)
- Configuration système

## 📚 Documentation

- **[CLAUDE.md](CLAUDE.md)** - Documentation complète du projet
- **[CHANGELOG.md](CHANGELOG.md)** - Historique des versions
- **[docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md)** - Guide d'installation détaillé
- **[docs/architecture/mcp-integration.md](docs/architecture/mcp-integration.md)** - Architecture MCP
- **[docs/agents/market-watcher-spec.md](docs/agents/market-watcher-spec.md)** - Specs Market Watcher
- **[docs/agents/portfolio-advisor-spec.md](docs/agents/portfolio-advisor-spec.md)** - Specs Portfolio Advisor

## 📜 Glossaire

- **PEA** : Plan d'Épargne en Actions (enveloppe fiscale française)
- **MCP** : Model Context Protocol (standard pour connecter les LLM aux données)
- **RSI** : Relative Strength Index (indicateur de momentum)
- **MACD** : Moving Average Convergence Divergence (indicateur de tendance)
- **Claude Code** : CLI tool pour exécuter des agents Claude

## ⚠️ Disclaimer

**AVERTISSEMENT IMPORTANT**

Ce projet est un **outil d'aide à la décision** utilisant l'analyse technique automatisée. Il **NE CONSTITUE EN AUCUN CAS UN CONSEIL EN INVESTISSEMENT** au sens de l'AMF (Autorité des Marchés Financiers).

**Responsabilités** :
- Toutes les décisions d'investissement restent sous votre **entière responsabilité**
- Les performances passées ne préjugent **pas** des performances futures
- Les marchés financiers comportent des **risques de perte en capital**
- Vous devez toujours effectuer vos **propres recherches**
- Consultez un conseiller financier agréé si nécessaire

**Limites de l'outil** :
- Les analyses sont basées uniquement sur des indicateurs techniques
- Les données peuvent contenir des erreurs ou retards
- L'IA peut générer des recommandations erronées
- Aucune garantie de rentabilité n'est fournie

**Utilisation à vos risques et périls.**

## 📄 Licence

[À définir]

## 🙏 Remerciements

- [Anthropic](https://www.anthropic.com/) pour Claude et Claude Code
- [Model Context Protocol](https://modelcontextprotocol.io/) pour le standard MCP
- [Yahoo Finance](https://finance.yahoo.com/) pour les données de marché gratuites

---

**Version** : 2.0.0
**Dernière mise à jour** : 2026-01-08
**Statut** : Phase 1 terminée, Agent Market Watcher opérationnel
**Architecture** : MCP-native avec Claude Code

Créé avec ❤️ et Claude Code
