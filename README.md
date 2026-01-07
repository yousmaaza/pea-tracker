# PEA Tracker - Suivi Intelligent de Portefeuille

Plateforme intelligente de gestion de portefeuille PEA composée de deux agents IA autonomes qui collaborent pour optimiser les décisions d'investissement.

## Démarrage rapide

1. **Lire la documentation complète** : [CLAUDE.md](./CLAUDE.md)
2. **Configurer l'environnement** : Copier `config/.env.example` vers `config/.env`
3. **Suivre la roadmap** : Phase 1 - Setup Infrastructure
4. **Consulter les specs des agents** :
   - [Market Watcher](./docs/agents/market-watcher-spec.md)
   - [Portfolio Advisor](./docs/agents/portfolio-advisor-spec.md)

## Vue d'ensemble

### Les deux agents IA

**🔍 Market Watcher** - Surveillance des marchés
- Analyse temps réel des indicateurs techniques
- Génération d'alertes d'opportunités (achat/vente)
- Scoring de fiabilité des signaux
- Fréquence : Quotidien à 8h

**📊 Portfolio Advisor** - Analyse de portefeuille
- Calcul de performance mensuelle
- Analyse d'allocation et diversification
- Recommandations stratégiques personnalisées
- Fréquence : Mensuel (1er du mois)

## Architecture

```
Boursorama → Export Excel → Google Drive → n8n → Claude API → Gmail
```

### Stack technique

- **Stockage** : Google Drive + Google Sheets
- **Orchestration** : n8n (workflows automatisés)
- **Intelligence** : Claude API (Anthropic)
- **Données** : Yahoo Finance API
- **Notifications** : Gmail

## Structure du projet

```
pea-tracker/
├── CLAUDE.md                 # Documentation complète du projet
├── README.md                 # Ce fichier
├── .gitignore
│
├── docs/                     # Documentation
│   ├── agents/              # Spécifications des agents
│   │   ├── market-watcher-spec.md
│   │   └── portfolio-advisor-spec.md
│   ├── workflows/           # Documentation workflows n8n
│   └── api/                 # Documentation APIs
│
├── n8n/                     # Workflows n8n
│   ├── README.md           # Guide n8n
│   ├── portfolio-sync/
│   ├── market-watcher/
│   └── portfolio-advisor/
│
├── templates/               # Templates Excel et rapports
│   ├── import-template.xlsx
│   ├── watchlist-template.xlsx
│   └── report-template.md
│
├── scripts/                 # Scripts utilitaires
│   ├── parsers/            # Parseurs de données
│   └── calculators/        # Calculateurs d'indicateurs
│
├── prompts/                # Prompts Claude optimisés
│   ├── market-analysis.md
│   └── portfolio-review.md
│
└── config/                 # Configuration
    ├── .env.example
    ├── alert-thresholds.json
    └── notification-settings.json
```

## Installation

### Prérequis

- Compte Google (Drive + Gmail)
- n8n installé (Docker ou npm)
- Clé API Claude (Anthropic)
- Accès Yahoo Finance API (gratuit)

### Étape 1 : Cloner le projet

```bash
git clone <votre-repo>
cd pea-tracker
```

### Étape 2 : Configuration

```bash
# Copier le fichier d'environnement
cp config/.env.example config/.env

# Éditer avec vos clés API
nano config/.env
```

### Étape 3 : Installer n8n

**Option Docker** :
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**Option npm** :
```bash
npm install n8n -g
n8n start
```

Accéder à : http://localhost:5678

### Étape 4 : Configurer Google Drive

1. Créer la structure de dossiers :
   ```
   PEA-Tracker/
   ├── Imports/
   ├── Data/
   ├── Rapports/
   └── Config/
   ```

2. Configurer les credentials n8n pour Google Drive et Gmail

### Étape 5 : Importer les workflows n8n

Consulter [n8n/README.md](./n8n/README.md) pour instructions détaillées.

## Utilisation

### 0. Configuration pip (Nexus/PyPI)

Le projet inclut un utilitaire pour basculer entre les dépôts pip :

```bash
# Vérifier la configuration actuelle
./scripts/pip-mode.sh status

# Utiliser PyPI standard (recommandé pour développement)
./scripts/pip-mode.sh standard

# Utiliser Nexus interne (si disponible)
./scripts/pip-mode.sh nexus
```

**Via Claude Code** :
```bash
/pip-mode standard
/pip-mode nexus
/pip-mode status
```

Voir [docs/pip-mode-guide.md](./docs/pip-mode-guide.md) pour plus de détails.

### 1. Surveillance des marchés (Market Watcher)

Le workflow s'exécute automatiquement chaque jour à 8h :
- Analyse les titres de votre watchlist
- Calcule les indicateurs techniques
- Génère des alertes si opportunités détectées
- Envoie les alertes par email

**Configurer votre watchlist** :
Créer un Google Sheet avec vos titres à surveiller (voir templates/).

### 2. Synchronisation du portefeuille

Le workflow s'exécute automatiquement chaque jour à 19h :
- Détecte les nouveaux exports Boursorama
- Parse et consolide les données
- Met à jour l'historique

**Exporter depuis Boursorama** :
1. Se connecter à Boursorama
2. PEA → Télécharger l'historique (Excel)
3. Déposer le fichier dans Google Drive/PEA-Tracker/Imports/

### 3. Rapport mensuel (Portfolio Advisor)

Le workflow s'exécute le 1er de chaque mois à 9h :
- Analyse complète du portefeuille
- Calcul de performance
- Recommandations stratégiques
- Envoi du rapport par email

**Exécution manuelle** :
Possible via l'interface n8n si besoin d'un rapport à la demande.

## Configuration avancée

### Seuils d'alertes

Éditer `config/alert-thresholds.json` :
```json
{
  "technical_indicators": {
    "rsi": {
      "oversold": 30,
      "overbought": 70
    }
  },
  "alert_scoring": {
    "min_confidence_score": 60
  }
}
```

### Notifications

Éditer `config/notification-settings.json` :
```json
{
  "email": {
    "to": "your-email@example.com"
  },
  "notification_preferences": {
    "min_alert_score": 60,
    "max_daily_alerts": 10
  }
}
```

## Coûts estimés

| Service | Coût mensuel |
|---------|--------------|
| Google Workspace | Gratuit |
| n8n (self-hosted) | 0€ |
| n8n (cloud) | 0-20€ |
| Claude API | 5-20€ |
| Yahoo Finance | Gratuit |
| **Total** | **5-40€/mois** |

## Développement

### Ajouter un nouvel indicateur technique

1. Créer la fonction dans `scripts/calculators/`
2. L'intégrer dans le workflow Market Watcher
3. Mettre à jour le prompt Claude
4. Tester avec des données historiques

### Personnaliser les rapports

1. Éditer `prompts/portfolio-review.md`
2. Modifier le template dans `templates/report-template.md`
3. Ajuster le workflow n8n si nécessaire

## Troubleshooting

### Les alertes ne sont pas envoyées

1. Vérifier que le workflow Market Watcher est activé
2. Vérifier les credentials Gmail dans n8n
3. Vérifier le score minimum dans la configuration
4. Consulter les logs d'exécution n8n

### Le rapport mensuel n'est pas généré

1. Vérifier la clé API Claude
2. Vérifier les données du portefeuille dans Google Sheets
3. Consulter les logs d'erreur dans n8n

### Erreur Yahoo Finance API

1. Vérifier le format des tickers (ex: MC.PA pour LVMH)
2. Vérifier la connexion internet
3. Attendre quelques minutes (rate limiting possible)

## Sécurité

- Ne jamais commiter les fichiers `.env`
- Utiliser des mots de passe d'application Gmail
- Limiter les permissions Google Drive
- Chiffrer les données sensibles
- Sauvegarder régulièrement la configuration

## Roadmap

### Phase 1 : Setup Infrastructure ✅
- [x] Structure du projet
- [x] Configuration de base
- [ ] Installation n8n
- [ ] Configuration Google Drive
- [ ] Obtention clés API

### Phase 2 : Workflow Portfolio Sync
- [ ] Détection nouveaux fichiers
- [ ] Parsing Excel
- [ ] Consolidation historique
- [ ] Calcul métriques de base

### Phase 3 : Agent Market Watcher
- [ ] Intégration Yahoo Finance
- [ ] Calcul indicateurs techniques
- [ ] Système de scoring
- [ ] Workflow alertes
- [ ] Prompt Claude

### Phase 4 : Agent Portfolio Advisor
- [ ] Calcul performance
- [ ] Analyse allocation
- [ ] Template rapport
- [ ] Prompt Claude
- [ ] Workflow envoi rapport

### Phase 5 : Améliorations
- [ ] Profil de risque personnalisé
- [ ] Backtesting
- [ ] Actualités financières
- [ ] Dashboard web

## Support et contribution

### Signaler un bug

Créer une issue avec :
- Description du problème
- Étapes pour reproduire
- Logs d'erreur
- Configuration (sans clés API)

### Proposer une amélioration

Les pull requests sont les bienvenues !

### Questions

Consulter d'abord :
- [CLAUDE.md](./CLAUDE.md) - Documentation complète
- [docs/agents/](./docs/agents/) - Spécifications détaillées
- [n8n/README.md](./n8n/README.md) - Guide n8n

## Licence

[À définir]

## Disclaimer

⚠️ **Important** : Ce projet est un outil d'aide à la décision. Il ne constitue en aucun cas un conseil en investissement. Les décisions d'investissement restent sous votre entière responsabilité. Les performances passées ne préjugent pas des performances futures.

Cet outil ne remplace pas l'analyse et le jugement humain. Toujours effectuer vos propres recherches avant d'investir.

---

**Version** : 1.0.0
**Dernière mise à jour** : 2026-01-07
**Statut** : En développement

Créé avec Claude Code
