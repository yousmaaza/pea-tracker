#!/bin/bash
#
# start-yfinance-mcp.sh
# Démarre le serveur MCP Yahoo Finance si nécessaire
#
# Exit codes:
#   0 - Serveur démarré ou déjà actif
#   1 - Échec du démarrage

set -euo pipefail

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
MCP_PORT=8000
MCP_HOST="localhost"
MCP_HEALTH_ENDPOINT="http://${MCP_HOST}:${MCP_PORT}/health"
PID_FILE="/tmp/pea-tracker-yfinance-mcp.pid"
MAX_WAIT_TIME=${MCP_HEALTH_CHECK_TIMEOUT:-30}  # secondes
RETRY_INTERVAL=1  # secondes

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

# Fonction pour vérifier si le serveur répond
check_server_health() {
    if curl -s --max-time 2 "$MCP_HEALTH_ENDPOINT" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Fonction pour vérifier si le port est occupé
is_port_occupied() {
    if lsof -ti:$MCP_PORT &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# 1. Vérifier si le serveur est déjà actif et fonctionne
log_info "Vérification du serveur MCP Yahoo Finance sur port $MCP_PORT..."

if check_server_health; then
    log_info "✓ Serveur MCP Yahoo Finance déjà actif et répond correctement"

    # Vérifier si on a un PID enregistré
    if [ -f "$PID_FILE" ]; then
        EXISTING_PID=$(cat "$PID_FILE")
        log_info "PID existant: $EXISTING_PID"
    fi

    exit 0
fi

# 2. Vérifier si le port est occupé mais serveur ne répond pas
if is_port_occupied; then
    OCCUPYING_PID=$(lsof -ti:$MCP_PORT)
    log_warn "Port $MCP_PORT occupé par PID $OCCUPYING_PID mais serveur ne répond pas"
    log_warn "Processus: $(ps -p $OCCUPYING_PID -o comm= 2>/dev/null || echo 'inconnu')"
    log_error "Impossible de démarrer le serveur MCP"
    exit 1
fi

# 3. Démarrer le serveur
log_info "Démarrage du serveur MCP Yahoo Finance..."

# Vérifier le chemin du serveur MCP
if [ -z "${YAHOO_FINANCE_MCP_PATH:-}" ]; then
    log_error "YAHOO_FINANCE_MCP_PATH non défini"
    log_error "Définir dans config/.env : YAHOO_FINANCE_MCP_PATH=/chemin/vers/yahoo-finance-mcp"
    exit 1
fi

if [ ! -d "$YAHOO_FINANCE_MCP_PATH" ]; then
    log_error "Répertoire MCP Yahoo Finance non trouvé: $YAHOO_FINANCE_MCP_PATH"
    exit 1
fi

if [ ! -f "$YAHOO_FINANCE_MCP_PATH/server.py" ]; then
    log_error "server.py non trouvé dans $YAHOO_FINANCE_MCP_PATH"
    exit 1
fi

# Démarrer le serveur en arrière-plan
log_info "Lancement de python3 server.py dans $YAHOO_FINANCE_MCP_PATH"
cd "$YAHOO_FINANCE_MCP_PATH"

# Rediriger sortie vers un log temporaire
MCP_LOG="/tmp/pea-tracker-yfinance-mcp.log"
nohup python3 server.py > "$MCP_LOG" 2>&1 &
SERVER_PID=$!

# Enregistrer le PID
echo $SERVER_PID > "$PID_FILE"
log_info "Serveur démarré avec PID: $SERVER_PID"

# 4. Attendre que le serveur soit prêt (health check avec retry)
log_info "Attente de la disponibilité du serveur (max ${MAX_WAIT_TIME}s)..."

ELAPSED=0
while [ $ELAPSED -lt $MAX_WAIT_TIME ]; do
    if check_server_health; then
        log_info "✓ Serveur MCP Yahoo Finance opérationnel après ${ELAPSED}s"
        exit 0
    fi

    # Vérifier que le processus est toujours actif
    if ! ps -p $SERVER_PID > /dev/null 2>&1; then
        log_error "Le processus serveur (PID $SERVER_PID) s'est arrêté"
        log_error "Dernières lignes du log:"
        tail -n 20 "$MCP_LOG"
        rm -f "$PID_FILE"
        exit 1
    fi

    sleep $RETRY_INTERVAL
    ELAPSED=$((ELAPSED + RETRY_INTERVAL))

    # Afficher progression tous les 5 secondes
    if [ $((ELAPSED % 5)) -eq 0 ]; then
        log_info "Attente... (${ELAPSED}s/${MAX_WAIT_TIME}s)"
    fi
done

# Timeout atteint
log_error "Timeout: Le serveur n'a pas répondu après ${MAX_WAIT_TIME}s"
log_error "Arrêt du processus..."
kill $SERVER_PID 2>/dev/null || true
rm -f "$PID_FILE"

log_error "Dernières lignes du log:"
tail -n 20 "$MCP_LOG"

exit 1
