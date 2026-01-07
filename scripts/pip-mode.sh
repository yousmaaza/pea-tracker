#!/bin/bash

# Configuration pip - Basculement entre PyPI standard et Nexus

# Configuration Nexus
export NEXUS_INDEX="https://nexus-ext.cnt.zone.local/repository/cnt-pypi-public/simple"
export NEXUS_HOST="nexus-ext.cnt.zone.local"

# Fonction pour basculer le mode pip
pip_mode() {
    local mode="${1:-status}"

    case "$mode" in
        nexus)
            export PIP_INDEX_URL="$NEXUS_INDEX"
            export PIP_TRUSTED_HOST="$NEXUS_HOST"
            echo "✓ Mode Nexus activé"
            echo "  Index URL: $PIP_INDEX_URL"
            echo "  Trusted Host: $PIP_TRUSTED_HOST"
            ;;
        standard)
            unset PIP_INDEX_URL
            unset PIP_TRUSTED_HOST
            echo "✓ Mode PyPI standard activé"
            echo "  Les variables PIP_INDEX_URL et PIP_TRUSTED_HOST ont été supprimées"
            ;;
        status)
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "📦 Configuration pip actuelle"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            if [ -n "$PIP_INDEX_URL" ]; then
                echo "Mode: Nexus"
                echo "PIP_INDEX_URL: $PIP_INDEX_URL"
                echo "PIP_TRUSTED_HOST: ${PIP_TRUSTED_HOST:-'Non défini'}"
            else
                echo "Mode: PyPI standard"
                echo "PIP_INDEX_URL: Non défini (utilise PyPI par défaut)"
                echo "PIP_TRUSTED_HOST: Non défini"
            fi
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            ;;
        *)
            echo "❌ Usage: pip-mode {nexus|standard|status}"
            echo ""
            echo "Modes disponibles:"
            echo "  nexus    - Utiliser le dépôt Nexus interne"
            echo "  standard - Utiliser PyPI standard"
            echo "  status   - Afficher la configuration actuelle"
            return 1
            ;;
    esac
}

# Si le script est exécuté directement (pas sourcé), appeler la fonction
if [ "${BASH_SOURCE[0]}" -ef "$0" ]; then
    pip_mode "$@"
fi
