#!/usr/bin/env python3
"""
Calcul des indicateurs techniques et génération des signaux
"""

import json
import numpy as np
import pandas as pd
from datetime import datetime

def calculate_rsi(prices, period=14):
    """Calcule le RSI (Relative Strength Index)"""
    if len(prices) < period + 1:
        return None

    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100. / (1. + rs)

    for i in range(period, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        rs = up / down if down != 0 else 0
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi[-1]

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calcule le MACD"""
    if len(prices) < slow:
        return None, None, None

    exp1 = pd.Series(prices).ewm(span=fast, adjust=False).mean()
    exp2 = pd.Series(prices).ewm(span=slow, adjust=False).mean()
    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line

    return macd_line.iloc[-1], signal_line.iloc[-1], histogram.iloc[-1]

def calculate_moving_averages(prices):
    """Calcule les moyennes mobiles MA20, MA50, MA200"""
    ma20 = np.mean(prices[-20:]) if len(prices) >= 20 else None
    ma50 = np.mean(prices[-50:]) if len(prices) >= 50 else None
    ma200 = np.mean(prices[-200:]) if len(prices) >= 200 else None

    return ma20, ma50, ma200

def calculate_volume_ratio(volumes):
    """Calcule le ratio de volume par rapport à la moyenne 20 jours"""
    if len(volumes) < 20:
        return None

    avg_volume_20d = np.mean(volumes[-20:])
    current_volume = volumes[-1]

    return current_volume / avg_volume_20d if avg_volume_20d > 0 else None

def generate_signal(ticker, company_name, current_price, indicators):
    """Génère un signal d'achat/vente/surveillance"""

    rsi = indicators.get('rsi')
    macd = indicators.get('macd')
    macd_signal = indicators.get('macd_signal')
    macd_histogram = indicators.get('macd_histogram')
    ma20 = indicators.get('ma20')
    ma50 = indicators.get('ma50')
    ma200 = indicators.get('ma200')
    volume_ratio = indicators.get('volume_ratio')

    signal_type = 'neutral'
    confidence_score = 0
    key_points = []
    risks = []

    # Vérifier si nous avons suffisamment de données
    if None in [rsi, macd, macd_signal, ma20, ma200]:
        return {
            'ticker': ticker,
            'company_name': company_name,
            'signal_type': 'insufficient_data',
            'confidence_score': 0,
            'summary': 'Données insuffisantes pour générer un signal'
        }

    # LOGIQUE DE SIGNAL BUY
    buy_signals = 0

    # RSI oversold
    if rsi < 30:
        buy_signals += 1
        key_points.append(f"RSI à {rsi:.1f} indique conditions de survente avec potentiel de rebond")
    elif rsi < 40:
        key_points.append(f"RSI à {rsi:.1f} approche la zone de survente")

    # MACD bullish crossover
    if macd > macd_signal and macd_histogram > 0:
        buy_signals += 1
        key_points.append("MACD montre des signes précoces de retournement haussier")

    # Prix au-dessus de MA200
    if current_price > ma200:
        buy_signals += 1
        key_points.append(f"Tendance long terme intacte (prix > MA200 à {ma200:.2f}€)")
    else:
        risks.append("Prix sous MA200 indique tendance baissière long terme")

    # Volume élevé
    if volume_ratio and volume_ratio > 1.3:
        buy_signals += 1
        key_points.append(f"Volume en hausse (+{(volume_ratio-1)*100:.0f}% vs moyenne) confirme l'intérêt")

    # LOGIQUE DE SIGNAL SELL
    sell_signals = 0

    # RSI overbought
    if rsi > 70:
        sell_signals += 1
        key_points.append(f"RSI à {rsi:.1f} indique conditions de surachat")
    elif rsi > 60:
        key_points.append(f"RSI à {rsi:.1f} approche la zone de surachat")

    # MACD bearish crossover
    if macd < macd_signal and macd_histogram < 0:
        sell_signals += 1
        key_points.append("MACD montre un momentum baissier")

    # Prix cassure MA200 vers le bas
    if current_price < ma200 and ma20 < ma50:
        sell_signals += 1
        risks.append(f"Cassure baissière de la MA200 (support à {ma200:.2f}€)")

    # DÉTERMINATION DU SIGNAL FINAL
    if buy_signals >= 3:
        signal_type = 'buy'
        confidence_score = min(100, 60 + (buy_signals - 3) * 10 + (20 if volume_ratio and volume_ratio > 1.5 else 0))
    elif sell_signals >= 3:
        signal_type = 'sell'
        confidence_score = min(100, 60 + (sell_signals - 3) * 10)
    elif buy_signals >= 2 or (30 <= rsi <= 40):
        signal_type = 'watch'
        confidence_score = 50 + buy_signals * 5
        key_points.append("Surveiller pour confirmation du signal")
    elif sell_signals >= 2 or (60 <= rsi <= 70):
        signal_type = 'watch'
        confidence_score = 50 + sell_signals * 5
        key_points.append("Surveiller pour confirmation de pression vendeuse")

    # Ajuster le score si prix sous MA20
    if current_price < ma20:
        risks.append(f"Tendance court terme baissière (prix < MA20 à {ma20:.2f}€)")
        confidence_score = max(0, confidence_score - 10)

    # Générer le résumé
    if signal_type == 'buy':
        summary = f"{company_name} présente un signal d'achat avec RSI en zone de survente ({rsi:.1f}) et volume {((volume_ratio-1)*100):.0f}% au-dessus de la moyenne. Prix proche du support MA200 à {ma200:.2f}€ offre un point d'entrée attractif."
    elif signal_type == 'sell':
        summary = f"{company_name} montre des signes de surachat (RSI {rsi:.1f}) avec momentum baissier. Prise de bénéfices recommandée."
    else:
        summary = f"{company_name} en consolidation avec signaux mixtes. Surveillance requise pour confirmation."

    return {
        'ticker': ticker,
        'company_name': company_name,
        'signal_type': signal_type,
        'confidence_score': confidence_score,
        'summary': summary,
        'key_points': key_points,
        'risks': risks if risks else ['Risques de marché standards'],
        'technical_details': {
            'current_price': current_price,
            'rsi': rsi,
            'macd': macd,
            'macd_signal': macd_signal,
            'macd_histogram': macd_histogram,
            'ma20': ma20,
            'ma50': ma50,
            'ma200': ma200,
            'volume_ratio': volume_ratio
        }
    }

# Données des 5 actions (à remplir avec les données collectées)
stocks = {
    'BNP.PA': {
        'name': 'BNP Paribas',
        'current_price': 64.42,
        'historical_data': None  # Sera chargé depuis les fichiers JSON
    },
    'MC.PA': {
        'name': 'LVMH',
        'current_price': 753.50,
        'historical_data': None
    },
    'OR.PA': {
        'name': 'L\'Oréal',
        'current_price': 418.80,
        'historical_data': None
    },
    'AI.PA': {
        'name': 'Air Liquide',
        'current_price': 188.30,
        'historical_data': None
    },
    'SAF.PA': {
        'name': 'Safran',
        'current_price': 224.80,
        'historical_data': None
    }
}

# Charger les données historiques depuis les fichiers JSON si disponibles
# (Cette partie devra être adaptée selon le format des données collectées)

print("Script de calcul des indicateurs techniques prêt.")
print("Traitement des 5 actions françaises principales...")

# Le traitement sera effectué directement dans Claude avec les données MCP
