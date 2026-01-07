# Intégration MCP Yahoo Finance (yousmaaza)

## Vue d'ensemble

Le projet utilise le serveur MCP Yahoo Finance développé par yousmaaza pour récupérer les données boursières en temps réel.

**Repository** : https://github.com/yousmaaza/yahoo-finance-mcp

## Fonctionnalités du serveur

Le serveur MCP Yahoo Finance fournit les outils suivants pour récupérer des données boursières :

### Outils disponibles

Basé sur le repository, le serveur expose typiquement ces fonctionnalités :

1. **Récupération de prix en temps réel**
   - Prix actuel
   - Variation du jour
   - Volume

2. **Historique des cours**
   - Prix de clôture historiques
   - Volumes historiques
   - Dates associées

3. **Informations sur le titre**
   - Nom de l'entreprise
   - Secteur
   - Capitalisation boursière
   - Ratios financiers (PE, etc.)

4. **Données de marché**
   - Prix d'ouverture/fermeture
   - Plus haut/plus bas du jour
   - Plus haut/plus bas sur 52 semaines

## Installation

### Prérequis
- Node.js 18+ installé
- npm ou npx disponible

### Étape 1 : Installer le package

```bash
# Installation globale (recommandé)
npm install -g yahoo-finance-mcp

# Ou via npx (pas d'installation nécessaire)
# Le serveur sera téléchargé à la première utilisation
```

### Étape 2 : Vérifier l'installation

```bash
# Tester que le serveur est accessible
npx yahoo-finance-mcp --version

# Ou si installé globalement
yahoo-finance-mcp --version
```

### Étape 3 : Configuration

Le serveur est déjà configuré dans `mcp/config.json` :

```json
{
  "mcpServers": {
    "yahoo-finance": {
      "command": "npx",
      "args": ["-y", "yahoo-finance-mcp"],
      "env": {}
    }
  }
}
```

**Note** : Aucune clé API n'est nécessaire car Yahoo Finance API est gratuite pour un usage standard.

## Utilisation dans les agents

### Agent Market Watcher

L'agent Market Watcher utilise le serveur MCP Yahoo Finance pour :

1. **Récupérer les données en temps réel** pour chaque ticker de la watchlist
2. **Obtenir l'historique** pour calculer les indicateurs techniques (RSI, MACD, MM)
3. **Analyser les volumes** pour détecter les anomalies

#### Exemple d'utilisation dans le prompt

```markdown
## Ta mission : Market Watcher

Tu dois surveiller les marchés et générer des alertes.

### Étape 1 : Lire la watchlist
Utilise l'outil MCP Google Drive pour lire la watchlist :
- `mcp__googledrive__find_file("watchlist.csv")`
- `mcp__googledrive__download_file(file_id)`

### Étape 2 : Pour chaque ticker, récupérer les données Yahoo Finance

Utilise les outils MCP Yahoo Finance disponibles. Par exemple :
- `mcp__yahoo_finance__get_quote(ticker)` - Prix et données du jour
- `mcp__yahoo_finance__get_historical_data(ticker, period)` - Historique
- `mcp__yahoo_finance__get_info(ticker)` - Infos sur l'entreprise

**Exemple pour LVMH (MC.PA)** :
1. Récupère le prix actuel : `mcp__yahoo_finance__get_quote("MC.PA")`
2. Récupère 200 jours d'historique : `mcp__yahoo_finance__get_historical_data("MC.PA", "200d")`
3. Récupère les infos : `mcp__yahoo_finance__get_info("MC.PA")`

### Étape 3 : Calculer les indicateurs techniques

Avec les données historiques, calcule :
- RSI sur 14 périodes
- MACD (12, 26, 9)
- Moyennes mobiles (20, 50, 200 jours)
- Analyse du volume

### Étape 4 : Générer et scorer les signaux

...
```

### Agent Portfolio Advisor

L'agent Portfolio Advisor utilise le serveur pour :

1. **Obtenir les prix actuels** des positions du portefeuille
2. **Récupérer les données des indices** (CAC40, Euro Stoxx) pour benchmarking
3. **Analyser la performance** en comparant aux indices

## Outils MCP Yahoo Finance - Référence

### Structure des outils

Les outils MCP sont généralement nommés selon ce pattern :
```
mcp__yahoo_finance__<action>
```

### Outils probables (à vérifier dans la documentation du package)

#### 1. `mcp__yahoo_finance__get_quote`

Récupère le prix et données actuelles d'un ticker.

**Paramètres** :
```typescript
{
  ticker: string  // Ex: "MC.PA", "SAP.DE"
}
```

**Retour** :
```json
{
  "ticker": "MC.PA",
  "price": 750.50,
  "change": -17.30,
  "changePercent": -2.25,
  "volume": 1250000,
  "open": 768.00,
  "high": 770.00,
  "low": 748.00,
  "previousClose": 767.80
}
```

#### 2. `mcp__yahoo_finance__get_historical_data`

Récupère l'historique des cours.

**Paramètres** :
```typescript
{
  ticker: string,      // Ex: "MC.PA"
  period: string,      // "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"
  interval: string     // "1d", "1wk", "1mo"
}
```

**Retour** :
```json
{
  "ticker": "MC.PA",
  "history": [
    {
      "date": "2024-12-01",
      "open": 760.00,
      "high": 765.00,
      "low": 755.00,
      "close": 762.50,
      "volume": 980000
    },
    // ...
  ]
}
```

#### 3. `mcp__yahoo_finance__get_info`

Récupère les informations détaillées sur un titre.

**Paramètres** :
```typescript
{
  ticker: string  // Ex: "MC.PA"
}
```

**Retour** :
```json
{
  "ticker": "MC.PA",
  "name": "LVMH Moët Hennessy Louis Vuitton SE",
  "sector": "Consumer Cyclical",
  "industry": "Luxury Goods",
  "marketCap": 375000000000,
  "currency": "EUR",
  "exchange": "EPA",
  "peRatio": 24.5,
  "dividendYield": 1.8,
  "fiftyTwoWeekHigh": 850.00,
  "fiftyTwoWeekLow": 650.00
}
```

## Mapping des tickers pour le PEA

### Format des tickers Yahoo Finance

Pour les marchés européens éligibles PEA :

| Marché | Suffixe | Exemple |
|--------|---------|---------|
| Euronext Paris | .PA | MC.PA (LVMH) |
| Xetra (Allemagne) | .DE | SAP.DE (SAP) |
| Borsa Italiana | .MI | RACE.MI (Ferrari) |
| BME (Espagne) | .MC | ITX.MC (Inditex) |
| Euronext Amsterdam | .AS | ASML.AS (ASML) |
| Euronext Brussels | .BR | ABI.BR (AB InBev) |
| Euronext Lisbon | .LS | EDP.LS (EDP) |

### Exemples de tickers

**France (Euronext Paris)** :
- LVMH : `MC.PA`
- Sanofi : `SAN.PA`
- TotalEnergies : `TTE.PA`
- L'Oréal : `OR.PA`

**Allemagne (Xetra)** :
- SAP : `SAP.DE`
- Siemens : `SIE.DE`
- Volkswagen : `VOW3.DE`
- Allianz : `ALV.DE`

**Pays-Bas** :
- ASML : `ASML.AS`
- Shell : `SHEL.AS`

**Indices** :
- CAC 40 : `^FCHI`
- DAX : `^GDAXI`
- Euro Stoxx 50 : `^STOXX50E`

## Calcul des indicateurs techniques

Les indicateurs sont calculés côté agent Claude à partir des données historiques.

### RSI (Relative Strength Index)

```javascript
// Pseudo-code pour l'agent
function calculateRSI(prices, period = 14) {
  // Calculer les gains et pertes
  let gains = [];
  let losses = [];

  for (let i = 1; i < prices.length; i++) {
    const change = prices[i] - prices[i-1];
    gains.push(change > 0 ? change : 0);
    losses.push(change < 0 ? -change : 0);
  }

  // Moyennes
  const avgGain = gains.slice(0, period).reduce((a,b) => a+b) / period;
  const avgLoss = losses.slice(0, period).reduce((a,b) => a+b) / period;

  // RSI
  const rs = avgGain / avgLoss;
  const rsi = 100 - (100 / (1 + rs));

  return rsi;
}
```

### MACD

```javascript
// Pseudo-code
function calculateMACD(prices) {
  const ema12 = calculateEMA(prices, 12);
  const ema26 = calculateEMA(prices, 26);

  const macd = ema12 - ema26;
  const signal = calculateEMA([macd], 9);
  const histogram = macd - signal;

  return { macd, signal, histogram };
}
```

### Moyennes Mobiles

```javascript
// Pseudo-code
function calculateMA(prices, period) {
  const slice = prices.slice(-period);
  return slice.reduce((a,b) => a+b) / period;
}

const ma20 = calculateMA(prices, 20);
const ma50 = calculateMA(prices, 50);
const ma200 = calculateMA(prices, 200);
```

## Test du serveur MCP

### Script de test manuel

Créer un fichier `mcp/examples/test-yahoo-finance.js` :

```javascript
// Test du serveur MCP Yahoo Finance

async function testYahooFinance() {
  console.log("🧪 Test du serveur MCP Yahoo Finance\n");

  // Tickers à tester
  const tickers = ["MC.PA", "SAP.DE", "ASML.AS"];

  for (const ticker of tickers) {
    console.log(`\n📊 Test pour ${ticker}:`);
    console.log("─".repeat(50));

    // Note: L'implémentation exacte dépend du package
    // Adapter selon la documentation de yahoo-finance-mcp

    try {
      // Exemple d'appel (à adapter)
      const quote = await yahooFinance.getQuote(ticker);
      console.log(`Prix: ${quote.price} €`);
      console.log(`Variation: ${quote.changePercent}%`);
      console.log(`Volume: ${quote.volume}`);

      const history = await yahooFinance.getHistory(ticker, "1mo");
      console.log(`Historique: ${history.length} jours`);

      console.log("✅ Test réussi");
    } catch (error) {
      console.error(`❌ Erreur: ${error.message}`);
    }
  }
}

testYahooFinance();
```

### Test via ligne de commande

```bash
# Tester l'accès au serveur
npx yahoo-finance-mcp --help

# Ou si le package fournit une CLI de test
npx yahoo-finance-mcp test MC.PA
```

## Gestion des erreurs

### Erreurs courantes

#### 1. Ticker invalide

```json
{
  "error": "Invalid ticker symbol",
  "ticker": "INVALID"
}
```

**Solution** : Vérifier le format du ticker (suffixe correct)

#### 2. Marché fermé

Les données peuvent être retardées si le marché est fermé.

**Solution** : L'agent doit gérer les données du jour précédent

#### 3. Rate limiting

Yahoo Finance peut limiter le nombre de requêtes.

**Solution** :
- Implémenter un cache
- Limiter à 1 requête par ticker par exécution
- Espacer les requêtes

### Gestion dans les prompts

```markdown
## Gestion des erreurs

Si un outil MCP Yahoo Finance échoue :
1. Logger l'erreur
2. Passer au ticker suivant
3. Ne pas bloquer l'analyse complète
4. Mentionner dans le rapport les tickers non analysables
```

## Performance et optimisation

### Caching

Pour réduire les appels API :

```markdown
## Stratégie de caching

1. **Données intraday** : Cache de 5 minutes
   - Prix, volume actuel

2. **Données historiques** : Cache de 24 heures
   - Historique des 200 derniers jours
   - Les données passées ne changent pas

3. **Informations entreprise** : Cache de 7 jours
   - Secteur, industrie, etc.
```

### Optimisation des requêtes

```markdown
## Bonnes pratiques

1. **Batch les requêtes** :
   - Traiter tous les tickers en parallèle si possible

2. **Limiter l'historique** :
   - Ne récupérer que les données nécessaires
   - Pour RSI(14) : 30 jours suffisent
   - Pour MA(200) : 250 jours minimum

3. **Réutiliser les données** :
   - Une seule requête historique pour tous les indicateurs
```

## Monitoring

### Logs à suivre

```bash
# Dans les logs de l'agent
[2026-01-07 08:00:15] 📊 Récupération données MC.PA...
[2026-01-07 08:00:16] ✅ MC.PA: Prix=750.50€ Volume=1.2M
[2026-01-07 08:00:17] 📊 Récupération données SAP.DE...
[2026-01-07 08:00:18] ✅ SAP.DE: Prix=185.30€ Volume=3.5M
```

### Métriques

- Temps de réponse par ticker : < 2 secondes
- Taux de succès : > 95%
- Nombre de requêtes par exécution : ~20-50

## Ressources

### Documentation
- [Repository Yahoo Finance MCP](https://github.com/yousmaaza/yahoo-finance-mcp)
- [Yahoo Finance API](https://finance.yahoo.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

### Support
- Issues GitHub : https://github.com/yousmaaza/yahoo-finance-mcp/issues
- Documentation MCP : https://modelcontextprotocol.io/docs

---

**Version** : 1.0
**Dernière mise à jour** : 2026-01-07
**Package** : yahoo-finance-mcp (yousmaaza)
