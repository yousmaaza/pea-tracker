#!/bin/bash

# Script de test pour pip-mode
# Vérifie que toutes les fonctionnalités sont opérationnelles

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PIP_MODE_SCRIPT="$SCRIPT_DIR/pip-mode.sh"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Tests pip-mode"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Compteurs de tests
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Fonction de test
test_case() {
    local name="$1"
    local command="$2"
    local expected="$3"

    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    echo "Test $TESTS_TOTAL: $name"

    if eval "$command" | grep -q "$expected"; then
        echo "  ✓ PASS"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "  ✗ FAIL"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    echo ""
}

# Vérifier que le script existe
echo "Vérification préliminaire..."
if [ ! -f "$PIP_MODE_SCRIPT" ]; then
    echo "❌ Erreur: $PIP_MODE_SCRIPT non trouvé"
    exit 1
fi
echo "✓ Script trouvé: $PIP_MODE_SCRIPT"
echo ""

# Charger les fonctions pip-mode
source "$PIP_MODE_SCRIPT"

# Test 1: Mode status par défaut
test_case \
    "Affichage du status par défaut" \
    "pip_mode status" \
    "Configuration pip actuelle"

# Test 2: Basculement vers Nexus
test_case \
    "Activation du mode Nexus" \
    "pip_mode nexus" \
    "Mode Nexus activé"

# Test 3: Variables Nexus définies
echo "Test $((TESTS_TOTAL + 1)): Variables Nexus définies après activation"
TESTS_TOTAL=$((TESTS_TOTAL + 1))
pip_mode nexus > /dev/null 2>&1
if [ -n "$PIP_INDEX_URL" ] && [ -n "$PIP_TRUSTED_HOST" ]; then
    echo "  ✓ PASS"
    echo "    PIP_INDEX_URL=$PIP_INDEX_URL"
    echo "    PIP_TRUSTED_HOST=$PIP_TRUSTED_HOST"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAIL"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
echo ""

# Test 4: Basculement vers standard
test_case \
    "Activation du mode standard" \
    "pip_mode standard" \
    "Mode PyPI standard activé"

# Test 5: Variables supprimées en mode standard
echo "Test $((TESTS_TOTAL + 1)): Variables supprimées en mode standard"
TESTS_TOTAL=$((TESTS_TOTAL + 1))
pip_mode standard > /dev/null 2>&1
if [ -z "$PIP_INDEX_URL" ] && [ -z "$PIP_TRUSTED_HOST" ]; then
    echo "  ✓ PASS"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAIL (variables encore définies)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
echo ""

# Test 6: Mode invalide
echo "Test $((TESTS_TOTAL + 1)): Gestion mode invalide"
TESTS_TOTAL=$((TESTS_TOTAL + 1))
if pip_mode invalid 2>&1 | grep -q "Usage"; then
    echo "  ✓ PASS (message d'erreur affiché)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAIL"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
echo ""

# Test 7: Script exécutable
echo "Test $((TESTS_TOTAL + 1)): Script exécutable directement"
TESTS_TOTAL=$((TESTS_TOTAL + 1))
if [ -x "$PIP_MODE_SCRIPT" ]; then
    if "$PIP_MODE_SCRIPT" status 2>&1 | grep -q "Configuration pip"; then
        echo "  ✓ PASS"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "  ✗ FAIL (erreur d'exécution)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo "  ✗ FAIL (script non exécutable)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
echo ""

# Test 8: URLs Nexus valides
echo "Test $((TESTS_TOTAL + 1)): URLs Nexus valides"
TESTS_TOTAL=$((TESTS_TOTAL + 1))
pip_mode nexus > /dev/null 2>&1
if [[ "$PIP_INDEX_URL" == https://* ]] && [[ "$PIP_TRUSTED_HOST" != "" ]]; then
    echo "  ✓ PASS"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAIL (URL invalide)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
echo ""

# Résumé des tests
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Résumé des tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Tests exécutés : $TESTS_TOTAL"
echo "Tests réussis  : $TESTS_PASSED ✓"
echo "Tests échoués  : $TESTS_FAILED ✗"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo "🎉 Tous les tests sont passés avec succès !"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 0
else
    echo "❌ Certains tests ont échoué"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 1
fi
