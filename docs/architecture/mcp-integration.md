# Intégration MCP (Model Context Protocol) - PEA Tracker

## Vue d'ensemble

PEA Tracker utilise le **Model Context Protocol (MCP)** pour permettre aux agents IA Claude d'accéder directement aux données sans passer par des APIs intermédiaires. Cette approche simplifie l'architecture et améliore les performances.

## Qu'est-ce que MCP?

MCP (Model Context Protocol) est un protocole standardisé qui permet aux modèles d'IA d'interagir directement avec des sources de données et des outils externes de manière sécurisée et contrôlée.

### Avantages pour PEA Tracker

1. **Accès direct aux données** : Les agents Claude peuvent lire/écrire dans Google Drive et récupérer des données financières sans middleware
2. **Simplification** : Pas besoin de développer des APIs intermédiaires ou des parseurs complexes
3. **Sécurité** : Gestion des permissions au niveau MCP
4. **Temps réel** : Accès instantané aux données les plus récentes
5. **Coûts réduits** : Moins d'infrastructure à maintenir

## Architecture MCP pour PEA Tracker

### Schéma d'architecture révisé

```
┌─────────────────────────────────────────────────────────────┐
│                    Utilisateur                               │
│  - Dépose exports Boursorama dans Google Drive              │
│  - Reçoit alertes et rapports par email                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     v
┌─────────────────────────────────────────────────────────────┐
│                  Google Drive (Stockage)                     │
│  - PEA-Tracker/Imports/     (Exports Boursorama)           │
│  - PEA-Tracker/Data/        (Portefeuille, Watchlist)      │
│  - PEA-Tracker/Rapports/    (Rapports mensuels)            │
│  - PEA-Tracker/Config/      (Configuration)                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ MCP Google Drive
                     v
┌─────────────────────────────────────────────────────────────┐
│              Agent Market Watcher (Claude)                   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  MCP Tools disponibles:                              │  │
│  │  - mcp__googledrive__*  (lecture/écriture Drive)    │  │
│  │  - mcp__yahoo_finance__* (données boursières)       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  Workflow:                                                   │
│  1. Lit watchlist via MCP Google Drive                      │
│  2. Récupère données via MCP Yahoo Finance                  │
│  3. Analyse et génère signaux                               │
│  4. Envoie alertes via MCP Gmail                            │
└─────────────────────────────────────────────────────────────┘
                     │
                     │ MCP Gmail
                     v
┌─────────────────────────────────────────────────────────────┐
│              Agent Portfolio Advisor (Claude)                │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  MCP Tools disponibles:                              │  │
│  │  - mcp__googledrive__*  (lecture portefeuille)      │  │
│  │  - mcp__gmail__*         (envoi rapport)             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  Workflow:                                                   │
│  1. Lit portefeuille via MCP Google Drive                   │
│  2. Analyse et calcule métriques                            │
│  3. Génère rapport avec recommandations                     │
│  4. Envoie rapport via MCP Gmail                            │
└─────────────────────────────────────────────────────────────┘
                     │
                     v
┌─────────────────────────────────────────────────────────────┐
│                    Gmail (Notifications)                     │
│  - Alertes Market Watcher                                   │
│  - Rapports mensuels Portfolio Advisor                      │
└─────────────────────────────────────────────────────────────┘
```

## MCP Servers utilisés

### 1. MCP Google Drive

**Serveur** : `@modelcontextprotocol/server-google-drive`

**Fonctionnalités utilisées** :

**Pour Market Watcher** :
- `mcp__googledrive__find_file` : Trouver la watchlist
- `mcp__googledrive__download_file` : Télécharger fichiers de données
- `mcp__googledrive__get_file_metadata` : Vérifier les modifications
- `mcp__googledrive__create_file_from_text` : Logger les signaux

**Pour Portfolio Advisor** :
- `mcp__googledrive__find_file` : Localiser fichiers portefeuille
- `mcp__googledrive__download_file` : Télécharger données
- `mcp__googledrive__list_files` : Lister historique transactions
- `mcp__googledrive__upload_file` : Sauvegarder rapports

**Configuration** :
```json
{
  "mcpServers": {
    "google-drive": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-google-drive"
      ],
      "env": {
        "GOOGLE_DRIVE_CREDENTIALS": "/path/to/credentials.json",
        "GOOGLE_DRIVE_TOKEN": "/path/to/token.json"
      }
    }
  }
}
```

### 2. MCP Yahoo Finance

**Serveur** : `yahoo-finance-mcp` (serveur local développé avec FastMCP)
**Chemin** : `/Users/yousrimaazaoui/Documents/projets/test-debile/yahoo-finance-mcp`

**Outils MCP disponibles** :
- `get_historical_stock_prices(ticker, period, interval)` : Historique OHLCV
- `get_stock_info(ticker)` : Informations détaillées (prix, volume, métriques)
- `get_yahoo_finance_news(ticker)` : Actualités financières
- `get_stock_actions(ticker)` : Dividendes et splits
- `get_financial_statement(ticker, financial_type)` : États financiers
- `get_holder_info(ticker, holder_type)` : Détenteurs et insiders
- `get_option_expiration_dates(ticker)` : Dates d'expiration options
- `get_option_chain(ticker, expiration_date, option_type)` : Chaîne d'options
- `get_recommendations(ticker, recommendation_type, months_back)` : Recommandations analystes

**Configuration Claude Desktop** :
```json
{
  "mcpServers": {
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

**Exemple d'utilisation pour Market Watcher** :
```python
# Récupérer informations actuelles
info = get_stock_info(ticker="MC.PA")

# Récupérer historique pour indicateurs techniques
history = get_historical_stock_prices(
    ticker="MC.PA",
    period="1y",  # 1 an pour MA200
    interval="1d"  # Quotidien
)

# Récupérer actualités (optionnel)
news = get_yahoo_finance_news(ticker="MC.PA")
```

### 3. MCP Gmail

**Serveur** : `@modelcontextprotocol/server-gmail` (si disponible)

**Fonctionnalités utilisées** :
- `mcp__gmail__send_email` : Envoi des alertes et rapports
- `mcp__gmail__create_email_draft` : Brouillons pour validation (optionnel)

**Configuration** :
```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-gmail"
      ],
      "env": {
        "GMAIL_CREDENTIALS": "/path/to/gmail-credentials.json",
        "GMAIL_TOKEN": "/path/to/gmail-token.json"
      }
    }
  }
}
```

## Flux de données avec MCP

### Flux Market Watcher

```
1. Déclencheur (Cron 8h00)
   ↓
2. Agent Claude activé avec prompt market-analysis.md
   ↓
3. Agent utilise mcp__googledrive__find_file("watchlist.csv")
   → Récupère la liste des tickers à surveiller
   ↓
4. Pour chaque ticker:
   Agent utilise get_stock_info(ticker) et get_historical_stock_prices(ticker, period="1y", interval="1d")
   → Récupère prix actuel, volume, et historique pour calcul des indicateurs
   ↓
5. Agent calcule les indicateurs techniques
   (RSI, MACD, MM) dans sa logique interne
   ↓
6. Agent analyse et génère signaux avec scoring
   ↓
7. Si signal pertinent (score >= 60):
   Agent utilise mcp__gmail__send_email(alert)
   → Envoie l'alerte formatée
   ↓
8. Agent utilise mcp__googledrive__create_file_from_text(log)
   → Sauvegarde historique des signaux
```

### Flux Portfolio Advisor

```
1. Déclencheur (Cron 1er du mois 9h00)
   ↓
2. Agent Claude activé avec prompt portfolio-review.md
   ↓
3. Agent utilise mcp__googledrive__find_file("portfolio.csv")
   → Récupère positions actuelles
   ↓
4. Agent utilise mcp__googledrive__list_files("transactions/")
   → Liste historique des transactions
   ↓
5. Agent lit les fichiers de transactions
   mcp__googledrive__download_file(transaction_id)
   ↓
6. Agent calcule:
   - Performance (MTD, YTD, Total)
   - Allocation (sectorielle, géographique)
   - Diversification (Herfindahl, ENS)
   ↓
7. Agent génère rapport avec recommandations
   (texte formaté en Markdown/HTML)
   ↓
8. Agent utilise mcp__gmail__send_email(report)
   → Envoie le rapport mensuel
   ↓
9. Agent utilise mcp__googledrive__upload_file(report)
   → Sauvegarde le rapport dans Drive
```

## Avantages par rapport à l'architecture n8n

### Architecture initiale (n8n + APIs)

```
n8n workflow:
1. Scheduler → 2. Google Drive API → 3. Parse data →
4. Yahoo Finance API → 5. Calculate indicators →
6. Claude API (analyse) → 7. Gmail API
```

**Complexité** : 7 étapes, 4 APIs différentes, parsing manuel

### Architecture MCP

```
Claude Agent avec MCP:
1. Scheduler → 2. Claude (avec accès MCP direct)
```

**Simplicité** : 2 étapes, l'agent Claude gère tout via MCP

### Comparaison

| Aspect | n8n + APIs | MCP |
|--------|-----------|-----|
| Complexité | Haute (7+ nodes) | Faible (1 agent) |
| Maintenance | Nombreux points de défaillance | Centralisée |
| Flexibilité | Rigide (workflow fixe) | Haute (agent adaptatif) |
| Coûts | n8n cloud + APIs | Seulement Claude API |
| Développement | Chaque workflow à créer | Prompts à optimiser |
| Évolutions | Modifier workflows | Ajuster prompts |

## Architecture hybride recommandée

Pour débuter, une approche hybride peut être pertinente :

### Phase 1 : MCP pur (Recommandé)

**Avantages** :
- Plus simple à démarrer
- Moins de composants
- Plus flexible
- Coûts réduits

**Utilisation** :
- Les agents Claude sont invoqués directement (via Claude Desktop, API, ou Claude Code)
- Utilisation des MCP servers pour accès aux données
- Pas besoin de n8n

**Scheduling** :
- Utiliser un cron job système simple :
```bash
# Crontab
0 8 * * * /usr/local/bin/run-market-watcher.sh
0 9 1 * * /usr/local/bin/run-portfolio-advisor.sh
```

### Phase 2 : Hybride (Optionnel)

Si besoin de workflows complexes plus tard :
- n8n pour l'orchestration et le scheduling
- Appels à Claude avec MCP pour l'analyse
- Best of both worlds

## Configuration MCP pour le projet

### Structure des fichiers MCP

```
pea-tracker/
├── mcp/
│   ├── config.json              # Configuration MCP globale
│   ├── google-drive-config.json # Config Google Drive
│   ├── gmail-config.json        # Config Gmail
│   └── yahoo-finance-config.json # Config Yahoo Finance
└── scripts/
    ├── run-market-watcher.sh    # Script lancement Market Watcher
    └── run-portfolio-advisor.sh # Script lancement Portfolio Advisor
```

### Fichier de configuration MCP principal

**mcp/config.json** :
```json
{
  "mcpServers": {
    "google-drive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-drive"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "./mcp/google-drive-credentials.json"
      }
    },
    "gmail": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gmail"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "./mcp/gmail-credentials.json"
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

## Scripts d'exécution des agents

### Script Market Watcher

**scripts/run-market-watcher.sh** :
```bash
#!/bin/bash

# Configuration
CLAUDE_API_KEY="${CLAUDE_API_KEY}"
MCP_CONFIG="./mcp/config.json"
PROMPT_FILE="./prompts/market-analysis.md"

# Logs
LOG_DIR="./logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/market-watcher-$(date +%Y%m%d-%H%M%S).log"

echo "Starting Market Watcher Agent..." | tee -a "$LOG_FILE"

# Lancer l'agent Claude avec MCP
# (Commande à adapter selon votre méthode d'invocation)
claude-code agent run \
  --prompt-file "$PROMPT_FILE" \
  --mcp-config "$MCP_CONFIG" \
  --log-file "$LOG_FILE"

echo "Market Watcher completed" | tee -a "$LOG_FILE"
```

### Script Portfolio Advisor

**scripts/run-portfolio-advisor.sh** :
```bash
#!/bin/bash

# Configuration
CLAUDE_API_KEY="${CLAUDE_API_KEY}"
MCP_CONFIG="./mcp/config.json"
PROMPT_FILE="./prompts/portfolio-review.md"

# Logs
LOG_DIR="./logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/portfolio-advisor-$(date +%Y%m%d-%H%M%S).log"

echo "Starting Portfolio Advisor Agent..." | tee -a "$LOG_FILE"

# Lancer l'agent Claude avec MCP
claude-code agent run \
  --prompt-file "$PROMPT_FILE" \
  --mcp-config "$MCP_CONFIG" \
  --log-file "$LOG_FILE"

echo "Portfolio Advisor completed" | tee -a "$LOG_FILE"
```

## Prochaines étapes

### Setup MCP (Phase 1)

1. **Installer les MCP servers** :
```bash
npm install -g @modelcontextprotocol/server-google-drive
npm install -g @modelcontextprotocol/server-gmail
```

2. **Configurer les credentials Google** :
   - Créer projet Google Cloud
   - Activer APIs Drive et Gmail
   - Télécharger credentials OAuth 2.0
   - Placer dans `mcp/`

3. **Serveur Yahoo Finance** : ✅ **DÉJÀ CONFIGURÉ**
   - Serveur local : `/Users/yousrimaazaoui/Documents/projets/test-debile/yahoo-finance-mcp`
   - Configuration Claude Desktop déjà en place
   - 9 outils MCP disponibles (voir section "MCP Yahoo Finance")

4. **Tester les agents** :
   - Lancer Market Watcher manuellement
   - Vérifier accès aux données
   - Valider génération des alertes

5. **Automatiser** :
   - Configurer cron jobs
   - Mettre en place monitoring
   - Logger les exécutions

## Ressources

### Documentation MCP
- [Model Context Protocol Spec](https://modelcontextprotocol.io/)
- [MCP Servers Registry](https://github.com/modelcontextprotocol/servers)
- [Claude MCP Documentation](https://docs.anthropic.com/claude/docs/mcp)

### Serveurs MCP disponibles
- [@modelcontextprotocol/server-google-drive](https://github.com/modelcontextprotocol/servers/tree/main/src/google-drive)
- [@modelcontextprotocol/server-gmail](https://github.com/modelcontextprotocol/servers/tree/main/src/gmail)

### Développement MCP custom
- [MCP SDK](https://github.com/modelcontextprotocol/sdk)
- [Building MCP Servers Guide](https://modelcontextprotocol.io/docs/building-servers)

## Questions ouvertes

1. **Serveur MCP Yahoo Finance** : ✅ **RÉSOLU**
   - Serveur local développé avec FastMCP
   - Basé sur yfinance Python library
   - Configuration dans Claude Desktop : voir section "MCP Yahoo Finance"

2. **Scheduling** :
   - Cron jobs système suffisant ?
   - Besoin de n8n pour orchestration complexe ?

3. **Monitoring** :
   - Comment monitorer les exécutions des agents ?
   - Alertes en cas d'échec ?

4. **Coûts Claude API** :
   - Estimation précise avec MCP ?
   - Optimisation des prompts pour réduire tokens ?

---

**Version** : 1.0
**Dernière mise à jour** : 2026-01-07
