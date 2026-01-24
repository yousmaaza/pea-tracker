#!/bin/bash
#
# start-yfinance-mcp.sh
# Démarre le serveur MCP Yahoo Finance via Docker si nécessaire
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
MCP_SSE_ENDPOINT="http://${MCP_HOST}:${MCP_PORT}/sse"
DOCKER_CONTAINER_NAME="yfinance-mcp"
DOCKER_IMAGE_NAME="yahoo-finance-mcp"
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

# Fonction pour vérifier si le serveur MCP répond via SSE
check_server_health() {
    # Le endpoint SSE doit retourner "event: endpoint"
    # SSE est un stream qui ne se termine jamais, on utilise --max-time 1
    local response=$(curl -s --max-time 1 "$MCP_SSE_ENDPOINT" 2>/dev/null || true)
    if echo "$response" | head -n 1 | grep -q "event: endpoint"; then
        return 0
    else
        return 1
    fi
}

# Fonction pour vérifier si Docker est disponible
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker n'est pas installé ou pas dans PATH"
        log_error "Installation: https://docs.docker.com/get-docker/"
        return 1
    fi

    # Vérifier que le daemon Docker est actif
    if ! docker info &> /dev/null; then
        log_error "Docker daemon n'est pas actif"
        log_error "Lancer Docker Desktop ou démarrer le service Docker"
        return 1
    fi

    return 0
}

# 1. Vérifier Docker
log_info "Vérification de Docker..."
if ! check_docker; then
    exit 1
fi
log_info "✓ Docker disponible"

# 2. Vérifier si le serveur est déjà actif et fonctionne
log_info "Vérification du serveur MCP Yahoo Finance sur port $MCP_PORT..."

if check_server_health; then
    log_info "✓ Serveur MCP Yahoo Finance déjà actif et répond correctement"

    # Vérifier le conteneur Docker
    if docker ps --filter "name=${DOCKER_CONTAINER_NAME}" --format "{{.Names}}" | grep -q "${DOCKER_CONTAINER_NAME}"; then
        CONTAINER_STATUS=$(docker ps --filter "name=${DOCKER_CONTAINER_NAME}" --format "{{.Status}}")
        log_info "Conteneur Docker: ${DOCKER_CONTAINER_NAME} (${CONTAINER_STATUS})"
    fi

    exit 0
fi

# 3. Vérifier si le conteneur existe (même s'il est arrêté)
log_info "Recherche du conteneur Docker ${DOCKER_CONTAINER_NAME}..."

if docker ps -a --filter "name=${DOCKER_CONTAINER_NAME}" --format "{{.Names}}" | grep -q "${DOCKER_CONTAINER_NAME}"; then
    # Le conteneur existe
    CONTAINER_STATUS=$(docker ps -a --filter "name=${DOCKER_CONTAINER_NAME}" --format "{{.Status}}")
    log_info "Conteneur trouvé: ${DOCKER_CONTAINER_NAME} (${CONTAINER_STATUS})"

    # Vérifier si le conteneur est arrêté
    if docker ps --filter "name=${DOCKER_CONTAINER_NAME}" --format "{{.Names}}" | grep -q "${DOCKER_CONTAINER_NAME}"; then
        log_info "Conteneur déjà en cours d'exécution"
    else
        log_info "Redémarrage du conteneur..."
        if docker start "${DOCKER_CONTAINER_NAME}" > /dev/null; then
            log_info "✓ Conteneur redémarré"
        else
            log_error "Échec du redémarrage du conteneur"
            exit 1
        fi
    fi
else
    # Le conteneur n'existe pas, il faut le créer
    log_info "Conteneur non trouvé, création d'un nouveau conteneur..."

    # Vérifier que l'image Docker existe
    if ! docker images --format "{{.Repository}}" | grep -q "^${DOCKER_IMAGE_NAME}$"; then
        log_error "Image Docker ${DOCKER_IMAGE_NAME} non trouvée"
        log_error ""
        log_error "Pour construire l'image:"
        log_error "  cd ${YAHOO_FINANCE_MCP_PATH:-/path/to/yahoo-finance-mcp}"
        log_error "  docker build -t ${DOCKER_IMAGE_NAME} ."
        exit 1
    fi

    # Créer et démarrer le conteneur
    log_info "Création du conteneur ${DOCKER_CONTAINER_NAME}..."
    if docker run -d --name "${DOCKER_CONTAINER_NAME}" -p ${MCP_PORT}:${MCP_PORT} "${DOCKER_IMAGE_NAME}" > /dev/null; then
        log_info "✓ Conteneur créé et démarré"
    else
        log_error "Échec de la création du conteneur"
        exit 1
    fi
fi

# 4. Attendre que le serveur soit prêt (health check avec retry)
log_info "Attente de la disponibilité du serveur SSE (max ${MAX_WAIT_TIME}s)..."

ELAPSED=0
while [ $ELAPSED -lt $MAX_WAIT_TIME ]; do
    if check_server_health; then
        log_info "✓ Serveur MCP Yahoo Finance opérationnel après ${ELAPSED}s"
        log_info "Endpoint SSE: ${MCP_SSE_ENDPOINT}"
        exit 0
    fi

    # Vérifier que le conteneur est toujours actif
    if ! docker ps --filter "name=${DOCKER_CONTAINER_NAME}" --format "{{.Names}}" | grep -q "${DOCKER_CONTAINER_NAME}"; then
        log_error "Le conteneur ${DOCKER_CONTAINER_NAME} s'est arrêté"
        log_error "Logs du conteneur:"
        docker logs --tail 50 "${DOCKER_CONTAINER_NAME}" 2>&1
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
log_error "Logs du conteneur:"
docker logs --tail 50 "${DOCKER_CONTAINER_NAME}" 2>&1

exit 1
