# Décision d'Architecture : MCP vs n8n

## Contexte

Le projet PEA Tracker nécessite une architecture pour orchestrer deux agents IA (Market Watcher et Portfolio Advisor) qui doivent accéder à différentes sources de données (Google Drive, Yahoo Finance, Gmail).

## Options évaluées

### Option 1 : n8n + APIs (Architecture initiale)

**Description** : Utiliser n8n comme orchestrateur avec des appels API manuels.

```
Scheduler → n8n → Google Drive API → Parse → Yahoo Finance API
          → Calculate → Claude API → Format → Gmail API
```

**Avantages** :
- Interface visuelle pour créer les workflows
- Nombreux connecteurs prêts à l'emploi
- Pas besoin de développer des parseurs

**Inconvénients** :
- Complexité : 7+ étapes par workflow
- Maintenance : Nombreux points de défaillance
- Rigidité : Workflows fixes, difficiles à adapter
- Coûts : n8n cloud (0-20€/mois) + infrastructure
- Développement : Chaque workflow à créer manuellement
- Parsing manuel des données nécessaire

### Option 2 : MCP (Model Context Protocol) - **RETENUE**

**Description** : Utiliser des serveurs MCP pour donner un accès direct aux agents Claude.

```
Scheduler → Claude Agent (avec MCP) → Direct access to:
                                       - Google Drive
                                       - Yahoo Finance
                                       - Gmail
```

**Avantages** :
- ✅ **Simplicité** : 2 étapes au lieu de 7+ (scheduler → agent)
- ✅ **Flexibilité** : Les agents s'adaptent aux situations
- ✅ **Maintenance** : Point unique de défaillance (l'agent)
- ✅ **Coûts réduits** : Pas besoin de n8n cloud
- ✅ **Développement rapide** : Optimisation de prompts vs workflows
- ✅ **Pas de parsing** : MCP gère la structure des données
- ✅ **Évolutivité** : Ajouter une source = ajouter un serveur MCP

**Inconvénients** :
- Nouveauté : MCP est récent (2024)
- Serveur Yahoo Finance à développer ou trouver
- Moins de GUI (interface visuelle)

### Option 3 : Hybride (Future)

**Description** : n8n pour orchestration + Claude avec MCP pour analyse

**Cas d'usage** : Si besoin de workflows très complexes plus tard

## Décision

**Architecture retenue : MCP pur (Option 2)**

### Justification

1. **Simplicité avant tout** :
   - Le projet vise à être "léger" (philosophie du CLAUDE.md)
   - MCP élimine 70% de la complexité

2. **Coûts** :
   - Budget : 5-40€/mois selon config
   - Avec MCP : 5-20€/mois (seulement Claude API)
   - Sans n8n cloud : économie de 0-20€/mois

3. **Maintenance** :
   - 2 scripts shell vs 3 workflows n8n complexes
   - 2 prompts à optimiser vs 20+ nodes à configurer

4. **Flexibilité** :
   - Agents adaptatifs vs workflows rigides
   - Exemple : Si nouvelle métrique nécessaire, ajuster le prompt vs reconstruire le workflow

5. **Alignement avec la vision** :
   - "Architecture légère basée sur des outils existants"
   - MCP = standard émergent, pas une solution custom

## Architecture finale

### Composants

```
┌─────────────┐
│  Cron Jobs  │  (Scheduling)
└──────┬──────┘
       │
       v
┌─────────────────────────────────┐
│  Claude Agents                  │
│  - Market Watcher (8h daily)    │
│  - Portfolio Advisor (1st/month)│
└────────┬────────────────────────┘
         │
         │ MCP Protocol
         v
┌─────────────────────────────────┐
│  MCP Servers                    │
│  - Google Drive                 │
│  - Gmail                        │
│  - Yahoo Finance                │
└─────────────────────────────────┘
```

### Flux de données Market Watcher

```
1. Cron trigger (8h00)
2. Run script: ./scripts/run-market-watcher.sh
3. Claude agent activated with prompts/market-analysis.md
4. Agent uses MCP tools:
   - mcp__googledrive__find_file("watchlist.csv")
   - mcp__yahoo_finance__get_stock_data(ticker)
   - Calculates indicators internally
   - mcp__gmail__send_email(alert)
5. Log results
```

### Flux de données Portfolio Advisor

```
1. Cron trigger (1st of month, 9h00)
2. Run script: ./scripts/run-portfolio-advisor.sh
3. Claude agent activated with prompts/portfolio-review.md
4. Agent uses MCP tools:
   - mcp__googledrive__list_files("portfolio/")
   - mcp__googledrive__download_file(file_id)
   - Analyzes and generates report internally
   - mcp__gmail__send_email(report)
   - mcp__googledrive__upload_file(report)
5. Log results
```

## Plan de migration

### Phase actuelle : Setup MCP

1. ✅ Documentation créée (docs/architecture/mcp-integration.md)
2. ✅ Configuration MCP (mcp/config.json)
3. ✅ Scripts de lancement (scripts/run-*.sh)
4. 🔄 À faire : Installer serveurs MCP
5. 🔄 À faire : Configurer credentials Google
6. 🔄 À faire : Développer/trouver serveur MCP Yahoo Finance

### Si besoin futur : Passage au hybride

Si les besoins évoluent vers des workflows très complexes :
1. Garder les agents MCP pour l'analyse
2. Ajouter n8n uniquement pour orchestration avancée
3. n8n appelle les agents via API

## Métriques de succès

Pour valider cette décision, mesurer :

| Métrique | Cible | Justification |
|----------|-------|---------------|
| Temps de dev initial | < 1 semaine | vs 2 semaines avec n8n |
| Lignes de code | < 200 | vs 0 mais 3 workflows complexes |
| Coût mensuel | < 15€ | vs 25-40€ avec n8n cloud |
| Temps d'exécution agent | < 2 min | Performance acceptable |
| Taux de succès | > 95% | Fiabilité |

## Risques et mitigations

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| Serveur MCP Yahoo Finance inexistant | Moyen | Moyen | Développer custom ou utiliser HTTP générique |
| MCP encore récent, peu de docs | Faible | Élevé | Documentation officielle + communauté active |
| Pas d'interface visuelle | Faible | Certain | Logs détaillés + scripts bien documentés |
| Coûts Claude API imprévus | Moyen | Faible | Monitoring tokens + caching intelligent |

## Évolution future

### Court terme (0-3 mois)
- Implémenter architecture MCP pure
- Tester et optimiser les prompts
- Mesurer coûts et performances

### Moyen terme (3-6 mois)
- Évaluer si MCP seul suffit
- Si workflows complexes nécessaires : introduire n8n en hybride
- Sinon : continuer avec MCP pur

### Long terme (6-12 mois)
- Automatiser davantage (ML pour scoring)
- Ajouter sources de données (news, fundamentals)
- Évaluer passage à agents autonomes permanents (vs cron)

## Références

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [n8n Documentation](https://docs.n8n.io/)
- [Architecture Decision Records](https://adr.github.io/)

## Auteur

**Date** : 2026-01-07
**Statut** : ✅ Acceptée
**Décideurs** : Équipe PEA Tracker

## Révisions

| Date | Version | Changement | Auteur |
|------|---------|------------|--------|
| 2026-01-07 | 1.0 | Décision initiale : MCP vs n8n | - |

---

Cette décision peut être révisée si les besoins évoluent significativement.
