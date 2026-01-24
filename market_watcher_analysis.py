#!/usr/bin/env python3
"""
Market Watcher PEA - Analyse complète des marchés
Analyse les titres de la watchlist et génère des signaux d'achat/vente
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class MarketWatcherPEA:
    def __init__(self, excel_file_path):
        self.excel_file_path = excel_file_path
        self.watchlist_df = None
        self.indicateurs_df = None
        self.positions_df = None
        self.signals = []

    def load_excel_data(self):
        """Charge les données du fichier Excel"""
        print(f"Chargement du fichier Excel: {self.excel_file_path}")

        try:
            # Charger les différentes feuilles
            xls = pd.ExcelFile(self.excel_file_path)
            print(f"Feuilles disponibles: {xls.sheet_names}")

            # Watchlist
            if 'Watchlist' in xls.sheet_names:
                self.watchlist_df = pd.read_excel(xls, sheet_name='Watchlist')
                print(f"\nWatchlist chargée: {len(self.watchlist_df)} titres")
                print(self.watchlist_df.head())

            # Indicateurs
            if 'Indicateurs' in xls.sheet_names:
                self.indicateurs_df = pd.read_excel(xls, sheet_name='Indicateurs')
                print(f"\nIndicateurs chargés: {len(self.indicateurs_df)} entrées")
                print(self.indicateurs_df.head())

            # Positions
            if 'Positions' in xls.sheet_names:
                self.positions_df = pd.read_excel(xls, sheet_name='Positions')
                print(f"\nPositions chargées: {len(self.positions_df)} positions")
                print(self.positions_df.head())

            return True
        except Exception as e:
            print(f"Erreur lors du chargement du fichier Excel: {e}")
            return False

    def get_active_tickers(self):
        """Récupère la liste des tickers actifs"""
        if self.watchlist_df is None:
            return []

        # Filtrer les tickers actifs
        active_tickers = []
        for _, row in self.watchlist_df.iterrows():
            if pd.notna(row.get('Ticker')) and row.get('Actif', False):
                active_tickers.append({
                    'ticker': row['Ticker'],
                    'nom': row.get('Nom', ''),
                    'marche': row.get('Marché', ''),
                    'secteur': row.get('Secteur', ''),
                    'pays': row.get('Pays', '')
                })

        print(f"\nTickers actifs trouvés: {len(active_tickers)}")
        for ticker in active_tickers:
            print(f"  - {ticker['ticker']}: {ticker['nom']}")

        return active_tickers

    def calculate_rsi(self, prices, period=14):
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

    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calcule le MACD"""
        if len(prices) < slow:
            return None, None, None

        exp1 = pd.Series(prices).ewm(span=fast, adjust=False).mean()
        exp2 = pd.Series(prices).ewm(span=slow, adjust=False).mean()
        macd_line = exp1 - exp2
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line

        return macd_line.iloc[-1], signal_line.iloc[-1], histogram.iloc[-1]

    def calculate_moving_averages(self, prices):
        """Calcule les moyennes mobiles MA20, MA50, MA200"""
        ma20 = np.mean(prices[-20:]) if len(prices) >= 20 else None
        ma50 = np.mean(prices[-50:]) if len(prices) >= 50 else None
        ma200 = np.mean(prices[-200:]) if len(prices) >= 200 else None

        return ma20, ma50, ma200

    def calculate_volume_ratio(self, volumes):
        """Calcule le ratio de volume par rapport à la moyenne 20 jours"""
        if len(volumes) < 20:
            return None

        avg_volume_20d = np.mean(volumes[-20:])
        current_volume = volumes[-1]

        return current_volume / avg_volume_20d if avg_volume_20d > 0 else None

    def generate_signal(self, ticker_data, indicators):
        """Génère un signal d'achat/vente/surveillance basé sur les indicateurs"""

        current_price = indicators.get('current_price')
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
        emoji = '🟢' if signal_type == 'buy' else '🔴' if signal_type == 'sell' else '🟡'
        summary = self._generate_summary(ticker_data, signal_type, indicators)

        return {
            'ticker': ticker_data['ticker'],
            'company_name': ticker_data['nom'],
            'signal_type': signal_type,
            'confidence_score': confidence_score,
            'emoji': emoji,
            'summary': summary,
            'key_points': key_points,
            'risks': risks if risks else ['Risques de marché standards'],
            'technical_details': indicators
        }

    def _generate_summary(self, ticker_data, signal_type, indicators):
        """Génère un résumé textuel du signal"""
        rsi = indicators.get('rsi', 0)
        volume_ratio = indicators.get('volume_ratio', 1)
        ma200 = indicators.get('ma200', 0)
        current_price = indicators.get('current_price', 0)

        if signal_type == 'buy':
            return f"{ticker_data['nom']} présente un signal d'achat avec RSI en zone de survente ({rsi:.1f}) et volume {((volume_ratio-1)*100):.0f}% au-dessus de la moyenne. Prix proche du support MA200 à {ma200:.2f}€ offre un point d'entrée attractif."
        elif signal_type == 'sell':
            return f"{ticker_data['nom']} montre des signes de surachat (RSI {rsi:.1f}) avec momentum baissier. Prise de bénéfices recommandée."
        else:
            return f"{ticker_data['nom']} en consolidation avec signaux mixtes. Surveillance requise pour confirmation."

    def export_results(self, output_file='market_analysis_results.json'):
        """Exporte les résultats de l'analyse"""
        output_path = os.path.join(os.path.dirname(self.excel_file_path), output_file)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'analysis_date': datetime.now().isoformat(),
                'signals': self.signals,
                'summary': {
                    'total_analyzed': len(self.signals),
                    'buy_signals': len([s for s in self.signals if s['signal_type'] == 'buy']),
                    'sell_signals': len([s for s in self.signals if s['signal_type'] == 'sell']),
                    'watch_signals': len([s for s in self.signals if s['signal_type'] == 'watch']),
                    'high_confidence': len([s for s in self.signals if s['confidence_score'] >= 60])
                }
            }, f, ensure_ascii=False, indent=2)

        print(f"\nRésultats exportés vers: {output_path}")
        return output_path

def main():
    # Chemin du fichier Excel
    excel_file = '/Users/yousrids/Documents/pea-tracker/PEA_Watchlist_Indicateurs.xlsx'

    # Créer l'instance de Market Watcher
    watcher = MarketWatcherPEA(excel_file)

    # Charger les données
    if not watcher.load_excel_data():
        print("Impossible de charger les données Excel")
        return

    # Récupérer les tickers actifs
    active_tickers = watcher.get_active_tickers()

    if not active_tickers:
        print("Aucun ticker actif trouvé dans la watchlist")
        return

    print(f"\n{'='*80}")
    print("ANALYSE PRÊTE À DÉMARRER")
    print(f"{'='*80}")
    print(f"Nombre de tickers à analyser: {len(active_tickers)}")
    print("\nPour continuer l'analyse avec les données de marché réelles,")
    print("nous allons utiliser Yahoo Finance MCP pour récupérer:")
    print("  - Prix historiques (1 an)")
    print("  - Volumes")
    print("  - Informations de marché")

    # Exporter la liste des tickers pour la suite
    tickers_list = [t['ticker'] for t in active_tickers]
    print(f"\nTickers à analyser: {', '.join(tickers_list)}")

    # Sauvegarder les tickers actifs
    with open('/Users/yousrids/Documents/pea-tracker/active_tickers.json', 'w') as f:
        json.dump(active_tickers, f, ensure_ascii=False, indent=2)

    return active_tickers

if __name__ == '__main__':
    main()
