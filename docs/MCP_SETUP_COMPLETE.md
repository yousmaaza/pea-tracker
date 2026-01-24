# Guide complet de configuration MCP pour Market Watcher PEA

Ce guide détaille la configuration complète des serveurs MCP nécessaires au fonctionnement du Market Watcher.

---

## Table des matières

1. [Prérequis](#prérequis)
2. [Installation des serveurs MCP](#installation-des-serveurs-mcp)
3. [Configuration Google Drive](#configuration-google-drive)
4. [Configuration Gmail](#configuration-gmail)
5. [Configuration Yahoo Finance](#configuration-yahoo-finance)
6. [Fichier de configuration final](#fichier-de-configuration-final)
7. [Tests de validation](#tests-de-validation)
8. [Troubleshooting](#troubleshooting)

---

## Prérequis

### Logiciels requis

- **Node.js** >= 16.x
- **Python** >= 3.11
- **Claude Code CLI** (dernière version)
- **Compte Google** avec accès à Drive et Gmail
- **npm** (inclus avec Node.js)

Vérifier les installations:
```bash
node --version    # >= 16.x
python3 --version # >= 3.11
npm --version
```

### Compte Google

Vous aurez besoin:
- Un compte Google actif
- Accès à Google Cloud Console
- Validation en 2 étapes activée (pour Gmail)

---

## Installation des serveurs MCP

### 1. Google Drive MCP Server

```bash
# Installation globale
npm install -g @modelcontextprotocol/server-google-drive

# Vérifier l'installation
which mcp-server-google-drive
```

### 2. Gmail MCP Server

```bash
# Installation globale
npm install -g @modelcontextprotocol/server-gmail

# Vérifier l'installation
which mcp-server-gmail
```

### 3. Yahoo Finance MCP Server

```bash
# Installation globale
npm install -g mcp-server-yfinance

# Vérifier l'installation
which mcp-server-yfinance
```

---

## Configuration Google Drive

### Étape 1: Créer un projet Google Cloud

1. Aller sur [Google Cloud Console](https://console.cloud.google.com/)
2. Cliquer sur "Nouveau projet"
3. Nommer le projet: "PEA Tracker MCP"
4. Cliquer sur "Créer"

### Étape 2: Activer l'API Google Drive

1. Dans le projet créé, aller dans "APIs & Services" > "Library"
2. Rechercher "Google Drive API"
3. Cliquer sur "Google Drive API"
4. Cliquer sur "Activer"

### Étape 3: Créer des credentials OAuth 2.0

1. Aller dans "APIs & Services" > "Credentials"
2. Cliquer sur "Create Credentials" > "OAuth client ID"
3. Si demandé, configurer l'écran de consentement OAuth:
   - Type d'application: Externe
   - Nom de l'application: "PEA Tracker"
   - Email: votre email
   - Scopes: `https://www.googleapis.com/auth/drive`
4. Type d'application: "Application de bureau" (Desktop app)
5. Nom: "PEA Tracker Desktop"
6. Cliquer sur "Créer"
7. **Télécharger le JSON** avec Client ID et Client Secret

### Étape 4: Obtenir un Refresh Token

Créer un script pour obtenir le refresh token:

```bash
cat > /tmp/get_google_token.py << 'EOF'
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_refresh_token(client_secrets_file):
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES)
    creds = flow.run_local_server(port=0)

    print("\n" + "="*60)
    print("✅ Authentication successful!")
    print("="*60)
    print(f"\nClient ID: {creds.client_id}")
    print(f"Client Secret: {creds.client_secret}")
    print(f"Refresh Token: {creds.refresh_token}")
    print("="*60)

    return creds.refresh_token

# Remplacer par le chemin de votre fichier JSON téléchargé
client_secrets = 'path/to/your/client_secrets.json'
get_refresh_token(client_secrets)
EOF

# Installer la bibliothèque nécessaire
pip3 install google-auth-oauthlib google-auth-httplib2

# Exécuter le script (remplacer le chemin)
python3 /tmp/get_google_token.py
```

**Important**: Copier les valeurs affichées:
- `Client ID`
- `Client Secret`
- `Refresh Token`

### Étape 5: Créer la structure Google Drive

1. Aller sur [Google Drive](https://drive.google.com)
2. Créer un dossier "PEA-Tracker" à la racine
3. Créer les sous-dossiers:
   ```
   PEA-Tracker/
   ├── Imports/
   ├── Reports/
   │   ├── monthly/
   │   └── signals/
   ```

### Étape 6: Créer le fichier Excel watchlist

Créer un fichier Google Sheets nommé `PEA_Watchlist_Indicateurs` dans le dossier `PEA-Tracker/`.

**Feuille 1: "Watchlist"**

| Ticker | Nom | Marché | Secteur | Pays | Actif | Date ajout | Notes |
|--------|-----|--------|---------|------|-------|------------|-------|
| MC.PA | LVMH | Euronext Paris | Luxe | France | TRUE | 2026-01-24 | |
| OR.PA | L'Oréal | Euronext Paris | Cosmétiques | France | TRUE | 2026-01-24 | |
| AI.PA | Air Liquide | Euronext Paris | Chimie | France | TRUE | 2026-01-24 | |

**Feuille 2: "Indicateurs"**

| Ticker | Date dernière MAJ | RSI | MACD | MA20 | MA50 | MA200 | Volume moyen 20j | Dernier signal | Score confiance |
|--------|-------------------|-----|------|------|------|-------|------------------|----------------|-----------------|
| MC.PA | | | | | | | | | |
| OR.PA | | | | | | | | | |
| AI.PA | | | | | | | | | |

**Feuille 3: "Positions"**

| Ticker | Quantité | Prix moyen achat | Date dernière transaction | Valeur totale |
|--------|----------|------------------|---------------------------|---------------|
| | | | | |

Ensuite, **Télécharger en format Excel** (.xlsx):
- Fichier > Télécharger > Microsoft Excel (.xlsx)
- Uploader le fichier `.xlsx` dans le dossier `PEA-Tracker/` sur Google Drive

---

## Configuration Gmail

### Étape 1: Activer la validation en 2 étapes

1. Aller dans [Compte Google](https://myaccount.google.com/)
2. Sécurité > Validation en deux étapes
3. Suivre les instructions pour activer

### Étape 2: Créer un mot de passe d'application

1. Toujours dans Sécurité, chercher "Mots de passe des applications"
2. Si disponible, cliquer dessus
3. Sélectionner "Autre (nom personnalisé)"
4. Entrer: "Claude Code PEA Tracker"
5. Cliquer sur "Générer"
6. **Copier le mot de passe de 16 caractères** (sans espaces)

**Note**: Si "Mots de passe des applications" n'est pas visible, assurez-vous que:
- La validation en 2 étapes est activée
- Vous utilisez un compte Google Workspace (pas de restriction admin)

### Étape 3: Tester l'envoi d'email

```python
cat > /tmp/test_gmail.py << 'EOF'
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_gmail(email, app_password):
    sender = email
    recipient = email  # Envoyer à soi-même

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = "Test PEA Tracker - Configuration Gmail"

    body = "✅ Configuration Gmail réussie! Le Market Watcher peut envoyer des alertes."
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, app_password)
        server.send_message(msg)
        server.quit()

        print("✅ Email envoyé avec succès!")
        print(f"Vérifier votre boîte mail: {email}")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

# Remplacer par vos valeurs
email = "votre.email@gmail.com"
app_password = "votre mot de passe d'application"

test_gmail(email, app_password)
EOF

python3 /tmp/test_gmail.py
```

---

## Configuration Yahoo Finance

Aucune configuration spéciale requise. Yahoo Finance MCP est prêt à l'emploi.

Tester la connexion:

```python
cat > /tmp/test_yfinance.py << 'EOF'
import yfinance as yf
from datetime import datetime

print("\n🔍 Test Yahoo Finance API")
print("="*60)

tickers = ["MC.PA", "OR.PA", "AI.PA"]

for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="5d")

        if not hist.empty:
            current_price = hist['Close'].iloc[-1]
            print(f"✅ {ticker}: {current_price:.2f}€")
        else:
            print(f"⚠️  {ticker}: Pas de données")
    except Exception as e:
        print(f"❌ {ticker}: Erreur - {e}")

print("="*60 + "\n")
EOF

# Installer yfinance si nécessaire
pip3 install yfinance

python3 /tmp/test_yfinance.py
```

---

## Fichier de configuration final

Créer ou éditer le fichier de configuration MCP pour Claude Code.

### Option 1: Configuration globale

Fichier: `~/.config/claude-code/mcp_settings.json`

```json
{
  "mcpServers": {
    "google-drive": {
      "command": "mcp-server-google-drive",
      "args": [],
      "env": {
        "GOOGLE_CLIENT_ID": "VOTRE_CLIENT_ID.apps.googleusercontent.com",
        "GOOGLE_CLIENT_SECRET": "VOTRE_CLIENT_SECRET",
        "GOOGLE_REFRESH_TOKEN": "VOTRE_REFRESH_TOKEN"
      }
    },
    "gmail": {
      "command": "mcp-server-gmail",
      "args": [],
      "env": {
        "GMAIL_ADDRESS": "votre.email@gmail.com",
        "GMAIL_APP_PASSWORD": "votre mot de passe application"
      }
    },
    "yfinance": {
      "command": "mcp-server-yfinance",
      "args": []
    }
  }
}
```

### Option 2: Configuration projet

Fichier: `/Users/yousrids/Documents/pea-tracker/.claude/settings.local.json`

Ajouter la section `mcpServers` au fichier existant:

```json
{
  "permissions": {
    "allow": [
      "Skill(pip-mode)",
      "Bash(export PIP_INDEX_URL=\"\")",
      "Bash(export PIP_TRUSTED_HOST=\"\")",
      "Bash(python3:*)",
      "Bash(source venv_mcp/bin/activate)",
      "Bash(pip install:*)",
      "Bash(source venv_market_watcher/bin/activate:*)"
    ]
  },
  "mcpServers": {
    "google-drive": {
      "command": "mcp-server-google-drive",
      "args": [],
      "env": {
        "GOOGLE_CLIENT_ID": "VOTRE_CLIENT_ID",
        "GOOGLE_CLIENT_SECRET": "VOTRE_CLIENT_SECRET",
        "GOOGLE_REFRESH_TOKEN": "VOTRE_REFRESH_TOKEN"
      }
    },
    "gmail": {
      "command": "mcp-server-gmail",
      "args": [],
      "env": {
        "GMAIL_ADDRESS": "votre.email@gmail.com",
        "GMAIL_APP_PASSWORD": "votremotdepasse"
      }
    },
    "yfinance": {
      "command": "mcp-server-yfinance",
      "args": []
    }
  }
}
```

**Important**: Ne jamais commiter ce fichier dans Git. Il est déjà dans `.gitignore`.

---

## Tests de validation

### Test 1: Vérifier les serveurs MCP

```bash
# Lister les serveurs configurés
claude-code mcp list

# Devrait afficher:
# - google-drive
# - gmail
# - yfinance
```

### Test 2: Tester Google Drive

```bash
# Dans Claude Code
claude-code

# Puis dans l'interface
> mcp__googledrive__search_files(q="name='PEA_Watchlist_Indicateurs'")
```

Devrait retourner le fichier Excel.

### Test 3: Tester Gmail

```bash
# Dans Claude Code
> mcp__gmail__send_email(
    recipient_email="votre.email@gmail.com",
    subject="Test PEA Tracker",
    body="Configuration réussie!",
    is_html=false
  )
```

Devrait envoyer un email de test.

### Test 4: Tester Yahoo Finance

```bash
# Dans Claude Code
> mcp__yfinance__get_stock_info(ticker="MC.PA")
```

Devrait retourner les informations de LVMH.

### Test 5: Test complet Market Watcher

```bash
cd /Users/yousrids/Documents/pea-tracker
python3 market_watcher_mcp.py
```

Devrait:
1. Analyser les tickers de la watchlist
2. Calculer les indicateurs
3. Générer des signaux
4. Créer des rapports Markdown
5. (Si MCP configuré) Uploader vers Drive et envoyer emails

---

## Troubleshooting

### Problème: "Command not found: mcp-server-google-drive"

**Solution**:
```bash
# Vérifier l'installation
npm list -g | grep mcp

# Réinstaller si nécessaire
npm install -g @modelcontextprotocol/server-google-drive

# Vérifier le PATH
echo $PATH | grep npm
```

### Problème: "Invalid refresh token"

**Causes possibles**:
- Le refresh token a expiré
- Le client ID/secret ne correspond pas

**Solution**:
Regénérer le refresh token avec le script Python fourni.

### Problème: "Authentication failed" pour Gmail

**Causes possibles**:
- Mot de passe d'application incorrect
- Validation en 2 étapes non activée
- Email incorrect

**Solution**:
1. Vérifier que la validation en 2 étapes est activée
2. Régénérer un nouveau mot de passe d'application
3. S'assurer qu'il n'y a pas d'espaces dans le mot de passe

### Problème: Yahoo Finance ne retourne pas de données

**Causes possibles**:
- Ticker incorrect (ex: MC.PA vs MC)
- Problème de connexion internet
- Yahoo Finance API temporairement indisponible

**Solution**:
```python
# Tester manuellement
import yfinance as yf
ticker = yf.Ticker("MC.PA")
print(ticker.history(period="1d"))
```

### Problème: "Permission denied" pour Google Drive

**Causes possibles**:
- Les scopes OAuth ne incluent pas Drive
- Le dossier PEA-Tracker n'existe pas
- Permissions insuffisantes

**Solution**:
1. Recréer les credentials avec le scope correct: `https://www.googleapis.com/auth/drive`
2. Vérifier que le dossier existe dans Google Drive
3. Régénérer le refresh token

---

## Sécurité

### Variables d'environnement (recommandé)

Au lieu de mettre les credentials directement dans le JSON, utiliser des variables d'environnement:

```bash
# Ajouter dans ~/.zshrc ou ~/.bashrc
export GOOGLE_CLIENT_ID="votre_client_id"
export GOOGLE_CLIENT_SECRET="votre_client_secret"
export GOOGLE_REFRESH_TOKEN="votre_refresh_token"
export GMAIL_ADDRESS="votre.email@gmail.com"
export GMAIL_APP_PASSWORD="votre_mot_de_passe"
```

Puis dans le fichier de configuration:

```json
{
  "mcpServers": {
    "google-drive": {
      "command": "mcp-server-google-drive",
      "args": [],
      "env": {
        "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
        "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}",
        "GOOGLE_REFRESH_TOKEN": "${GOOGLE_REFRESH_TOKEN}"
      }
    }
  }
}
```

### Fichiers à ne jamais commiter

Ajouter dans `.gitignore`:
```
.claude/settings.local.json
credentials.json
token.json
.env
*_secrets.json
```

---

## Ressources additionnelles

- [Documentation MCP officielle](https://modelcontextprotocol.io/)
- [Google OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
- [Yahoo Finance Python](https://github.com/ranaroussi/yfinance)

---

## Checklist finale

Avant de lancer le Market Watcher en production:

- [ ] Node.js et npm installés
- [ ] Python 3.11+ installé
- [ ] Serveurs MCP installés (google-drive, gmail, yfinance)
- [ ] Projet Google Cloud créé
- [ ] API Google Drive activée
- [ ] Credentials OAuth créés
- [ ] Refresh token obtenu
- [ ] Structure Google Drive créée
- [ ] Fichier Excel watchlist créé et uploadé
- [ ] Validation en 2 étapes activée sur Gmail
- [ ] Mot de passe d'application Gmail généré
- [ ] Fichier de configuration MCP créé
- [ ] Variables d'environnement configurées (optionnel)
- [ ] Test Google Drive réussi
- [ ] Test Gmail réussi
- [ ] Test Yahoo Finance réussi
- [ ] Test Market Watcher complet réussi

---

**Date de dernière mise à jour**: 2026-01-24
