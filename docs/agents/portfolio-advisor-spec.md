# Spécifications Agent Portfolio Advisor

## Vue d'ensemble

L'Agent Portfolio Advisor est responsable de l'analyse mensuelle complète du portefeuille PEA, du suivi de performance et des recommandations stratégiques d'optimisation.

## Objectifs

1. **Analyser** la performance globale et par ligne du portefeuille
2. **Évaluer** l'allocation sectorielle et géographique
3. **Mesurer** le niveau de diversification et les risques
4. **Recommander** des ajustements stratégiques personnalisés
5. **Rapporter** mensuellement avec des insights actionnables

## Responsabilités détaillées

### 1. Calcul de performance

#### Métriques de performance

**Performance absolue**
```javascript
// Performance globale
total_return = (current_value - initial_investment) / initial_investment * 100

// Performance mensuelle (MTD)
mtd_return = (current_value - start_month_value) / start_month_value * 100

// Performance annuelle (YTD)
ytd_return = (current_value - start_year_value) / start_year_value * 100

// Performance depuis création
inception_return = (current_value - first_investment) / first_investment * 100
```

**Performance par ligne**
```javascript
// P&L par position
position_pnl = (current_price - avg_buy_price) * quantity
position_pnl_pct = (current_price - avg_buy_price) / avg_buy_price * 100

// Contribution à la performance
contribution = position_pnl / total_portfolio_value * 100
```

**Performance ajustée du risque**
```javascript
// Sharpe Ratio (si données suffisantes)
sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility

// Maximum Drawdown
max_drawdown = (trough_value - peak_value) / peak_value * 100
```

#### Benchmarking

Comparaison aux indices :
- **CAC 40** : Référence actions françaises
- **Euro Stoxx 50** : Référence actions européennes
- **MSCI Europe** : Référence large cap Europe

Sources de données :
- Yahoo Finance pour indices
- Calcul de la surperformance/sous-performance

### 2. Analyse d'allocation

#### Allocation sectorielle

**Calcul des poids**
```javascript
// Poids par secteur
sector_weight = sector_value / total_invested * 100

// Concentration sectorielle (Herfindahl Index)
herfindahl_sector = sum(sector_weight^2)
// Interprétation:
// < 1500: Bien diversifié
// 1500-2500: Concentration modérée
// > 2500: Forte concentration
```

**Secteurs standards** :
- Technologie
- Santé
- Finance
- Industrie
- Consommation cyclique
- Consommation défensive
- Énergie
- Matériaux
- Services publics
- Immobilier
- Luxe
- Télécommunications

**Alertes de concentration** :
- ⚠️ Un secteur > 40% du portefeuille
- ⚠️ Herfindahl > 2500
- ✅ Recommandation : 4-6 secteurs minimum

#### Allocation géographique

**Calcul des poids par pays**
```javascript
country_weight = country_value / total_invested * 100
```

**Pays éligibles PEA** :
- France
- Allemagne
- Italie
- Espagne
- Pays-Bas
- Belgique
- Portugal
- Autres UE

**Seuils recommandés** :
- France : 40-70% (biais domestique acceptable)
- 2-3 autres pays minimum
- Aucun pays hors France > 30%

#### Concentration du portefeuille

**Métriques clés**
```javascript
// Top N concentration
top3_weight = sum(top_3_positions_weights)
// Alerte si > 60%

// Nombre de lignes
num_positions = count(active_positions)
// Recommandation : 5-8 lignes minimum

// Effective Number of Stocks (ENS)
ens = 1 / sum(weight^2)
// Plus ENS est élevé, meilleure est la diversification
```

**Niveaux de diversification** :
- Excellente : 8+ lignes, ENS > 6, Top3 < 50%
- Bonne : 5-7 lignes, ENS 4-6, Top3 50-60%
- Moyenne : 3-4 lignes, ENS 2-4, Top3 60-75%
- Faible : < 3 lignes, ENS < 2, Top3 > 75%

### 3. Analyse des transactions

#### Métriques de trading

**Activité**
```javascript
// Nombre de transactions
monthly_trades = count(transactions_in_month)
trade_frequency = total_trades / months_since_inception

// Répartition achats/ventes
buy_ratio = buy_count / total_trades * 100
sell_ratio = sell_count / total_trades * 100
```

**Qualité des décisions**
```javascript
// Taux de réussite des achats
successful_buys = count(buys with pnl > 0) / total_buys * 100

// Prix moyen d'achat vs prix actuel
avg_discount = (current_price - avg_buy_price) / current_price * 100
```

**Timing**
- Meilleurs/pires achats du mois
- Opportunités manquées (signaux non suivis)
- Timing des ventes (trop tôt/tard)

### 4. Recommandations stratégiques

#### Framework de recommandations

**1. Réduction de concentration**

Condition : Position > 30% du portefeuille
```
Recommandation:
- Réduire progressivement à 25-30% maximum
- Vendre X actions sur Y mois
- Libérer Z€ pour diversification
```

**2. Diversification géographique**

Condition : 1-2 pays seulement
```
Recommandation:
- Ajouter 2-3 positions sur nouveaux marchés
- Suggestions de titres par pays
- Budget à allouer : X% du portefeuille
```

**3. Équilibrage sectoriel**

Condition : Secteur > 40% ou < 5%
```
Recommandation:
- Rééquilibrer vers allocation cible
- Secteurs à renforcer / alléger
- Titres suggérés par secteur
```

**4. Optimisation liquidité**

Condition : Cash < 3% ou > 15%
```
Recommandation:
- Si cash < 3% : Alléger positions pour liquidité
- Si cash > 15% : Déployer progressivement
- Objectif : 3-8% de liquidités
```

**5. Qualité du portefeuille**

Critères analysés :
- Solidité financière des entreprises
- Dividendes et rendement
- Perspectives de croissance
- Valorisation (PER, PEG, etc.)

#### Priorisation des recommandations

**Priorité 🔴 Urgente** :
- Concentration excessive (> 50% sur 1 position)
- Diversification très faible (< 3 lignes)
- Risque sectoriel majeur

**Priorité 🟡 Importante** :
- Allocation sous-optimale
- Liquidité inadaptée
- Opportunités de rééquilibrage

**Priorité 🟢 Optionnelle** :
- Optimisations marginales
- Suggestions d'amélioration long terme
- Opportunités tactiques

### 5. Génération du rapport mensuel

#### Structure du rapport

```markdown
# 📊 Rapport Mensuel PEA Tracker - [Mois Année]

## Executive Summary (3-5 lignes)
Synthèse des points clés du mois

## 📈 Performance Globale
- Valeur, rendements MTD/YTD/Total
- Comparaison indices
- Graphiques de performance

## 🎯 Allocation du Portefeuille
- Tables sectorielles/géographiques
- Niveau de concentration
- Métriques de diversification

## 💼 Positions Principales
- Top 5 positions détaillées
- Meilleurs/pires performers

## 📊 Activité du Mois
- Transactions effectuées
- Évolution des positions

## ⚠️ Points d'Attention
- Risques identifiés
- Alertes

## 💡 Recommandations
- Actions prioritaires
- Plan d'action trimestriel
- Suggestions de titres

## 🎯 Portefeuille Cible
- Allocation cible proposée
- Écart vs actuel

## 📅 Plan d'Action
- Roadmap 3 mois
- Étapes concrètes

## 📌 Suivi des Objectifs
- Objectifs utilisateur
- Progression

## 💬 Conclusion
- Synthèse et prochaines étapes

---
Disclaimer + Date génération
```

#### Format et design

**Email HTML** :
- Template responsive
- Tableaux clairs et lisibles
- Couleurs par thème :
  - Vert : Positif
  - Rouge : Négatif
  - Bleu : Neutre/Info
  - Jaune : Attention
- Emojis pour clarté visuelle

**Pièce jointe PDF** (optionnel V2) :
- Export formaté du rapport
- Graphiques de performance
- Sauvegarde dans Google Drive

## Architecture technique

### Workflow n8n

```
┌─────────────┐
│  Scheduler  │ Cron: 1er du mois à 9h
└──────┬──────┘
       │
       v
┌─────────────┐
│  Read       │ Google Sheets:
│  Portfolio  │ - Positions actuelles
│  Data       │ - Historique valorisation
└──────┬──────┘
       │
       v
┌─────────────┐
│  Read       │ Google Sheets:
│  Transactions│ - Transactions du mois
│  History    │
└──────┬──────┘
       │
       v
┌─────────────┐
│  Calculate  │ Function Node:
│  Performance│ - MTD, YTD, Total
│             │ - P&L par ligne
└──────┬──────┘
       │
       v
┌─────────────┐
│  Calculate  │ Function Node:
│  Allocation │ - Secteurs, pays
│             │ - Concentration
└──────┬──────┘
       │
       v
┌─────────────┐
│  Fetch      │ Yahoo Finance:
│  Benchmark  │ - CAC40, Euro Stoxx
│  Data       │
└──────┬──────┘
       │
       v
┌─────────────┐
│  Build      │ Function Node:
│  Claude     │ - Format JSON complet
│  Payload    │ - Inclure prompt
└──────┬──────┘
       │
       v
┌─────────────┐
│  Call       │ HTTP Request:
│  Claude API │ - Prompt portfolio-review
│             │ - Max tokens: 8000
└──────┬──────┘
       │
       v
┌─────────────┐
│  Parse      │ Function Node:
│  Report     │ - Extract Markdown
│             │ - Format HTML
└──────┬──────┘
       │
       v
┌─────────────┐
│  Send       │ Gmail:
│  Email      │ - Rapport formaté
│  Report     │ - HTML + CSS inline
└──────┬──────┘
       │
       v
┌─────────────┐
│  Save       │ Google Drive:
│  Report     │ - Dossier Rapports/
│             │ - Format .md ou .pdf
└──────┬──────┘
       │
       v
┌─────────────┐
│  Update     │ Google Sheets:
│  Report Log │ - Historique rapports
└─────────────┘
```

### Calculs JavaScript

**Performance mensuelle**
```javascript
function calculateMonthlyPerformance(portfolio, history) {
  const currentValue = portfolio.total_value;
  const startMonthValue = history.find(h => h.date === startOfMonth).value;

  const mtd = ((currentValue - startMonthValue) / startMonthValue) * 100;

  return {
    mtd: mtd.toFixed(2),
    start_value: startMonthValue,
    end_value: currentValue,
    absolute_change: (currentValue - startMonthValue).toFixed(2)
  };
}
```

**Allocation sectorielle**
```javascript
function calculateSectorAllocation(positions) {
  const sectorMap = {};
  const totalInvested = positions.reduce((sum, p) => sum + p.market_value, 0);

  positions.forEach(position => {
    const sector = position.sector;
    if (!sectorMap[sector]) {
      sectorMap[sector] = { value: 0, positions: [] };
    }
    sectorMap[sector].value += position.market_value;
    sectorMap[sector].positions.push(position);
  });

  // Calculer poids et trier
  const sectors = Object.entries(sectorMap).map(([name, data]) => ({
    name,
    value: data.value,
    weight: (data.value / totalInvested * 100).toFixed(2),
    count: data.positions.length
  })).sort((a, b) => b.value - a.value);

  // Calculer Herfindahl
  const herfindahl = sectors.reduce((sum, s) => sum + Math.pow(s.weight, 2), 0);

  return { sectors, herfindahl: herfindahl.toFixed(0) };
}
```

**Indice de diversification**
```javascript
function calculateDiversificationMetrics(positions) {
  const totalValue = positions.reduce((sum, p) => sum + p.market_value, 0);

  // Effective Number of Stocks
  const sumSquaredWeights = positions.reduce((sum, p) => {
    const weight = p.market_value / totalValue;
    return sum + Math.pow(weight, 2);
  }, 0);
  const ens = 1 / sumSquaredWeights;

  // Top 3 concentration
  const sorted = [...positions].sort((a, b) => b.market_value - a.market_value);
  const top3Value = sorted.slice(0, 3).reduce((sum, p) => sum + p.market_value, 0);
  const top3Weight = (top3Value / totalValue * 100).toFixed(2);

  // Niveau de diversification
  let level;
  if (positions.length >= 8 && ens > 6 && top3Weight < 50) level = 'Excellente';
  else if (positions.length >= 5 && ens >= 4 && top3Weight <= 60) level = 'Bonne';
  else if (positions.length >= 3 && ens >= 2 && top3Weight <= 75) level = 'Moyenne';
  else level = 'Faible';

  return {
    num_positions: positions.length,
    ens: ens.toFixed(2),
    top3_weight: top3Weight,
    level
  };
}
```

## Configuration

### Variables d'environnement

```bash
# Claude API
CLAUDE_API_KEY=sk-ant-xxxxx
CLAUDE_MODEL=claude-3-5-sonnet-20241022
CLAUDE_MAX_TOKENS=8000

# Google Sheets
SHEET_ID_PORTFOLIO=xxxxx
SHEET_ID_TRANSACTIONS=xxxxx
SHEET_ID_HISTORY=xxxxx
SHEET_ID_REPORTS_LOG=xxxxx

# Google Drive
DRIVE_FOLDER_REPORTS=xxxxx

# Notifications
EMAIL_TO=your-email@example.com
REPORT_DAY=1  # 1er du mois
```

### Format Portfolio (Google Sheets)

**Onglet "Positions"** :
| Ticker | Name | Quantity | Avg Buy Price | Current Price | Market Value | P&L | P&L % | Weight % | Sector | Country |
|--------|------|----------|---------------|---------------|--------------|-----|-------|----------|--------|---------|
| MC.PA | LVMH | 50 | 720 | 750 | 37500 | 1500 | 4.17 | 90.36 | Luxe | France |

**Onglet "History"** :
| Date | Total Value | Cash | Invested | Daily Change % | Notes |
|------|-------------|------|----------|----------------|-------|
| 2024-12-01 | 45000 | 3500 | 41500 | +0.5 | |

**Onglet "User Profile"** :
| Field | Value |
|-------|-------|
| Risk Tolerance | Moderate |
| Investment Horizon | Long Term |
| Objectives | Growth, Diversification |

## Tests et validation

### Checklist de validation

**Calculs** :
- [ ] Performance calculée correctement (MTD, YTD)
- [ ] Allocation sectorielle = 100%
- [ ] P&L par ligne exact
- [ ] Métriques de diversification cohérentes

**Rapport** :
- [ ] Toutes les sections présentes
- [ ] Données à jour
- [ ] Recommandations pertinentes
- [ ] Formatage HTML correct
- [ ] Liens et tableaux fonctionnels

**Intégration** :
- [ ] Email reçu
- [ ] Rapport sauvegardé dans Drive
- [ ] Log mis à jour
- [ ] Pas d'erreurs dans n8n

### Scénarios de test

1. **Portfolio simple** (2-3 lignes) :
   - Vérifier alertes de concentration
   - Recommandations de diversification

2. **Portfolio diversifié** (8+ lignes) :
   - Vérifier calculs d'allocation
   - Recommandations d'optimisation

3. **Portfolio avec pertes** :
   - Ton approprié dans le rapport
   - Suggestions constructives

4. **Premier rapport** :
   - Gestion absence d'historique
   - Métriques depuis inception

## Métriques de succès

| KPI | Cible | Mesure |
|-----|-------|--------|
| Taux de génération | 100% | Rapports envoyés / mois |
| Temps génération | < 2 min | Durée workflow |
| Pertinence recommandations | > 80% | Feedback utilisateur |
| Coût par rapport | < 0.20€ | Claude API tokens |
| Lisibilité | > 4/5 | Score utilisateur |

## Évolutions futures (V2)

1. **Graphiques visuels** : Charts de performance intégrés
2. **Rapport PDF** : Export professionnel
3. **Comparaison historique** : Évolution mois par mois
4. **Objectifs quantitatifs** : Tracking automatique
5. **Simulations** : Impact des rééquilibrages proposés
6. **Dividend tracking** : Suivi des dividendes PEA
7. **Rapport trimestriel** : Version approfondie

## Ressources

- [Scripts de calcul](../../scripts/calculators/)
- [Prompt Claude](../../prompts/portfolio-review.md)
- [Template email](../../templates/report-template.md)
- [Workflow n8n](../../n8n/portfolio-advisor/)

## Références

- [Modern Portfolio Theory](https://www.investopedia.com/terms/m/modernportfoliotheory.asp)
- [Diversification](https://www.investopedia.com/terms/d/diversification.asp)
- [Herfindahl Index](https://www.investopedia.com/terms/h/hhi.asp)
- [Sharpe Ratio](https://www.investopedia.com/terms/s/sharperatio.asp)
