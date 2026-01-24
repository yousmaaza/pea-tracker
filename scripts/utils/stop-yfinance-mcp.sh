#!/bin/bash
#
# stop-yfinance-mcp.sh
# Arrête proprement le serveur MCP Yahoo Finance s'il a été démarré par nos scripts
#
# Exit codes:
#   0 - Serveur arrêté ou n'était pas actif
#   1 - Erreur lors de l'arrêt

set -euo pipefail

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PID_FILE="/tmp/pea-tracker-yfinance-mcp.pid"
SIGTERM_WAIT=5  # Secondes d'attente avant SIGKILL

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

# Vérifier si le fichier PID existe
if [ ! -f "$PID_FILE" ]; then
    log_info "Aucun PID enregistré - serveur MCP non démarré par nos scripts"
    exit 0
fi

# Lire le PID
SERVER_PID=$(cat "$PID_FILE")
log_info "PID trouvé: $SERVER_PID"

# Vérifier si le processus existe
if ! ps -p $SERVER_PID > /dev/null 2>&1; then
    log_warn "Le processus PID $SERVER_PID n'est plus actif"
    rm -f "$PID_FILE"
    log_info "Fichier PID nettoyé"
    exit 0
fi

# Arrêt gracieux avec SIGTERM
log_info "Envoi de SIGTERM au processus $SERVER_PID..."
kill -TERM $SERVER_PID 2>/dev/null

# Attendre que le processus se termine
log_info "Attente de l'arrêt du processus (max ${SIGTERM_WAIT}s)..."
ELAPSED=0
while ps -p $SERVER_PID > /dev/null 2>&1; do
    if [ $ELAPSED -ge $SIGTERM_WAIT ]; then
        log_warn "Le processus ne s'est pas arrêté après ${SIGTERM_WAIT}s"
        log_warn "Envoi de SIGKILL..."
        kill -KILL $SERVER_PID 2>/dev/null || true
        sleep 1
        break
    fi

    sleep 1
    ELAPSED=$((ELAPSED + 1))
done

# Vérifier que le processus est bien arrêté
if ps -p $SERVER_PID > /dev/null 2>&1; then
    log_error "Impossible d'arrêter le processus $SERVER_PID"
    exit 1
fi

# Cleanup du fichier PID
rm -f "$PID_FILE"
log_info "✓ Serveur MCP Yahoo Finance arrêté proprement"

# Cleanup optionnel du log temporaire
MCP_LOG="/tmp/pea-tracker-yfinance-mcp.log"
if [ -f "$MCP_LOG" ]; then
    rm -f "$MCP_LOG"
    log_info "Log temporaire nettoyé"
fi

exit 0
