#!/usr/bin/env python3
"""
Traitement direct des données de marché pour générer les signaux
"""

import numpy as np
import pandas as pd
from datetime import datetime
import json

# Données historiques collectées via Yahoo Finance MCP
# Note: Ces données seront traitées directement

def process_ticker_data(ticker, company_name, historical_prices, historical_volumes, current_price):
    """
    Traite les données d'un ticker et génère un signal

    Args:
        ticker: Symbole du ticker (ex: 'BNP.PA')
        company_name: Nom de l'entreprise
        historical_prices: Liste des prix de clôture (plus ancien au plus récent)
        historical_volumes: Liste des volumes
        current_price: Prix actuel
    """

    # Convertir en arrays numpy
    prices = np.array(historical_prices)
    volumes = np.array(historical_volumes)

    # Calcul RSI (14 périodes)
    def calc_rsi(prices, period=14):
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

    # Calcul MACD
    def calc_macd(prices, fast=12, slow=26, signal=9):
        if len(prices) < slow:
            return None, None, None
        exp1 = pd.Series(prices).ewm(span=fast, adjust=False).mean()
        exp2 = pd.Series(prices).ewm(span=slow, adjust=False).mean()
        macd_line = exp1 - exp2
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line.iloc[-1], signal_line.iloc[-1], histogram.iloc[-1]

    # Calcul moyennes mobiles
    ma20 = np.mean(prices[-20:]) if len(prices) >= 20 else None
    ma50 = np.mean(prices[-50:]) if len(prices) >= 50 else None
    ma200 = np.mean(prices[-200:]) if len(prices) >= 200 else None

    # Calcul volume ratio
    avg_volume_20d = np.mean(volumes[-20:]) if len(volumes) >= 20 else None
    volume_ratio = volumes[-1] / avg_volume_20d if avg_volume_20d and avg_volume_20d > 0 else None

    # Calcul RSI et MACD
    rsi = calc_rsi(prices)
    macd, macd_signal, macd_histogram = calc_macd(prices)

    # Génération du signal
    signal_type = 'neutral'
    confidence_score = 0
    key_points = []
    risks = []

    if None in [rsi, macd, macd_signal, ma20, ma200]:
        return {
            'ticker': ticker,
            'company_name': company_name,
            'signal_type': 'insufficient_data',
            'confidence_score': 0,
            'summary': 'Données insuffisantes'
        }

    # Compteurs de signaux
    buy_signals = 0
    sell_signals = 0

    # RSI oversold
    if rsi < 30:
        buy_signals += 1
        key_points.append(f"RSI à {rsi:.1f} indique conditions de survente avec potentiel de rebond")
    elif rsi < 40:
        key_points.append(f"RSI à {rsi:.1f} approche la zone de survente")

    # MACD bullish
    if macd > macd_signal and macd_histogram > 0:
        buy_signals += 1
        key_points.append("MACD montre des signes précoces de retournement haussier")

    # Prix > MA200
    if current_price > ma200:
        buy_signals += 1
        key_points.append(f"Tendance long terme intacte (prix > MA200 à {ma200:.2f}€)")
    else:
        risks.append("Prix sous MA200 indique tendance baissière long terme")

    # Volume élevé
    if volume_ratio and volume_ratio > 1.3:
        buy_signals += 1
        key_points.append(f"Volume en hausse (+{(volume_ratio-1)*100:.0f}% vs moyenne) confirme l'intérêt")

    # RSI overbought
    if rsi > 70:
        sell_signals += 1
        key_points.append(f"RSI à {rsi:.1f} indique conditions de surachat")
    elif rsi > 60:
        key_points.append(f"RSI à {rsi:.1f} approche la zone de surachat")

    # MACD bearish
    if macd < macd_signal and macd_histogram < 0:
        sell_signals += 1
        key_points.append("MACD montre un momentum baissier")

    # Cassure MA200
    if current_price < ma200 and ma20 < ma50:
        sell_signals += 1
        risks.append(f"Cassure baissière de la MA200 (support à {ma200:.2f}€)")

    # Détermination signal final
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

    # Ajustement si prix < MA20
    if current_price < ma20:
        risks.append(f"Tendance court terme baissière (prix < MA20 à {ma20:.2f}€)")
        confidence_score = max(0, confidence_score - 10)

    # Générer résumé
    if signal_type == 'buy':
        summary = f"{company_name} présente un signal d'achat avec RSI en zone de survente ({rsi:.1f}). Prix proche du support MA200 à {ma200:.2f}€ offre un point d'entrée attractif."
    elif signal_type == 'sell':
        summary = f"{company_name} montre des signes de surachat (RSI {rsi:.1f}) avec momentum baissier. Prise de bénéfices recommandée."
    else:
        summary = f"{company_name} en consolidation avec signaux mixtes. Surveillance requise pour confirmation."

    emoji = '🟢' if signal_type == 'buy' else '🔴' if signal_type == 'sell' else '🟡'

    return {
        'ticker': ticker,
        'company_name': company_name,
        'signal_type': signal_type,
        'confidence_score': confidence_score,
        'emoji': emoji,
        'summary': summary,
        'key_points': key_points,
        'risks': risks if risks else ['Risques de marché standards'],
        'technical_details': {
            'current_price': current_price,
            'rsi': round(rsi, 2) if rsi else None,
            'macd': round(macd, 2) if macd else None,
            'macd_signal': round(macd_signal, 2) if macd_signal else None,
            'macd_histogram': round(macd_histogram, 2) if macd_histogram else None,
            'ma20': round(ma20, 2) if ma20 else None,
            'ma50': round(ma50, 2) if ma50 else None,
            'ma200': round(ma200, 2) if ma200 else None,
            'volume_ratio': round(volume_ratio, 2) if volume_ratio else None
        }
    }

if __name__ == '__main__':
    print("Module de traitement des données de marché chargé.")
    print("Utilisez process_ticker_data() pour analyser un ticker.")
