# Spécifications Agent Market Watcher

## Vue d'ensemble

L'Agent Market Watcher est responsable de la surveillance temps réel des marchés financiers et de la génération d'alertes d'opportunités sur les titres éligibles PEA.

## Objectifs

1. **Surveiller** en continu les indicateurs techniques des titres en watchlist
2. **Détecter** les signaux d'achat et de vente avec précision
3. **Scorer** la fiabilité de chaque signal (0-100)
4. **Alerter** l'utilisateur avec des notifications contextualisées
5. **Tracker** l'historique des signaux pour amélioration continue

## Responsabilités détaillées

### 1. Analyse technique

#### Indicateurs surveillés

**RSI (Relative Strength Index)**
- Période : 14 jours
- Seuil survente : < 30
- Seuil surachat : > 70
- Zones d'attention : 30-40 et 60-70

**MACD (Moving Average Convergence Divergence)**
- EMA rapide : 12 périodes
- EMA lente : 26 périodes
- Signal : 9 périodes
- Croisements surveillés :
  - Haussier : MACD > Signal
  - Baissier : MACD < Signal

**Moyennes Mobiles (MM)**
- MM20 : Tendance court terme
- MM50 : Tendance moyen terme
- MM200 : Tendance long terme
- Croisements clés :
  - Golden Cross : MM50 > MM200
  - Death Cross : MM50 < MM200

**Volume**
- Volume moyen sur 20 jours
- Détection des pics de volume (> 1.5x moyenne)
- Corrélation volume/prix

#### Analyse fondamentale (optionnel V2)
- Actualités importantes (résultats, acquisitions)
- Changements de recommandations analystes
- Événements corporate majeurs

### 2. Génération de signaux

#### Types de signaux

**Signal d'achat (🟢)**
Conditions de déclenchement :
- RSI < 35 ET volume > moyenne
- Prix touche support (MA200) avec rebond
- Croisement haussier MACD
- Golden Cross récent (MM50 > MM200)

Score de confiance élevé si :
- 3+ conditions remplies
- Contexte de marché favorable
- Tendance long terme positive (> MA200)

**Signal de vente (🔴)**
Conditions de déclenchement :
- RSI > 65 ET volume anormal
- Prix atteint résistance avec rejet
- Croisement baissier MACD
- Divergence prix/RSI

Score de confiance élevé si :
- 3+ conditions remplies
- Signes d'essoufflement
- Contexte macro défavorable

**Signal de surveillance (🟡)**
Conditions de déclenchement :
- RSI entre 30-40 ou 60-70
- Prix proche support/résistance majeur
- Volume anormal sans direction claire
- Pattern de consolidation

### 3. Scoring de fiabilité

#### Méthodologie

**Score 80-100 : Haute confiance**
- Convergence de 3+ indicateurs techniques
- Volume confirmant le signal
- Tendance claire
- Contexte macro favorable
- Historique de réussite de ce pattern

**Score 60-79 : Confiance moyenne**
- Convergence de 2 indicateurs
- Signal technique clair
- Contexte mixte
- Quelques facteurs contradictoires

**Score 40-59 : Confiance faible**
- 1 indicateur actif seulement
- Signaux contradictoires mineurs
- Contexte incertain
- Pattern peu fiable historiquement

**Score 0-39 : Pas de signal actionnable**
- Indicateurs neutres ou contradictoires
- Pas de pattern clair
- Attente recommandée

#### Facteurs de pondération

| Facteur | Poids | Impact |
|---------|-------|--------|
| Convergence indicateurs | 30% | +/- 30 points |
| Volume confirmation | 20% | +/- 20 points |
| Tendance long terme | 20% | +/- 20 points |
| Contexte marché | 15% | +/- 15 points |
| Historique pattern | 15% | +/- 15 points |

### 4. Notifications

#### Structure d'une alerte

```
Subject: 🟢 [PEA Tracker] Opportunité d'achat sur LVMH (Score: 85/100)

Corps:
═══════════════════════════════════════
🎯 SIGNAL D'ACHAT DÉTECTÉ
═══════════════════════════════════════

📊 Titre: LVMH (MC.PA)
💰 Prix actuel: 750.50 €
📉 Variation jour: -2.3%
🎯 Score de confiance: 85/100

───────────────────────────────────────
📝 RÉSUMÉ
───────────────────────────────────────
Le titre LVMH présente un signal d'achat fort avec un RSI en zone de survente (32) et un volume supérieur à la moyenne (+32%). Le prix est proche du support MA200 à 720€, offrant un bon point d'entrée technique.

───────────────────────────────────────
✅ POINTS CLÉS
───────────────────────────────────────
• RSI en zone de survente (32) suggère un rebond potentiel
• Volume élevé (+32% vs moyenne) confirme l'intérêt des acheteurs
• Support technique majeur sur MA200 à 720€
• MACD montre des signes précoces de retournement haussier
• Secteur du luxe résilient dans le contexte actuel

───────────────────────────────────────
⚠️ RISQUES IDENTIFIÉS
───────────────────────────────────────
• Tendance court terme encore baissière (sous MA20 et MA50)
• Contexte macro à surveiller (croissance européenne)
• Exposition à la demande asiatique (40% du CA)

───────────────────────────────────────
💡 SUGGESTION D'ACTION
───────────────────────────────────────
Surveiller un franchissement de la MA20 (760€) pour confirmer le retournement. Position initiale possible avec stop-loss à 710€ (-5.4%).

🎯 Objectifs:
• Court terme (1-3 mois): 780€ (+3.9%)
• Moyen terme (3-6 mois): 820€ (+9.3%)

═══════════════════════════════════════
⚖️ DISCLAIMER
═══════════════════════════════════════
Cette analyse est informative et ne constitue pas un conseil en investissement. Les décisions d'investissement restent sous votre responsabilité.

---
Généré automatiquement par PEA Tracker
[Date et heure]
```

#### Paramètres de notification

**Fréquence** :
- Maximum 1 alerte par titre par jour
- Maximum 10 alertes totales par jour
- Regroupement des alertes similaires

**Filtres** :
- Seuil minimum de confiance : 60/100
- Uniquement titres en watchlist active
- Pas d'alerte en dehors heures de marché

**Canaux** :
- Email (Gmail) - Principal
- Webhook (optionnel pour intégrations)

### 5. Historique et tracking

#### Données enregistrées

Pour chaque signal généré :
```json
{
  "signal_id": "uuid",
  "timestamp": "2024-12-05T08:30:00Z",
  "ticker": "MC.PA",
  "signal_type": "buy",
  "confidence_score": 85,
  "price_at_signal": 750.50,
  "indicators": {
    "rsi": 32,
    "macd": {...},
    "volume_ratio": 1.32
  },
  "notification_sent": true,
  "user_action": null,
  "outcome": {
    "price_7d": null,
    "price_30d": null,
    "profitable": null
  }
}
```

#### Métriques de performance

Tracking pour amélioration continue :
- Taux de réussite des signaux (par score)
- Précision par type de signal (achat/vente)
- Performance moyenne par indicateur
- Faux positifs / faux négatifs

## Architecture technique

### Architecture MCP-native

L'agent Market Watcher utilise le **Model Context Protocol (MCP)** pour accéder directement aux données sans infrastructure intermédiaire.

```
┌─────────────────────────────────────────────────────────┐
│                    Scheduler (Cron)                      │
│                Tous les jours à 8h                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     v
┌─────────────────────────────────────────────────────────┐
│              Agent Market Watcher (Claude)               │
│                                                          │
│  Prompt: prompts/market-analysis.md                     │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  MCP Tools disponibles:                            │ │
│  │                                                     │ │
│  │  Google Drive:                                     │ │
│  │  - find_file("watchlist")                          │ │
│  │  - download_file(file_id)                          │ │
│  │  - create_file_from_text(log)                      │ │
│  │                                                     │ │
│  │  Yahoo Finance (yfinance):                         │ │
│  │  - get_stock_info(ticker)                          │ │
│  │  - get_historical_stock_prices(ticker, period)     │ │
│  │  - get_yahoo_finance_news(ticker)                  │ │
│  │  - get_recommendations(ticker)                     │ │
│  │                                                     │ │
│  │  Gmail:                                            │ │
│  │  - send_email(to, subject, body)                   │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Workflow autonome:                                      │
│  1. Lit watchlist via Google Drive MCP                  │
│  2. Pour chaque ticker:                                 │
│     - Récupère données via Yahoo Finance MCP            │
│     - Calcule indicateurs (RSI, MACD, MM)               │
│     - Génère signal avec scoring                        │
│  3. Filtre signaux (score >= 60)                        │
│  4. Envoie alertes via Gmail MCP                        │
│  5. Log historique via Google Drive MCP                 │
└─────────────────────────────────────────────────────────┘
                     │
                     v
┌─────────────────────────────────────────────────────────┐
│              Sorties (via MCP)                           │
│                                                          │
│  - Gmail : Alertes formatées (HTML)                     │
│  - Google Drive : Logs des signaux                      │
└─────────────────────────────────────────────────────────┘
```

**Avantages MCP vs n8n** :
- ✅ Architecture simplifiée (1 agent au lieu de 10+ nodes)
- ✅ Agent autonome et adaptatif
- ✅ Moins de maintenance
- ✅ Pas de parsing manuel
- ✅ Coûts réduits (pas de n8n cloud)

### APIs et MCP utilisés

**Yahoo Finance MCP (Local)**
- Serveur : `yahoo-finance-mcp` (FastMCP + yfinance)
- Chemin : `/Users/yousrimaazaoui/Documents/projets/test-debile/yahoo-finance-mcp`
- Outils principaux :
  - `get_stock_info(ticker)` : Prix actuel, volume, métriques
  - `get_historical_stock_prices(ticker, period, interval)` : Historique OHLCV
  - `get_yahoo_finance_news(ticker)` : Actualités
  - `get_recommendations(ticker, recommendation_type)` : Recommandations analystes
- Rate limit : Aucun (local), limité par Yahoo Finance API (gratuit)
- Coût : Gratuit

**Agent Claude**
- Architecture : MCP-native (accès direct aux données via MCP)
- Modèle: `claude-3-5-sonnet-20241022` ou supérieur
- Max tokens: 4096
- Coût estimé: ~0.003€ par analyse

### Dépendances

**MCP Servers** :
- `yahoo-finance-mcp` : Serveur local (Python + FastMCP + yfinance)
- `@modelcontextprotocol/server-google-drive` : MCP Google Drive
- `@modelcontextprotocol/server-gmail` : MCP Gmail

**Configuration** : Voir `docs/architecture/mcp-integration.md`

## Configuration

### Variables d'environnement

```bash
# Claude API (pour exécution via scripts)
CLAUDE_API_KEY=sk-ant-xxxxx
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# Configuration MCP
# Les serveurs MCP sont configurés dans claude_desktop_config.json
# Voir: ~/Library/Application Support/Claude/claude_desktop_config.json

# Chemins Google Drive (à définir dans la watchlist)
DRIVE_FOLDER_WATCHLIST="PEA-Tracker/Data"
DRIVE_FOLDER_SIGNALS_LOG="PEA-Tracker/Rapports/Signaux"

# Paramètres de l'agent (à définir dans le prompt ou config)
MIN_CONFIDENCE_SCORE=60
MAX_DAILY_ALERTS=10
EMAIL_TO=your-email@example.com
```

**Note** : Avec MCP, les credentials Google (Drive, Gmail) et Yahoo Finance sont gérés par les serveurs MCP, pas par l'agent directement.

### Watchlist format (Google Sheets)

| Ticker | Name | Market | Sector | Country | Active | Priority |
|--------|------|--------|--------|---------|--------|----------|
| MC.PA | LVMH | Euronext Paris | Luxe | France | TRUE | HIGH |
| SAN.PA | Sanofi | Euronext Paris | Santé | France | TRUE | MEDIUM |
| SAP.DE | SAP | Xetra | Tech | Allemagne | TRUE | HIGH |

## Tests et validation

### Tests unitaires

- Calcul correct des indicateurs techniques
- Parsing des données Yahoo Finance
- Génération du prompt Claude
- Scoring de confiance

### Tests d'intégration

- Workflow complet end-to-end
- Gestion des erreurs API
- Rate limiting
- Notifications multiples

### Tests de performance

- Temps d'exécution par ticker : < 5s
- Temps total pour 20 tickers : < 2 minutes
- Coût Claude API : < 0.10€ par exécution

## Métriques de succès

| KPI | Cible | Mesure |
|-----|-------|--------|
| Précision signaux achat | > 60% | Profitable à 30 jours |
| Précision signaux vente | > 55% | Profitable à 30 jours |
| Faux positifs | < 30% | Signaux non confirmés |
| Latence notification | < 10 min | Après ouverture marché |
| Coût mensuel | < 10€ | APIs + Claude |

## Évolutions futures (V2)

1. **Machine Learning** : Améliorer le scoring avec historique
2. **Actualités** : Intégration sentiment analysis sur news
3. **Backtesting** : Validation historique des signaux
4. **Personnalisation** : Profils de risque utilisateur
5. **Multi-timeframes** : Signaux intraday et long terme
6. **Alertes push** : Notifications mobiles temps réel

## Ressources

- [Prompt de l'agent](../../prompts/market-analysis.md) ⭐ **Principal**
- [Architecture MCP](../architecture/mcp-integration.md)
- [Configuration alertes](../../config/alert-thresholds.json)
- [Serveur MCP Yahoo Finance](/Users/yousrimaazaoui/Documents/projets/test-debile/yahoo-finance-mcp)
- [Code indicateurs techniques](../../scripts/calculators/) (optionnel, calculs dans le prompt)

## Références

- [RSI Indicator](https://www.investopedia.com/terms/r/rsi.asp)
- [MACD Indicator](https://www.investopedia.com/terms/m/macd.asp)
- [Moving Averages](https://www.investopedia.com/terms/m/movingaverage.asp)
- [Technical Analysis](https://www.investopedia.com/technical-analysis-4689657)
