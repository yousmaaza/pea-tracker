# Comment les Agents Claude utilisent Python

## Vue d'ensemble

Un agent Claude (fichier `.md` dans `.claude/agents/`) **N'EST PAS** un script Python. C'est un **prompt intelligent** qui **instruit Claude** sur comment accomplir une tâche.

**Claude peut alors :**
- ✅ Écrire du code Python à la volée
- ✅ Exécuter ce code via l'outil `Bash`
- ✅ Importer et utiliser des modules Python existants
- ✅ Lire/écrire des fichiers, appeler des APIs, etc.

---

## 🎯 Approche 1 : Code Python inline (généré par l'agent)

**Principe** : L'agent génère le code Python directement et l'exécute

### Exemple dans le markdown de l'agent

```markdown
# Dans .claude/agents/market-watcher-pea.md

## STEP 3: Calculate Technical Indicators

For each ticker, calculate RSI using this Python code:

```python
import numpy as np

def calculate_rsi(prices, periods=14):
    """Calculate RSI indicator"""
    deltas = np.diff(prices)
    gain = np.where(deltas > 0, deltas, 0)
    loss = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gain[-periods:])
    avg_loss = np.mean(loss[-periods:])
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# Example usage
prices = [100, 102, 101, 105, 107, 103, 108]
rsi = calculate_rsi(np.array(prices))
print(f"RSI: {rsi:.2f}")
```

Execute this calculation for each ticker and store the results.
```

**Ce qui se passe quand l'agent s'exécute :**
1. Claude lit ces instructions
2. Claude **génère un fichier Python temporaire** avec ce code (ou l'exécute directement)
3. Claude utilise `Bash` tool pour exécuter : `python script.py`
4. Claude récupère les résultats

**✅ Avantages :**
- Tout est dans le markdown (documentation = code)
- Pas besoin de maintenir des fichiers séparés
- L'agent est autonome

**❌ Inconvénients :**
- Code dupliqué si plusieurs agents font la même chose
- Difficile à tester indépendamment
- Pas de réutilisation

---

## 🎯 Approche 2 : Import de modules existants (recommandé)

**Principe** : L'agent importe et utilise des modules Python prédéfinis

### Structure du projet

```
pea-tracker/
├── .claude/agents/
│   └── market-watcher-pea.md
├── src/
│   └── analysis/
│       ├── __init__.py
│       ├── indicators.py      # ← Vos fonctions de calcul
│       └── signals.py         # ← Logique de signaux
└── requirements.txt
```

### Fichier `src/analysis/indicators.py`

```python
"""Technical indicators calculation module"""
import numpy as np

def calculate_rsi(prices, periods=14):
    """Calculate RSI indicator"""
    if len(prices) < periods + 1:
        return None
    deltas = np.diff(prices)
    gain = np.where(deltas > 0, deltas, 0)
    loss = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gain[-periods:])
    avg_loss = np.mean(loss[-periods:])
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD indicator"""
    # Implementation...
    pass
```

### Dans le markdown de l'agent

```markdown
# Dans .claude/agents/market-watcher-pea.md

## SETUP

Before starting, ensure Python environment is ready:

1. Create virtual environment: `python3 -m venv .venv`
2. Activate: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Or use Claude Code's pip-mode: `/pip-mode standard`

## STEP 3: Calculate Technical Indicators

For each ticker, use the `src.analysis.indicators` module to calculate technical indicators.

**Example workflow:**

```python
import sys
sys.path.append('/home/user/pea-tracker')  # Adjust path as needed

from src.analysis.indicators import calculate_rsi, calculate_macd
import numpy as np

# Assume we have price data from Yahoo Finance MCP
prices = np.array([100, 102, 101, 105, 107, 103, 108, 110, 109, 112, 115, 113, 116, 118, 120])

# Calculate indicators
rsi = calculate_rsi(prices, periods=14)
macd_line, macd_signal, histogram = calculate_macd(prices)

print(f"RSI: {rsi:.2f}")
print(f"MACD: {macd_line:.2f}")
```

**Instructions for you (the agent):**
1. Write a Python script that imports these modules
2. Use the Bash tool to execute the script
3. Parse the output to extract indicator values
4. Continue with signal generation logic
```

**Ce qui se passe :**
1. Claude lit les instructions
2. Claude **crée un script Python** qui importe `src.analysis.indicators`
3. Claude exécute le script via `Bash`
4. Claude continue avec les étapes suivantes

**✅ Avantages :**
- Code Python testable indépendamment
- Réutilisable par plusieurs agents
- Séparation des responsabilités (calculs vs orchestration)
- Maintenable et évolutif

**❌ Inconvénients :**
- Nécessite une structure de projet plus complexe
- Dépendances à gérer (requirements.txt)

---

## 🎯 Approche 3 : Orchestration hybride (le meilleur des deux)

**Principe** : Combiner modules Python robustes + code inline flexible

### Exemple concret

```markdown
# Dans .claude/agents/market-watcher-pea.md

## STEP 3: Calculate Technical Indicators

Use the `src.analysis` module for core calculations, but add custom logic as needed.

**Core calculation workflow:**

```python
#!/usr/bin/env python3
import sys
sys.path.append('/home/user/pea-tracker')

from src.analysis.indicators import calculate_rsi, calculate_macd, calculate_ma
from src.analysis.signals import generate_buy_sell_signal
import json

# This will be populated with data from Yahoo Finance MCP
tickers_data = {
    "MC.PA": {
        "prices": [750, 755, 748, 760, 758, 762, 765, 770, 768, 775],
        "volumes": [1000000, 1200000, 950000, 1100000, 1050000, 1300000, 1250000, 1400000, 1350000, 1500000]
    }
}

results = []

for ticker, data in tickers_data.items():
    prices = data["prices"]
    volumes = data["volumes"]

    # Use module functions
    rsi = calculate_rsi(prices)
    macd_line, macd_signal, histogram = calculate_macd(prices)
    ma20 = calculate_ma(prices, 20)
    ma50 = calculate_ma(prices, 50)

    # Custom inline logic for volume analysis
    avg_volume = sum(volumes[-20:]) / 20
    volume_ratio = volumes[-1] / avg_volume

    # Generate signal using module
    signal = generate_buy_sell_signal(
        rsi=rsi,
        macd_histogram=histogram,
        price=prices[-1],
        ma20=ma20,
        volume_ratio=volume_ratio
    )

    results.append({
        "ticker": ticker,
        "rsi": rsi,
        "signal": signal
    })

# Output as JSON for easy parsing
print(json.dumps(results, indent=2))
```

**As the agent, you will:**
1. Fetch data from Yahoo Finance MCP
2. Format the data into the `tickers_data` structure
3. Create and execute this Python script
4. Parse the JSON output
5. Continue with report generation
```

---

## 🚀 Exécution réelle par l'agent

Voici ce qui se passe **concrètement** quand l'agent s'exécute :

### 1. L'agent est invoqué

```bash
claude-code agent run market-watcher-pea
```

### 2. Claude lit le markdown de l'agent

Claude comprend qu'il doit :
- Récupérer des données via MCP
- Calculer des indicateurs (avec du Python)
- Générer des rapports

### 3. Claude crée un script Python temporaire

```python
# /tmp/market_analysis_20260108_1430.py
import sys
sys.path.append('/home/user/pea-tracker')
from src.analysis.indicators import calculate_rsi

prices = [100, 102, 101, 105, 107]
rsi = calculate_rsi(prices)
print(f"RSI:{rsi:.2f}")
```

### 4. Claude exécute le script

Via le tool `Bash` :
```bash
python /tmp/market_analysis_20260108_1430.py
```

### 5. Claude récupère le résultat

```
RSI:45.23
```

### 6. Claude continue le workflow

- Parse le résultat
- Génère un signal d'achat/vente
- Crée un rapport Markdown
- Upload vers Google Drive
- Envoie un email

---

## 📋 Recommandation pour votre projet

**Pour market-watcher-pea, utilisez l'Approche 2 (modules importés) :**

### Structure proposée

```
pea-tracker/
├── .claude/
│   └── agents/
│       └── market-watcher-pea.md       # Orchestration
│
├── src/
│   ├── __init__.py
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── indicators.py               # RSI, MACD, MA
│   │   ├── signals.py                  # Logique de signaux
│   │   └── scoring.py                  # Calcul de confiance
│   │
│   └── data/
│       ├── __init__.py
│       ├── excel_parser.py             # Parse Excel
│       └── yahoo_client.py             # Wrapper Yahoo Finance
│
├── scripts/
│   └── run_analysis.py                 # Script principal appelé par l'agent
│
└── requirements.txt
```

### Dans l'agent markdown

```markdown
## STEP 3: Calculate Indicators and Generate Signals

Execute the main analysis script:

```bash
python /home/user/pea-tracker/scripts/run_analysis.py \
    --watchlist-file "$WATCHLIST_PATH" \
    --output-json /tmp/signals.json
```

This script will:
1. Import modules from `src.analysis`
2. Calculate all technical indicators
3. Generate buy/sell signals
4. Output results as JSON

Parse the JSON output and continue with report generation.
```

---

## 🎯 Résumé

| Approche | Quand l'utiliser | Complexité |
|----------|------------------|------------|
| **Inline** | Logique simple, one-off, pas de réutilisation | ⭐ Faible |
| **Modules importés** | Logique complexe, réutilisable, testable | ⭐⭐ Moyenne |
| **Hybride** | Mix des deux selon les besoins | ⭐⭐⭐ Élevée |

**Pour PEA Tracker : utilisez des modules importés** ✅

---

## Questions fréquentes

### Q: L'agent doit-il contenir le code Python complet ?

**Non.** L'agent contient des **instructions et exemples** de comment utiliser le code Python. Le code réel est dans `src/`.

### Q: Comment l'agent sait où trouver les modules ?

Vous lui indiquez dans le markdown :
```markdown
Ensure Python path includes the project root:
```python
import sys
sys.path.append('/home/user/pea-tracker')
from src.analysis.indicators import calculate_rsi
```
```

### Q: Faut-il `/pip-mode standard` ?

Oui, si vous utilisez des dépendances externes (pandas, numpy). Cela crée un environnement virtuel automatiquement.

### Q: L'agent peut-il modifier les fichiers Python ?

Oui ! L'agent a accès aux tools `Edit` et `Write`. Il peut améliorer le code si nécessaire.

---

## Prochaines étapes

Voulez-vous que je :
1. **Refactorise vos scripts existants** en modules `src/analysis/` ?
2. **Mette à jour l'agent markdown** pour utiliser ces modules ?
3. **Crée un script principal** `run_analysis.py` ?
