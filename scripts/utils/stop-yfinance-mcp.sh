#!/bin/bash
#
# stop-yfinance-mcp.sh
# Arrête proprement le serveur MCP Yahoo Finance (Docker)
#
# Exit codes:
#   0 - Serveur arrêté avec succès ou déjà arrêté
#   1 - Erreur lors de l'arrêt

set -euo pipefail

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DOCKER_CONTAINER_NAME="yfinance-mcp"
STOP_TIMEOUT=10  # Timeout pour docker stop (secondes)

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

# Vérifier si Docker est disponible
if ! command -v docker &> /dev/null; then
    log_warn "Docker n'est pas installé, rien à arrêter"
    exit 0
fi

# Vérifier si le daemon Docker est actif
if ! docker info &> /dev/null; then
    log_warn "Docker daemon n'est pas actif, rien à arrêter"
    exit 0
fi

# Vérifier si le conteneur existe
log_info "Recherche du conteneur ${DOCKER_CONTAINER_NAME}..."

if ! docker ps -a --filter "name=${DOCKER_CONTAINER_NAME}" --format "{{.Names}}" | grep -q "${DOCKER_CONTAINER_NAME}"; then
    log_info "Conteneur ${DOCKER_CONTAINER_NAME} non trouvé (déjà supprimé ou jamais créé)"
    exit 0
fi

# Vérifier si le conteneur est en cours d'exécution
if docker ps --filter "name=${DOCKER_CONTAINER_NAME}" --format "{{.Names}}" | grep -q "${DOCKER_CONTAINER_NAME}"; then
    log_info "Arrêt du conteneur ${DOCKER_CONTAINER_NAME}..."

    # Arrêter le conteneur avec timeout
    if docker stop --time=${STOP_TIMEOUT} "${DOCKER_CONTAINER_NAME}" > /dev/null 2>&1; then
        log_info "✓ Conteneur arrêté proprement"
    else
        log_error "Échec de l'arrêt du conteneur"
        log_error "Tentative de force kill..."

        if docker kill "${DOCKER_CONTAINER_NAME}" > /dev/null 2>&1; then
            log_warn "⚠ Conteneur tué (force kill)"
        else
            log_error "Impossible d'arrêter le conteneur"
            exit 1
        fi
    fi
else
    log_info "Conteneur ${DOCKER_CONTAINER_NAME} déjà arrêté"
fi

# Note: On ne supprime PAS le conteneur pour pouvoir le redémarrer facilement
# Si vous voulez le supprimer : docker rm ${DOCKER_CONTAINER_NAME}

log_info "✓ Arrêt terminé"
exit 0
