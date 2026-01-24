#!/bin/bash
#
# check-prerequisites.sh
# Vérifie tous les prérequis avant l'exécution de Market Watcher
#
# Exit codes:
#   0 - Tous les prérequis sont satisfaits
#   1 - Erreur critique (prérequis manquant)
#   2 - Avertissement (prérequis optionnel manquant)

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

# Flag pour tracking des erreurs
HAS_ERRORS=0

# 1. Vérifier Python 3.11+
log_info "Vérification de Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 11 ]; then
        log_info "✓ Python $PYTHON_VERSION détecté"
    else
        log_error "✗ Python 3.11+ requis, version $PYTHON_VERSION détectée"
        HAS_ERRORS=1
    fi
else
    log_error "✗ Python 3 non trouvé"
    HAS_ERRORS=1
fi

# 2. Vérifier claude-code
log_info "Vérification de claude-code..."
if command -v claude-code &> /dev/null; then
    log_info "✓ claude-code trouvé dans PATH"
    # Note: --version peut bloquer dans certains environnements, on skip cette vérification
else
    # Dans l'environnement Claude Code, le binaire peut ne pas être dans PATH
    # mais l'environnement fonctionne quand même via l'agent
    log_warn "⚠ claude-code non trouvé dans PATH (peut être OK si exécuté via l'environnement Claude)"
fi

# 3. Vérifier ANTHROPIC_API_KEY
log_info "Vérification de ANTHROPIC_API_KEY..."
if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
    KEY_PREFIX=$(echo "$ANTHROPIC_API_KEY" | cut -c1-10)
    log_info "✓ ANTHROPIC_API_KEY configurée ($KEY_PREFIX...)"
else
    log_error "✗ ANTHROPIC_API_KEY non définie"
    log_error "  Définir dans config/.env ou dans l'environnement"
    HAS_ERRORS=1
fi

# 4. Vérifier Docker (pour MCP Yahoo Finance)
log_info "Vérification de Docker..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version 2>&1 | head -n1)
    log_info "✓ Docker installé ($DOCKER_VERSION)"

    # Vérifier que le daemon Docker est actif
    if docker info &> /dev/null; then
        log_info "✓ Docker daemon actif"

        # Vérifier si l'image Docker MCP Yahoo Finance existe
        if docker images --format "{{.Repository}}" | grep -q "^yahoo-finance-mcp$"; then
            log_info "✓ Image Docker yahoo-finance-mcp trouvée"
        else
            log_warn "⚠ Image Docker yahoo-finance-mcp non trouvée"
            log_warn "  Construire l'image: cd \$YAHOO_FINANCE_MCP_PATH && docker build -t yahoo-finance-mcp ."
        fi

        # Vérifier si le conteneur existe
        if docker ps -a --filter "name=yfinance-mcp" --format "{{.Names}}" | grep -q "yfinance-mcp"; then
            CONTAINER_STATUS=$(docker ps -a --filter "name=yfinance-mcp" --format "{{.Status}}" | head -1)
            log_info "✓ Conteneur Docker yfinance-mcp trouvé ($CONTAINER_STATUS)"
        else
            log_info "ℹ Conteneur Docker yfinance-mcp non créé (sera créé automatiquement)"
        fi
    else
        log_warn "⚠ Docker daemon non actif"
        log_warn "  Lancer Docker Desktop pour démarrer le daemon"
    fi
else
    log_error "✗ Docker non installé"
    log_error "  Installation: https://docs.docker.com/get-docker/"
    HAS_ERRORS=1
fi

# Vérifier si le serveur MCP est déjà actif
SSE_RESPONSE=$(curl -s --max-time 1 http://localhost:8000/sse 2>/dev/null || true)
if echo "$SSE_RESPONSE" | head -n 1 | grep -q "event: endpoint"; then
    log_info "✓ Serveur MCP Yahoo Finance déjà actif sur port 8000"
else
    log_info "ℹ Serveur MCP Yahoo Finance non actif (sera démarré si nécessaire)"
fi

# 5. Vérifier accès Google Drive (via test MCP rapide - optionnel)
log_info "Vérification de l'accès Google Drive MCP..."
# Note: Ce test est optionnel car il nécessite que les serveurs MCP soient actifs
# On le skip pour les vérifications de base
log_info "ℹ Accès Google Drive sera vérifié lors de l'exécution de l'agent"

# 6. Vérifier accès Gmail MCP (optionnel)
log_info "Vérification de l'accès Gmail MCP..."
log_info "ℹ Accès Gmail sera vérifié lors de l'exécution de l'agent"

# 7. Vérifier structure des dossiers
log_info "Vérification de la structure de dossiers..."
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

REQUIRED_DIRS=("logs" "logs/market-watcher" "scripts" "scripts/utils" "config")
for DIR in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$PROJECT_ROOT/$DIR" ]; then
        log_info "✓ Dossier $DIR existe"
    else
        log_warn "⚠ Dossier $DIR manquant (sera créé automatiquement)"
    fi
done

# 8. Vérifier fichier .env
log_info "Vérification du fichier de configuration..."
if [ -f "$PROJECT_ROOT/config/.env" ]; then
    log_info "✓ Fichier config/.env trouvé"
else
    log_warn "⚠ Fichier config/.env non trouvé"
    log_warn "  Copier config/.env.template vers config/.env et configurer"
fi

# Résumé
echo ""
echo "═══════════════════════════════════════"
if [ $HAS_ERRORS -eq 0 ]; then
    log_info "✅ Tous les prérequis critiques sont satisfaits"
    echo "═══════════════════════════════════════"
    exit 0
else
    log_error "❌ Des prérequis critiques sont manquants"
    echo "═══════════════════════════════════════"
    exit 1
fi
