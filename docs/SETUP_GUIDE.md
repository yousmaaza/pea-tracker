# Guide de Setup - PEA Tracker

Ce guide vous accompagne pas à pas dans l'installation et la configuration de PEA Tracker.

## Prérequis

Avant de commencer, assurez-vous d'avoir :

- [ ] **Node.js 18+** installé (`node --version`)
- [ ] **npm ou npx** disponible (`npm --version`)
- [ ] **Python 3.11+** installé (`python --version` ou `python3 --version`)
- [ ] **uv** (gestionnaire de packages Python) installé (`which uv`)
  - Si non installé : `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Un compte Google (Drive + Gmail)
- [ ] Un compte Anthropic (pour Claude API)
- [ ] Un terminal/shell (bash, zsh, etc.)
- [ ] **Claude Desktop** installé (pour tester les MCP)

**Vérification rapide** :
```bash
node --version    # Doit être >= 18
npm --version
python3 --version # Doit être >= 3.11
uv --version
```

## Architecture MCP

PEA Tracker utilise le **Model Context Protocol (MCP)** pour permettre aux agents Claude d'accéder directement aux données :

- **Google Drive MCP** : Accès aux fichiers (watchlist, portfolio)
- **Gmail MCP** : Envoi des alertes et rapports
- **Yahoo Finance MCP (local)** : Récupération des données boursières

**Pourquoi un serveur local pour Yahoo Finance ?**
- Le serveur MCP Yahoo Finance est développé en Python avec FastMCP
- Il utilise la bibliothèque `yfinance` pour accéder gratuitement à Yahoo Finance
- Emplacement : `/Users/yousrimaazaoui/Documents/projets/test-debile/yahoo-finance-mcp`
- 9 outils MCP disponibles (prix, historique, actualités, recommandations, etc.)

Pour plus de détails, voir `docs/architecture/mcp-integration.md`.

## Installation complète

### Phase 1 : Configuration de base

#### 1.1 Cloner le projet

```bash
git clone <votre-repo>
cd pea-tracker
```

#### 1.2 Configurer les variables d'environnement

```bash
# Copier le template
cp config/.env.example config/.env

# Éditer avec vos valeurs
nano config/.env
```

Renseigner :
```bash
CLAUDE_API_KEY=sk-ant-xxxxx  # À obtenir sur console.anthropic.com
```

### Phase 2 : Configuration Google Cloud

#### 2.1 Créer un projet Google Cloud

1. Aller sur https://console.cloud.google.com/
2. Créer un nouveau projet "PEA-Tracker"
3. Noter le Project ID

#### 2.2 Activer les APIs nécessaires

Dans Google Cloud Console :
1. Navigation > APIs & Services > Library
2. Chercher et activer :
   - Google Drive API
   - Gmail API
   - Google Sheets API (si utilisation de Sheets)

#### 2.3 Créer les credentials OAuth 2.0

1. APIs & Services > Credentials
2. Create Credentials > OAuth 2.0 Client ID
3. Application type : Desktop app
4. Name : "PEA Tracker Desktop"
5. Télécharger le fichier JSON

#### 2.4 Placer les credentials

```bash
# Créer le dossier
mkdir -p mcp/credentials

# Copier les credentials (adapter le chemin)
cp ~/Downloads/client_secret_*.json mcp/credentials/google-drive-credentials.json
cp ~/Downloads/client_secret_*.json mcp/credentials/gmail-credentials.json
```

### Phase 3 : Installation des serveurs MCP

#### 3.1 Installer les serveurs MCP officiels

```bash
# Google Drive
npm install -g @modelcontextprotocol/server-google-drive

# Gmail
npm install -g @modelcontextprotocol/server-gmail
```

#### 3.2 Configurer le serveur Yahoo Finance local

Le serveur Yahoo Finance MCP est local et utilise Python. Il se trouve dans un dossier séparé.

**Emplacement du serveur** : `/Users/yousrimaazaoui/Documents/projets/test-debile/yahoo-finance-mcp`

```bash
# Se déplacer dans le dossier du serveur
cd /Users/yousrimaazaoui/Documents/projets/test-debile/yahoo-finance-mcp

# Créer l'environnement virtuel et installer les dépendances
uv venv
source .venv/bin/activate  # Sur Mac/Linux
# OU
.venv\Scripts\activate  # Sur Windows

# Installer les dépendances
uv pip install -e .
```

#### 3.3 Vérifier les installations

```bash
# Vérifier les serveurs npm
npx @modelcontextprotocol/server-google-drive --version
npx @modelcontextprotocol/server-gmail --version

# Tester le serveur Yahoo Finance local
cd /Users/yousrimaazaoui/Documents/projets/test-debile/yahoo-finance-mcp
uv run server.py
# Ctrl+C pour arrêter après vérification
```

#### 3.4 Authentification Google

```bash
# Authentifier Google Drive
npx @modelcontextprotocol/server-google-drive authenticate \
  --credentials mcp/credentials/google-drive-credentials.json

# Authentifier Gmail
npx @modelcontextprotocol/server-gmail authenticate \
  --credentials mcp/credentials/gmail-credentials.json
```

Suivre les instructions dans le navigateur pour autoriser l'accès.

**Note** : Le serveur Yahoo Finance ne nécessite pas d'authentification car il utilise l'API publique gratuite de Yahoo Finance via la bibliothèque `yfinance`.

### Phase 4 : Configuration Google Drive

#### 4.1 Créer la structure de dossiers

Créer ces dossiers dans votre Google Drive :

```
PEA-Tracker/
├── Imports/      # Exports Boursorama
├── Data/         # Portefeuille, watchlist
├── Rapports/     # Rapports mensuels
└── Config/       # Configuration
```

#### 4.2 Créer les fichiers de données

**watchlist.csv** (dans Data/) :
```csv
ticker,name,market,sector,country,active
MC.PA,LVMH,Euronext Paris,Luxe,France,true
SAN.PA,Sanofi,Euronext Paris,Santé,France,true
SAP.DE,SAP,Xetra,Technologie,Allemagne,true
```

**portfolio.csv** (dans Data/) :
```csv
ticker,name,quantity,avg_buy_price,sector,country
MC.PA,LVMH,50,720,Luxe,France
SAN.PA,Sanofi,40,95,Santé,France
```

#### 4.3 Noter les IDs des dossiers

Obtenir l'ID du dossier principal PEA-Tracker :
1. Ouvrir le dossier dans Google Drive
2. L'URL contient l'ID : `drive.google.com/drive/folders/[FOLDER_ID]`
3. Copier l'ID

Mettre à jour `.env` :
```bash
GOOGLE_DRIVE_FOLDER_ID=your_folder_id_here
```

### Phase 5 : Test des serveurs MCP

#### 5.1 Test rapide via Claude Desktop

1. Installer Claude Desktop si pas déjà fait

2. Configurer `~/Library/Application Support/Claude/claude_desktop_config.json` :

**Sur Mac** :
```bash
# Ouvrir le fichier de config avec VS Code ou nano
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
# OU
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Configuration à ajouter** :
```json
{
  "mcpServers": {
    "google-drive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-drive"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/CHEMIN_ABSOLU/mcp/credentials/google-drive-credentials.json"
      }
    },
    "gmail": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gmail"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/CHEMIN_ABSOLU/mcp/credentials/gmail-credentials.json"
      }
    },
    "yfinance": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/yousrimaazaoui/Documents/projets/test-debile/yahoo-finance-mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```

**Important** :
- Remplacer `/CHEMIN_ABSOLU/` par le chemin absolu vers votre projet PEA Tracker
- Le serveur `yfinance` utilise le chemin local du serveur Python
- Vérifier que `uv` est installé : `which uv`

3. Redémarrer Claude Desktop complètement (Quit + Reopen)

4. Tester dans une conversation Claude Desktop :

**Test Google Drive** :
```
Peux-tu lister les fichiers dans mon Google Drive qui contiennent "watchlist" ?
```

**Test Yahoo Finance** :
```
Peux-tu récupérer les informations sur LVMH avec le ticker MC.PA en utilisant get_stock_info ?
```

**Test historique** :
```
Récupère l'historique des prix de LVMH (MC.PA) sur 1 an avec get_historical_stock_prices(ticker="MC.PA", period="1y", interval="1d")
```

#### 5.2 Tester Yahoo Finance MCP en détail

**Outils MCP disponibles** :
1. `get_historical_stock_prices` : Historique OHLCV
2. `get_stock_info` : Informations complètes du titre
3. `get_yahoo_finance_news` : Actualités
4. `get_stock_actions` : Dividendes et splits
5. `get_financial_statement` : États financiers
6. `get_holder_info` : Détenteurs institutionnels
7. `get_option_expiration_dates` : Dates expiration options
8. `get_option_chain` : Chaîne d'options
9. `get_recommendations` : Recommandations analystes

**Exemples de tests dans Claude Desktop** :

```
# Test 1 : Prix actuel
Utilise get_stock_info pour récupérer les informations sur Total Energies (TTE.PA)

# Test 2 : Historique
Utilise get_historical_stock_prices pour récupérer l'historique sur 6 mois de LVMH (MC.PA) avec period="6mo" et interval="1d"

# Test 3 : Actualités
Récupère les dernières actualités sur Sanofi (SAN.PA) avec get_yahoo_finance_news

# Test 4 : Recommandations analystes
Utilise get_recommendations pour voir les recommandations sur Air Liquide (AI.PA)
```

Voir `mcp/examples/test-yahoo-finance.md` pour des tests détaillés.

### Phase 6 : Premier lancement des agents

#### 6.1 Test Market Watcher

```bash
# Rendre le script exécutable (si pas déjà fait)
chmod +x scripts/run-market-watcher.sh

# Lancer l'agent
./scripts/run-market-watcher.sh
```

Vérifier dans les logs (`logs/market-watcher-*.log`) :
- Connexion aux serveurs MCP réussie
- Lecture de la watchlist
- Récupération des données Yahoo Finance
- Calcul des indicateurs
- Envoi des alertes (si signaux détectés)

#### 6.2 Test Portfolio Advisor

```bash
# Lancer l'agent (avec --force pour tester hors 1er du mois)
./scripts/run-portfolio-advisor.sh --force
```

Vérifier dans les logs :
- Lecture du portefeuille
- Calcul des performances
- Génération du rapport
- Envoi par email

### Phase 7 : Automatisation

#### 7.1 Configurer les cron jobs

```bash
# Éditer crontab
crontab -e
```

Ajouter :
```bash
# Market Watcher - Tous les jours à 8h
0 8 * * * cd /path/to/pea-tracker && ./scripts/run-market-watcher.sh >> logs/cron-market-watcher.log 2>&1

# Portfolio Advisor - Le 1er de chaque mois à 9h
0 9 1 * * cd /path/to/pea-tracker && ./scripts/run-portfolio-advisor.sh >> logs/cron-portfolio-advisor.log 2>&1
```

**Important** : Remplacer `/path/to/pea-tracker` par le chemin absolu.

#### 7.2 Vérifier les cron jobs

```bash
# Lister les cron jobs
crontab -l

# Tester manuellement une fois
./scripts/run-market-watcher.sh
```

### Phase 8 : Configuration avancée (optionnel)

#### 8.1 Ajuster les seuils d'alertes

Éditer `config/alert-thresholds.json` :
```json
{
  "technical_indicators": {
    "rsi": {
      "oversold": 30,    // Modifier selon votre stratégie
      "overbought": 70
    }
  },
  "alert_scoring": {
    "high_confidence": {
      "min_score": 80    // Score minimum pour alertes prioritaires
    }
  }
}
```

#### 8.2 Personnaliser les notifications

Éditer `config/notification-settings.json` :
```json
{
  "email": {
    "to": "your-email@example.com"  // Votre email
  },
  "notification_preferences": {
    "min_alert_score": 60,     // Score minimum pour envoyer une alerte
    "max_daily_alerts": 10     // Limiter le nombre d'alertes par jour
  }
}
```

## Vérification finale

### Checklist de validation

- [ ] **Prérequis** : Node.js, Python 3.11+, uv installés
- [ ] **Serveurs MCP** :
  - [ ] Google Drive MCP installé et authentifié
  - [ ] Gmail MCP installé et authentifié
  - [ ] Yahoo Finance MCP local configuré (serveur Python)
- [ ] **Configuration Claude Desktop** :
  - [ ] Fichier `claude_desktop_config.json` mis à jour
  - [ ] Les 3 serveurs MCP configurés (google-drive, gmail, yfinance)
  - [ ] Claude Desktop redémarré
- [ ] **Tests MCP dans Claude Desktop** :
  - [ ] Test Google Drive réussi (liste fichiers)
  - [ ] Test Yahoo Finance réussi (get_stock_info)
  - [ ] Test historique réussi (get_historical_stock_prices)
- [ ] **Google Drive** :
  - [ ] Structure de dossiers créée (PEA-Tracker/*)
  - [ ] Fichiers watchlist.csv et portfolio.csv créés
- [ ] **Agents** :
  - [ ] Test Market Watcher réussi manuellement
  - [ ] Test Portfolio Advisor réussi manuellement
  - [ ] Premier email de test reçu
- [ ] **Automatisation** :
  - [ ] Les cron jobs sont configurés

### Test de bout en bout

1. Ajouter un ticker à la watchlist
2. Lancer Market Watcher manuellement
3. Vérifier réception de l'alerte (si signal détecté)
4. Vérifier les logs

## Dépannage

### Erreur : "CLAUDE_API_KEY not found"

Vérifier que `config/.env` contient la clé API Claude :
```bash
cat config/.env | grep CLAUDE_API_KEY
```

### Erreur : "Google authentication failed"

Réauthentifier :
```bash
npx @modelcontextprotocol/server-google-drive authenticate \
  --credentials mcp/credentials/google-drive-credentials.json
```

### Erreur : "File not found in Google Drive"

Vérifier :
1. Le fichier existe bien dans Google Drive
2. Les permissions de partage
3. Le nom du fichier est correct (watchlist.csv, pas watchlist.xlsx)

### Les cron jobs ne s'exécutent pas

Vérifier :
```bash
# Logs système cron
grep CRON /var/log/syslog  # Linux
log show --predicate 'process == "cron"' --last 1h  # Mac

# Vérifier les permissions
chmod +x scripts/run-market-watcher.sh
chmod +x scripts/run-portfolio-advisor.sh

# Tester manuellement
cd /path/to/pea-tracker && ./scripts/run-market-watcher.sh
```

### Yahoo Finance ne retourne pas de données

Vérifier :
1. Le format du ticker (MC.PA, pas MC)
2. Le marché est ouvert ou données disponibles
3. Le serveur MCP est bien configuré dans Claude Desktop
4. Tester manuellement le serveur :
```bash
cd /Users/yousrimaazaoui/Documents/projets/test-debile/yahoo-finance-mcp
uv run server.py
# Le serveur doit démarrer sans erreurs
```
5. Vérifier que `uv` est installé : `which uv`
6. Vérifier les logs de Claude Desktop pour voir les erreurs MCP

**Erreur courante** : "command not found: uv"
```bash
# Installer uv si nécessaire
curl -LsSf https://astral.sh/uv/install.sh | sh
# OU
pip install uv
```

## Support

### Documentation
- [Documentation MCP](docs/architecture/mcp-integration.md)
- [Yahoo Finance Integration](docs/mcp/yahoo-finance-integration.md)
- [Spécifications des agents](docs/agents/)

### Logs
Tous les logs sont dans `logs/` :
- `market-watcher-*.log` : Logs Market Watcher
- `portfolio-advisor-*.log` : Logs Portfolio Advisor
- `cron-*.log` : Logs des exécutions cron

### Aide supplémentaire

Pour des questions spécifiques :
1. Consulter la documentation dans `docs/`
2. Vérifier les logs d'erreur
3. Tester les serveurs MCP individuellement

## Prochaines étapes

Une fois le setup terminé :

1. **Personnaliser la watchlist** : Ajouter vos titres préférés
2. **Ajuster les seuils** : Adapter à votre profil de risque
3. **Monitorer les premières alertes** : Valider la pertinence
4. **Optimiser les prompts** : Améliorer la qualité des analyses
5. **Backtest** : Analyser la précision des signaux sur historique

---

**Félicitations!** Votre système PEA Tracker est maintenant opérationnel. 🎉

**Temps estimé de setup** : 1-2 heures
**Difficulté** : Intermédiaire

---

**Version** : 1.0
**Dernière mise à jour** : 2026-01-07
