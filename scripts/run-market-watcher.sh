#!/bin/bash
#
# run-market-watcher.sh
# Wrapper principal pour l'exécution automatisée de l'agent Market Watcher
#
# Ce script:
#   1. Vérifie les prérequis
#   2. Démarre le serveur MCP Yahoo Finance si nécessaire
#   3. Active l'environnement Python
#   4. Exécute l'agent Market Watcher via claude-code
#   5. Gère les erreurs et envoie des notifications
#   6. Nettoie les ressources (arrêt MCP si démarré par le script)
#
# Exit codes:
#   0 - Succès
#   1 - Échec

set -euo pipefail

# Configuration des chemins
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_ROOT/logs/market-watcher"
LOG_FILE="$LOG_DIR/market-watcher-$(date +%Y%m%d-%H%M%S).log"

# Charger les variables d'environnement depuis .env
if [ -f "$PROJECT_ROOT/config/.env" ]; then
    set -a  # Activer l'export automatique
    source "$PROJECT_ROOT/config/.env"
    set +a  # Désactiver l'export automatique
fi

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction de logging
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    case "$level" in
        INFO)
            echo -e "${GREEN}[$timestamp] [INFO]${NC} $message" | tee -a "$LOG_FILE"
            ;;
        WARN)
            echo -e "${YELLOW}[$timestamp] [WARN]${NC} $message" | tee -a "$LOG_FILE"
            ;;
        ERROR)
            echo -e "${RED}[$timestamp] [ERROR]${NC} $message" | tee -a "$LOG_FILE"
            ;;
        DEBUG)
            if [ "${LOG_LEVEL:-info}" == "debug" ]; then
                echo -e "${BLUE}[$timestamp] [DEBUG]${NC} $message" | tee -a "$LOG_FILE"
            fi
            ;;
        *)
            echo "[$timestamp] $message" | tee -a "$LOG_FILE"
            ;;
    esac
}

# Créer le dossier de logs s'il n'existe pas
mkdir -p "$LOG_DIR"

log INFO "═══════════════════════════════════════════════════════════════"
log INFO "🚀 Démarrage de Market Watcher"
log INFO "═══════════════════════════════════════════════════════════════"
log INFO "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
log INFO "Hostname: $(hostname)"
log INFO "Working directory: $PROJECT_ROOT"
log INFO "Log file: $LOG_FILE"
log INFO ""

# Flag pour tracker si on a démarré le MCP (pour le cleanup)
MCP_STARTED_BY_SCRIPT=false

# Fonction de cleanup appelée en cas de sortie (succès ou erreur)
cleanup() {
    local exit_code=$?

    log INFO ""
    log INFO "─────────────────────────────────────────────────────────────"
    log INFO "🧹 Cleanup en cours..."

    # Arrêter MCP si on l'a démarré
    if [ "$MCP_STARTED_BY_SCRIPT" = true ]; then
        log INFO "Arrêt du serveur MCP Yahoo Finance..."
        if "$SCRIPT_DIR/utils/stop-yfinance-mcp.sh" >> "$LOG_FILE" 2>&1; then
            log INFO "✓ MCP arrêté proprement"
        else
            log WARN "⚠ Problème lors de l'arrêt du MCP (non bloquant)"
        fi
    fi

    log INFO "─────────────────────────────────────────────────────────────"
    log INFO "🏁 Terminé avec code de sortie: $exit_code"
    log INFO "═══════════════════════════════════════════════════════════════"

    exit $exit_code
}

# Fonction de gestion d'erreur
handle_error() {
    local error_message="$1"
    local send_notification="${2:-true}"

    log ERROR "$error_message"

    if [ "$send_notification" = true ]; then
        log INFO "Envoi d'une notification d'erreur..."
        "$SCRIPT_DIR/utils/send-error-notification.sh" "$error_message" "$LOG_FILE" >> "$LOG_FILE" 2>&1 || true
    fi

    cleanup
    exit 1
}

# Configurer trap pour cleanup automatique
trap cleanup EXIT

# ═══════════════════════════════════════════════════════════════
# ÉTAPE 1: Vérification des prérequis
# ═══════════════════════════════════════════════════════════════
log INFO "📋 ÉTAPE 1/5: Vérification des prérequis"
log INFO ""

if ! "$SCRIPT_DIR/utils/check-prerequisites.sh" >> "$LOG_FILE" 2>&1; then
    handle_error "Les prérequis ne sont pas satisfaits. Consultez le log pour plus de détails."
fi

log INFO "✅ Tous les prérequis sont satisfaits"
log INFO ""

# ═══════════════════════════════════════════════════════════════
# ÉTAPE 2: Démarrage du serveur MCP Yahoo Finance
# ═══════════════════════════════════════════════════════════════
log INFO "🔧 ÉTAPE 2/5: Démarrage du serveur MCP Yahoo Finance"
log INFO ""

if ! "$SCRIPT_DIR/utils/start-yfinance-mcp.sh" >> "$LOG_FILE" 2>&1; then
    handle_error "Impossible de démarrer le serveur MCP Yahoo Finance"
fi

MCP_STARTED_BY_SCRIPT=true
log INFO "✅ Serveur MCP Yahoo Finance opérationnel"
log INFO ""

# ═══════════════════════════════════════════════════════════════
# ÉTAPE 3: Activation de l'environnement Python
# ═══════════════════════════════════════════════════════════════
log INFO "🐍 ÉTAPE 3/5: Activation de l'environnement Python"
log INFO ""

if [ -d "$PROJECT_ROOT/venv" ]; then
    log INFO "Activation du venv: $PROJECT_ROOT/venv"
    source "$PROJECT_ROOT/venv/bin/activate"
    PYTHON_VERSION=$(python3 --version)
    log INFO "✓ Python activé: $PYTHON_VERSION"
elif [ -d "$PROJECT_ROOT/venv_market_watcher" ]; then
    log INFO "Activation du venv: $PROJECT_ROOT/venv_market_watcher"
    source "$PROJECT_ROOT/venv_market_watcher/bin/activate"
    PYTHON_VERSION=$(python3 --version)
    log INFO "✓ Python activé: $PYTHON_VERSION"
else
    log WARN "⚠ Aucun environnement virtuel Python trouvé"
    log WARN "Utilisation de Python système"
fi

log INFO ""

# ═══════════════════════════════════════════════════════════════
# ÉTAPE 4: Exécution de l'agent Market Watcher
# ═══════════════════════════════════════════════════════════════
log INFO "🤖 ÉTAPE 4/5: Exécution de l'agent Market Watcher"
log INFO ""

log INFO "Commande: claude-code agent run market-watcher-pea"
log INFO "Début de l'exécution: $(date '+%H:%M:%S')"
log INFO ""

# Exécuter l'agent et capturer la sortie
START_TIME=$(date +%s)

if claude-code agent run market-watcher-pea >> "$LOG_FILE" 2>&1; then
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))

    log INFO ""
    log INFO "✅ Agent Market Watcher exécuté avec succès"
    log INFO "Durée d'exécution: ${DURATION}s"
else
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))

    log ERROR ""
    log ERROR "❌ Erreur lors de l'exécution de l'agent"
    log ERROR "Durée avant échec: ${DURATION}s"
    handle_error "L'agent Market Watcher a échoué après ${DURATION}s"
fi

log INFO ""

# ═══════════════════════════════════════════════════════════════
# ÉTAPE 5: Vérification post-exécution
# ═══════════════════════════════════════════════════════════════
log INFO "✓ ÉTAPE 5/5: Vérification post-exécution"
log INFO ""

# Vérifier que des fichiers ont été créés (optionnel)
# Par exemple, vérifier qu'un rapport a été généré dans Google Drive
# Note: Ceci nécessiterait une vérification via MCP - skip pour le moment

log INFO "✓ Exécution complète sans erreur"
log INFO ""

# Le cleanup sera appelé automatiquement par le trap EXIT
exit 0
