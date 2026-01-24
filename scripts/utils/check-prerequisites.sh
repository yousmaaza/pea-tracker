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
    CLAUDE_VERSION=$(claude-code --version 2>&1 | head -n1 || echo "version inconnue")
    log_info "✓ claude-code installé ($CLAUDE_VERSION)"
else
    log_error "✗ claude-code non installé"
    log_error "  Installation: npm install -g @anthropic-ai/claude-code"
    HAS_ERRORS=1
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

# 4. Vérifier MCP Yahoo Finance (optionnel au démarrage, sera lancé par script)
log_info "Vérification du serveur MCP Yahoo Finance..."
if [ -n "${YAHOO_FINANCE_MCP_PATH:-}" ]; then
    if [ -d "$YAHOO_FINANCE_MCP_PATH" ]; then
        log_info "✓ Chemin MCP Yahoo Finance configuré: $YAHOO_FINANCE_MCP_PATH"

        # Vérifier si server.py existe
        if [ -f "$YAHOO_FINANCE_MCP_PATH/server.py" ]; then
            log_info "✓ server.py trouvé"
        else
            log_warn "⚠ server.py non trouvé dans $YAHOO_FINANCE_MCP_PATH"
        fi
    else
        log_warn "⚠ Répertoire MCP Yahoo Finance non trouvé: $YAHOO_FINANCE_MCP_PATH"
    fi
else
    log_warn "⚠ YAHOO_FINANCE_MCP_PATH non défini (sera démarré par défaut)"
fi

# Vérifier si le serveur est déjà actif
if curl -s --max-time 2 http://localhost:8000/health &> /dev/null; then
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
