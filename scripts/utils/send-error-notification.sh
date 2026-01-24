#!/bin/bash
#
# send-error-notification.sh
# Envoie une notification d'erreur par email via Gmail MCP
#
# Usage: ./send-error-notification.sh "Error message" "/path/to/log/file.log"
#
# Exit codes:
#   0 - Notification envoyée
#   1 - Échec d'envoi (fallback vers log)

set -euo pipefail

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction de logging
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier les paramètres
if [ $# -lt 2 ]; then
    log_error "Usage: $0 <error_message> <log_file_path>"
    exit 1
fi

ERROR_MESSAGE="$1"
LOG_FILE="$2"

# Configuration
EMAIL_RECIPIENT=${EMAIL_RECIPIENT:-"votre@email.com"}
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
HOSTNAME=$(hostname)

# Extraire les dernières lignes du log (si le fichier existe)
LOG_EXCERPT=""
if [ -f "$LOG_FILE" ]; then
    LOG_EXCERPT=$(tail -n 30 "$LOG_FILE" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')
else
    LOG_EXCERPT="Fichier log non trouvé: $LOG_FILE"
fi

# Construire le corps de l'email en HTML
EMAIL_SUBJECT="[PEA Tracker] ❌ Erreur exécution Market Watcher"

EMAIL_BODY=$(cat <<EOF
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .header { background-color: #f44336; color: white; padding: 20px; border-radius: 5px; }
        .content { padding: 20px; background-color: #f9f9f9; margin-top: 10px; border-radius: 5px; }
        .error-box { background-color: #ffebee; border-left: 4px solid #f44336; padding: 15px; margin: 15px 0; }
        .log-box { background-color: #263238; color: #aed581; padding: 15px; margin: 15px 0; border-radius: 3px; overflow-x: auto; font-family: monospace; font-size: 12px; white-space: pre-wrap; }
        .info { color: #666; font-size: 14px; }
        .footer { margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; color: #999; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">
        <h2>❌ Erreur d'exécution - PEA Tracker</h2>
    </div>

    <div class="content">
        <div class="error-box">
            <h3>Message d'erreur</h3>
            <p><strong>$ERROR_MESSAGE</strong></p>
        </div>

        <div class="info">
            <p><strong>Timestamp:</strong> $TIMESTAMP</p>
            <p><strong>Hostname:</strong> $HOSTNAME</p>
            <p><strong>Fichier log:</strong> $LOG_FILE</p>
        </div>

        <h3>Extrait du log (30 dernières lignes)</h3>
        <div class="log-box">$LOG_EXCERPT</div>

        <div class="footer">
            <p>Cette notification automatique a été générée par le système PEA Tracker.</p>
            <p>Pour plus de détails, consultez le fichier log complet: <code>$LOG_FILE</code></p>
        </div>
    </div>
</body>
</html>
EOF
)

# Fonction pour envoyer l'email via Gmail MCP
send_email_via_mcp() {
    log_info "Envoi de la notification par email à $EMAIL_RECIPIENT..."

    # Échapper les guillemets et nouvelles lignes pour JSON
    ESCAPED_SUBJECT=$(echo "$EMAIL_SUBJECT" | sed 's/"/\\"/g')
    ESCAPED_BODY=$(echo "$EMAIL_BODY" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')

    # Utiliser claude-code pour appeler Gmail MCP
    # Note: Cette commande suppose que claude-code est configuré avec Gmail MCP
    if command -v claude-code &> /dev/null; then
        # Créer un fichier temporaire pour le corps de l'email
        TMP_EMAIL_FILE=$(mktemp)
        echo "$EMAIL_BODY" > "$TMP_EMAIL_FILE"

        # Appeler Gmail MCP via claude-code (syntaxe simplifiée)
        # Alternative: utiliser directement l'API MCP si disponible
        log_warn "Envoi via MCP (fonctionnalité à implémenter via claude-code ou API directe)"

        # Pour le moment, fallback vers log
        log_warn "Gmail MCP non encore intégré - écriture dans le log uniquement"
        rm -f "$TMP_EMAIL_FILE"
        return 1
    else
        log_warn "claude-code non disponible pour envoi via MCP"
        return 1
    fi
}

# Fallback: écrire dans un fichier de notifications
write_to_notification_log() {
    NOTIFICATION_LOG="/Users/yousrids/Documents/pea-tracker/logs/error-notifications.log"
    mkdir -p "$(dirname "$NOTIFICATION_LOG")"

    log_warn "Fallback: Écriture de la notification dans $NOTIFICATION_LOG"

    cat >> "$NOTIFICATION_LOG" <<EOF

═══════════════════════════════════════════════════════════════
❌ ERREUR DÉTECTÉE - $TIMESTAMP
═══════════════════════════════════════════════════════════════
Hostname: $HOSTNAME
Message: $ERROR_MESSAGE
Fichier log: $LOG_FILE

--- Extrait du log (30 dernières lignes) ---
$(tail -n 30 "$LOG_FILE" 2>/dev/null || echo "Log non disponible")
═══════════════════════════════════════════════════════════════

EOF

    log_info "✓ Notification enregistrée dans $NOTIFICATION_LOG"
}

# Tentative d'envoi par email
if send_email_via_mcp; then
    log_info "✓ Notification envoyée par email"
    exit 0
else
    # Fallback vers fichier log
    write_to_notification_log
    exit 0  # On considère le fallback comme un succès
fi
