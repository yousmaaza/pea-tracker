# Commande pip-mode

Bascule entre le mode pip standard (PyPI) et le mode Nexus pour la gestion des packages Python.

## Usage

```bash
/pip-mode [nexus|standard|status]
```

## Description

Cette commande permet de configurer dynamiquement l'environnement pip pour utiliser soit le dépôt PyPI standard, soit le dépôt Nexus interne.

### Modes disponibles

- **nexus** : Configure pip pour utiliser le dépôt Nexus
  - Index URL: https://nexus-ext.cnt.zone.local/repository/cnt-pypi-public/simple
  - Trusted Host: nexus-ext.cnt.zone.local

- **standard** : Configure pip pour utiliser PyPI standard (par défaut)
  - Supprime les configurations Nexus

- **status** : Affiche la configuration actuelle

## Comportement

Lorsque vous exécutez cette commande, je vais :

1. Configurer les variables d'environnement appropriées selon le mode choisi
2. Exporter les variables dans votre session shell actuelle
3. Confirmer le changement avec un message de statut

### Variables d'environnement

- `PIP_INDEX_URL` : URL de l'index pip à utiliser
- `PIP_TRUSTED_HOST` : Hôte de confiance pour les connexions HTTPS
- `NEXUS_INDEX` : URL du dépôt Nexus (constante)
- `NEXUS_HOST` : Hôte Nexus (constante)

## Exemples

### Basculer en mode Nexus
```bash
/pip-mode nexus
```
Résultat : Configure pip pour utiliser le dépôt Nexus

### Revenir en mode standard
```bash
/pip-mode standard
```
Résultat : Configure pip pour utiliser PyPI standard

### Vérifier la configuration actuelle
```bash
/pip-mode status
```
Résultat : Affiche les variables d'environnement actuelles

## Workflow recommandé

Pour travailler avec Python dans ce projet :

1. **Démarrage** : Basculer en mode standard
   ```bash
   /pip-mode standard
   ```

2. **Créer l'environnement virtuel**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Si besoin de Nexus** : Basculer en mode Nexus
   ```bash
   /pip-mode nexus
   pip install package-from-nexus
   ```

## Notes

- Les changements de configuration persistent uniquement pour la session shell en cours
- Pour une configuration permanente, ajoutez les exports dans votre `~/.zshrc` ou `~/.bashrc`
- La commande utilise `export` pour que les variables soient disponibles dans les sous-processus

## Intégration avec le projet PEA Tracker

Cette commande est particulièrement utile pour :
- Configurer l'environnement avant d'exécuter les agents Claude
- Gérer les dépendances des agents Market Watcher et Portfolio Advisor
- Basculer entre environnements de développement (standard) et production (Nexus)
