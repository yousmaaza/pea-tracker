# Exemple Concret : Exécution de l'agent Market Watcher

## 📖 Scénario : Analyse quotidienne à 8h

Vous exécutez :
```bash
claude-code agent run market-watcher-pea
```

---

## 🎬 Ce qui se passe en coulisses

### 1️⃣ Claude lit le fichier `.claude/agents/market-watcher-pea.md`

```
Claude voit le markdown avec les instructions :
- "Récupère la watchlist depuis Google Drive"
- "Calcule RSI, MACD, MA pour chaque ticker"
- "Génère des signaux d'achat/vente"
- "Envoie des emails si score ≥ 60"
```

### 2️⃣ Claude commence à exécuter le workflow

**STEP 1 : Récupération des données**

Claude utilise le tool `mcp__googledrive__find_file` :
```
Assistant: "Je vais récupérer le fichier Excel depuis Google Drive"
[Appelle le MCP tool]
[Télécharge PEA_Watchlist_Indicateurs.xlsx]
```

**STEP 2 : Parsing de l'Excel**

Claude voit dans le markdown qu'il doit parser l'Excel avec pandas.

**Option A : Code inline (l'agent génère le code)**
```
Assistant: "Je vais créer un script pour parser l'Excel"

[Claude utilise le tool Write pour créer un fichier Python temporaire]
```

**Le fichier créé par Claude :**
```python
# /tmp/parse_watchlist_20260108.py
import pandas as pd
import sys

excel_file = sys.argv[1]

# Parse watchlist
df_watchlist = pd.read_excel(excel_file, sheet_name='Watchlist')
active_tickers = df_watchlist[df_watchlist['Actif'] == True]

print("ACTIVE_TICKERS:")
for _, row in active_tickers.iterrows():
    print(f"{row['Ticker']}|{row['Nom']}|{row['Secteur']}")
```

**Claude exécute ce script :**
```bash
Bash tool: python /tmp/parse_watchlist_20260108.py /tmp/downloaded_excel.xlsx
```

**Résultat :**
```
ACTIVE_TICKERS:
MC.PA|LVMH|Luxe
OR.PA|L'Oréal|Beauté
BNP.PA|BNP Paribas|Banque
```

**Option B : Import de module (recommandé)**

```python
# /tmp/parse_watchlist_20260108.py
import sys
sys.path.append('/home/user/pea-tracker')

from src.data.excel_parser import parse_watchlist_file

excel_file = sys.argv[1]
active_tickers = parse_watchlist_file(excel_file)

for ticker in active_tickers:
    print(f"{ticker['symbol']}|{ticker['name']}|{ticker['sector']}")
```

**Ici, Claude utilise VOTRE module Python existant !**

### 3️⃣ Collecte des données de marché

Claude appelle Yahoo Finance MCP pour chaque ticker :

```
Assistant: "Je vais récupérer les données pour MC.PA"

[Appelle mcp__yfinance__get_historical_stock_prices]
[Reçoit 250 jours de prix]
```

### 4️⃣ Calcul des indicateurs techniques

**Claude voit dans le markdown qu'il doit calculer RSI, MACD, etc.**

**Option A : Code inline**

Claude génère et exécute :
```python
# /tmp/calculate_indicators_20260108.py
import numpy as np
import json

def calculate_rsi(prices, periods=14):
    deltas = np.diff(prices)
    gain = np.where(deltas > 0, deltas, 0)
    loss = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gain[-periods:])
    avg_loss = np.mean(loss[-periods:])
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# Prix de MC.PA récupérés via Yahoo Finance
prices = [750.2, 755.8, 748.1, 760.5, 758.3, 762.0, 765.4, 770.2, 768.7, 775.1]

rsi = calculate_rsi(np.array(prices))
print(json.dumps({"ticker": "MC.PA", "rsi": rsi}))
```

**Option B : Import de module (recommandé)**

```python
# /tmp/calculate_indicators_20260108.py
import sys
sys.path.append('/home/user/pea-tracker')

from src.analysis.indicators import calculate_rsi, calculate_macd, calculate_ma
import json

# Prix de MC.PA récupérés via Yahoo Finance
prices = [750.2, 755.8, 748.1, 760.5, 758.3, 762.0, 765.4, 770.2, 768.7, 775.1]

result = {
    "ticker": "MC.PA",
    "rsi": calculate_rsi(prices),
    "macd": calculate_macd(prices),
    "ma20": calculate_ma(prices, 20),
    "ma50": calculate_ma(prices, 50),
    "ma200": calculate_ma(prices, 200)
}

print(json.dumps(result))
```

**Claude exécute :**
```bash
python /tmp/calculate_indicators_20260108.py
```

**Résultat :**
```json
{
  "ticker": "MC.PA",
  "rsi": 32.5,
  "macd": {"line": -1.5, "signal": -0.8, "histogram": -0.7},
  "ma20": 760.0,
  "ma50": 770.0,
  "ma200": 720.0
}
```

**Claude parse ce JSON et continue !**

### 5️⃣ Génération de signal

Claude applique la logique de décision :
```
RSI = 32.5 (< 30 = oversold) → +30 points
MACD histogram négatif → +0 points
Prix > MA200 → +20 points
Volume ratio > 1.3 → +15 points

Score total = 65 → Signal BUY avec confiance 65%
```

### 6️⃣ Création du rapport Markdown

Claude génère un rapport :

```markdown
# 🟢 Signal d'achat : LVMH (MC.PA)

**Date** : 2026-01-08 08:30
**Score de confiance** : 65/100

## Résumé

LVMH présente un signal d'achat avec un RSI en zone de survente (32.5) et un support solide sur la MA200 à €720.

## Indicateurs techniques

- **RSI(14)** : 32.5 (oversold)
- **MACD** : -1.5 (bearish mais histogram en amélioration)
- **Prix actuel** : €775.10
- **MA20** : €760 (résistance court terme)
- **MA200** : €720 (support long terme)

## Action recommandée

Considérer une position d'achat entre €770-€775.
Stop-loss suggéré : €710 (-8.4%)
Target court terme : €810 (+4.5%)
```

### 7️⃣ Sauvegarde dans Google Drive

```
Claude utilise : mcp__googledrive__create_file_from_text()
Fichier créé : PEA-Tracker/Reports/signals/signal_MC.PA_20260108_0830.md
```

### 8️⃣ Envoi de l'email

```
Claude utilise : mcp__gmail__send_email()
Sujet : [PEA Tracker] 🟢 Signal d'achat sur LVMH (Score: 65)
Corps : [Contenu HTML formaté]
```

---

## 🎯 Résumé : NON, vous n'intégrez pas les scripts dans le markdown

### ❌ CE QUE VOUS NE FAITES PAS

```markdown
# MAUVAIS EXEMPLE - Ne pas faire ça

Dans .claude/agents/market-watcher-pea.md :

```python
# Tout le code de market_watcher_analysis.py copié ici (400 lignes)
import pandas as pd
import numpy as np
...
def calculate_rsi(...):
    ...
def calculate_macd(...):
    ...
...
```
```

**Pourquoi ?**
- ❌ Markdown illisible (400+ lignes de code)
- ❌ Code non testable
- ❌ Duplication si plusieurs agents
- ❌ Mélange instructions et implémentation

### ✅ CE QUE VOUS FAITES

**Dans le markdown de l'agent (instructions seulement) :**

```markdown
# BON EXEMPLE

Dans .claude/agents/market-watcher-pea.md :

## STEP 3: Calculate Technical Indicators

Use the technical analysis module to calculate indicators.

**Execute this workflow:**

```bash
python /home/user/pea-tracker/scripts/run_analysis.py \
    --tickers MC.PA,OR.PA,BNP.PA \
    --output /tmp/signals.json
```

The script will use `src.analysis.indicators` module to calculate:
- RSI (14 periods)
- MACD (12, 26, 9)
- Moving averages (20, 50, 200)

Parse the JSON output and proceed to signal generation.
```

**Code Python dans des fichiers séparés :**

```python
# src/analysis/indicators.py
def calculate_rsi(prices, periods=14):
    """Calculate RSI"""
    # Implementation...

# src/analysis/signals.py
def generate_signal(rsi, macd, ma20, volume_ratio):
    """Generate buy/sell signal"""
    # Implementation...

# scripts/run_analysis.py
from src.analysis.indicators import calculate_rsi
from src.analysis.signals import generate_signal

# Main workflow...
```

---

## 🔑 Points clés

| Aspect | Où ça va |
|--------|----------|
| **Instructions** | `.claude/agents/market-watcher-pea.md` |
| **Code réutilisable** | `src/analysis/*.py` |
| **Scripts d'orchestration** | `scripts/*.py` |
| **Code temporaire généré** | Créé à la volée par Claude dans `/tmp/` |

**L'agent markdown** = Le chef d'orchestre (dit quoi faire)
**Les modules Python** = Les musiciens (font le travail)
**Claude** = Le chef qui coordonne tout

---

## 💡 Analogie

**Mauvaise approche :**
```
Recette de cuisine (markdown) :
1. Prendre des œufs
2. [Copie/colle de 400 lignes de code Python pour calculer la cuisson]
3. Servir
```

**Bonne approche :**
```
Recette de cuisine (markdown) :
1. Prendre des œufs
2. Utiliser la fonction `cuire_oeufs()` du module cuisine.py avec température=180°C
3. Servir
```

---

Voulez-vous que je **refactorise maintenant** vos scripts existants pour cette architecture ?
