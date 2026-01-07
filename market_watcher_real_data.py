#!/usr/bin/env python3
"""
Market Watcher PEA - Real Market Data Analysis
Uses Yahoo Finance data via MCP to perform technical analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import sys

# File paths
EXCEL_FILE = '/Users/yousrimaazaoui/Documents/projets/test-debile/claude-project/PEA_Watchlist_Indicateurs.xlsx'
YFINANCE_DATA_DIR = '/Users/yousrimaazaoui/Documents/projets/test-debile/claude-project/yfinance_data'
OUTPUT_JSON = '/Users/yousrimaazaoui/Documents/projets/test-debile/claude-project/market_analysis_real_results.json'

def parse_watchlist(excel_file):
    """Parse the Excel watchlist and return active tickers"""
    try:
        watchlist_df = pd.read_excel(excel_file, sheet_name='Watchlist')
        indicateurs_df = pd.read_excel(excel_file, sheet_name='Indicateurs')

        active_tickers = watchlist_df[watchlist_df['Actif'] == True].copy()

        print(f"Loaded {len(active_tickers)} active tickers from watchlist")
        return active_tickers, indicateurs_df
    except Exception as e:
        print(f"ERROR parsing Excel file: {e}")
        sys.exit(1)

def load_yahoo_finance_data(ticker):
    """Load historical price data from Yahoo Finance JSON files"""
    import os

    # Check if data file exists
    data_file = f"{YFINANCE_DATA_DIR}/{ticker}_historical.json"

    if not os.path.exists(data_file):
        print(f"  WARNING: No data file found for {ticker}")
        return None

    try:
        with open(data_file, 'r') as f:
            data = json.load(f)

        # Extract price and volume arrays
        if 'prices' not in data or len(data['prices']) == 0:
            print(f"  WARNING: No price data in file for {ticker}")
            return None

        prices = data['prices']
        volumes = data.get('volumes', [100000] * len(prices))

        return {
            'prices': np.array(prices),
            'volumes': np.array(volumes),
            'current_price': prices[-1],
            'current_volume': volumes[-1]
        }

    except Exception as e:
        print(f"  ERROR loading data for {ticker}: {e}")
        return None

def calculate_rsi(prices, periods=14):
    """Calculate Relative Strength Index"""
    if len(prices) < periods + 1:
        return None

    deltas = np.diff(prices)
    gain = np.where(deltas > 0, deltas, 0)
    loss = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.mean(gain[-periods:])
    avg_loss = np.mean(loss[-periods:])

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def calculate_ema(prices, periods):
    """Calculate Exponential Moving Average"""
    if len(prices) < periods:
        return None

    prices = np.array(prices)
    multiplier = 2 / (periods + 1)

    ema = np.zeros(len(prices))
    ema[periods-1] = np.mean(prices[:periods])

    for i in range(periods, len(prices)):
        ema[i] = (prices[i] - ema[i-1]) * multiplier + ema[i-1]

    return ema[-1]

def calculate_macd(prices):
    """Calculate MACD (12, 26, 9)"""
    if len(prices) < 26:
        return None, None, None

    prices = np.array(prices)

    # Calculate EMAs
    ema12 = calculate_ema(prices, 12)
    ema26 = calculate_ema(prices, 26)

    if ema12 is None or ema26 is None:
        return None, None, None

    macd_line = ema12 - ema26

    # Calculate MACD values for signal line
    macd_values = []
    for i in range(26, len(prices)+1):
        e12 = calculate_ema(prices[:i], 12)
        e26 = calculate_ema(prices[:i], 26)
        if e12 and e26:
            macd_values.append(e12 - e26)

    if len(macd_values) < 9:
        signal_line = macd_line
    else:
        signal_line = calculate_ema(np.array(macd_values), 9)
        if signal_line is None:
            signal_line = macd_line

    histogram = macd_line - signal_line

    return macd_line, signal_line, histogram

def calculate_moving_average(prices, periods):
    """Calculate Simple Moving Average"""
    if len(prices) < periods:
        return None
    return np.mean(prices[-periods:])

def generate_signal(ticker, company_name, current_price,
                   rsi, macd_line, macd_signal, macd_histogram,
                   ma20, ma50, ma200, volume_ratio):
    """Generate buy/sell/watch signal with confidence scoring"""

    signal_type = "neutral"
    confidence_score = 0
    signal_reasons = []
    risk_factors = []

    # BUY SIGNALS
    buy_score = 0

    if rsi and rsi < 30:
        buy_score += 30
        signal_reasons.append(f"RSI oversold at {rsi:.1f} indicates strong rebound potential")
    elif rsi and rsi < 40:
        buy_score += 15
        signal_reasons.append(f"RSI at {rsi:.1f} approaching oversold territory")

    if macd_histogram and macd_histogram > 0 and macd_line and macd_signal and macd_line > macd_signal:
        buy_score += 25
        signal_reasons.append("Bullish MACD crossover detected")
    elif macd_histogram and macd_histogram > 0:
        buy_score += 10
        signal_reasons.append("Positive MACD momentum")

    if ma200 and current_price > ma200:
        buy_score += 20
        signal_reasons.append(f"Price above MA200 ({ma200:.2f}) confirms long-term uptrend")

    if volume_ratio > 1.3:
        buy_score += 15
        signal_reasons.append(f"Volume surge ({volume_ratio:.1%} above average) confirms accumulation")

    if ma20 and current_price < ma20 and volume_ratio > 1.2:
        buy_score += 10
        signal_reasons.append("Price below MA20 with elevated volume suggests buying opportunity")

    # SELL SIGNALS
    sell_score = 0

    if rsi and rsi > 70:
        sell_score += 30
        risk_factors.append(f"RSI overbought at {rsi:.1f} indicates potential correction")
    elif rsi and rsi > 60:
        sell_score += 15
        risk_factors.append(f"RSI at {rsi:.1f} approaching overbought zone")

    if macd_histogram and macd_histogram < 0 and macd_line and macd_signal and macd_line < macd_signal:
        sell_score += 25
        risk_factors.append("Bearish MACD crossover detected")
    elif macd_histogram and macd_histogram < 0:
        sell_score += 10
        risk_factors.append("Negative MACD momentum")

    if ma200 and current_price < ma200:
        sell_score += 20
        risk_factors.append(f"Price below MA200 ({ma200:.2f}) indicates long-term downtrend")

    if ma20 and current_price > ma20 and rsi and rsi > 65:
        sell_score += 15
        risk_factors.append("Price extended above MA20 with high RSI suggests profit-taking zone")

    # Determine final signal
    if buy_score > sell_score and buy_score >= 40:
        signal_type = "buy"
        confidence_score = min(buy_score, 100)
    elif sell_score > buy_score and sell_score >= 40:
        signal_type = "sell"
        confidence_score = min(sell_score, 100)
    elif buy_score >= 30 or sell_score >= 30:
        signal_type = "watch"
        confidence_score = max(buy_score, sell_score)
        if not signal_reasons:
            signal_reasons.append("Mixed technical signals require confirmation")
    else:
        signal_type = "neutral"
        confidence_score = 0
        signal_reasons = ["All indicators in neutral zone"]

    # Add generic risk factors if missing
    if not risk_factors:
        risk_factors.append("Market conditions remain subject to volatility")
        risk_factors.append("External macroeconomic factors should be monitored")

    # Calculate target prices
    if signal_type == "buy":
        short_term_target = current_price * 1.05
        medium_term_target = current_price * 1.10
        stop_loss = current_price * 0.95
    elif signal_type == "sell":
        short_term_target = current_price * 0.95
        medium_term_target = current_price * 0.90
        stop_loss = current_price * 1.05
    else:
        short_term_target = current_price
        medium_term_target = current_price
        stop_loss = current_price * 0.97

    # Generate action suggestion
    if signal_type == "buy":
        action = f"Consider initiating position at current levels ({current_price:.2f}). "
        action += f"Set stop-loss at {stop_loss:.2f} (-5%). "
        action += f"First target at {short_term_target:.2f} (+5%), second target at {medium_term_target:.2f} (+10%)."
    elif signal_type == "sell":
        action = f"Consider reducing exposure or taking profits at {current_price:.2f}. "
        action += f"Monitor support at {stop_loss:.2f}. "
        action += f"Potential downside to {medium_term_target:.2f} (-10%)."
    else:
        action = "Wait for clearer technical confirmation before acting. "
        action += "Monitor key levels and volume for entry signals."

    # Generate summary
    signal_emoji = "🟢" if signal_type == "buy" else "🔴" if signal_type == "sell" else "🟡"
    title = f"{signal_emoji} {signal_type.upper()} Signal on {company_name}"

    if signal_type == "buy":
        summary = f"{company_name} shows a {signal_type} signal with confidence score {confidence_score}/100. "
        summary += f"Technical indicators suggest entry opportunity at {current_price:.2f}."
    elif signal_type == "sell":
        summary = f"{company_name} shows a {signal_type} signal with confidence score {confidence_score}/100. "
        summary += f"Technical indicators suggest taking profits at {current_price:.2f}."
    else:
        summary = f"{company_name} is in a {signal_type} zone. "
        summary += "Monitor for clearer directional signals."

    result = {
        "ticker": ticker,
        "company_name": company_name,
        "signal_type": signal_type,
        "confidence_score": confidence_score,
        "title": title,
        "summary": summary,
        "key_points": signal_reasons[:5],
        "risks": risk_factors[:3],
        "action_suggestion": action,
        "target_price": {
            "short_term": round(short_term_target, 2),
            "medium_term": round(medium_term_target, 2),
            "stop_loss": round(stop_loss, 2)
        },
        "technical_details": {
            "current_price": round(current_price, 2),
            "rsi": round(rsi, 2) if rsi else None,
            "macd": round(macd_line, 2) if macd_line else None,
            "macd_signal": round(macd_signal, 2) if macd_signal else None,
            "macd_histogram": round(macd_histogram, 2) if macd_histogram else None,
            "ma20": round(ma20, 2) if ma20 else None,
            "ma50": round(ma50, 2) if ma50 else None,
            "ma200": round(ma200, 2) if ma200 else None,
            "volume_ratio": round(volume_ratio, 2)
        }
    }

    return result

def analyze_ticker_with_real_data(ticker_info, market_data):
    """Perform complete technical analysis with real market data"""

    ticker = ticker_info['Ticker']
    company_name = ticker_info['Nom']

    print(f"\n{'='*60}")
    print(f"Analyzing: {company_name} ({ticker})")
    print(f"{'='*60}")

    if market_data is None:
        print("  SKIPPED: No market data available")
        return None

    prices = market_data['prices']
    volumes = market_data['volumes']
    current_price = market_data['current_price']
    current_volume = market_data['current_volume']

    print(f"Current price: {current_price:.2f}")
    print(f"Current volume: {current_volume:.0f}")
    print(f"Data points: {len(prices)}")

    # Calculate technical indicators
    rsi = calculate_rsi(prices)
    macd_line, macd_signal, macd_histogram = calculate_macd(prices)
    ma20 = calculate_moving_average(prices, 20)
    ma50 = calculate_moving_average(prices, 50)
    ma200 = calculate_moving_average(prices, 200)
    avg_volume_20 = np.mean(volumes[-20:]) if len(volumes) >= 20 else current_volume
    volume_ratio = current_volume / avg_volume_20 if avg_volume_20 > 0 else 1.0

    print(f"\nTechnical Indicators:")
    print(f"  RSI(14): {rsi:.2f}" if rsi else "  RSI(14): N/A")
    print(f"  MACD: {macd_line:.4f}" if macd_line else "  MACD: N/A")
    print(f"  MACD Signal: {macd_signal:.4f}" if macd_signal else "  MACD Signal: N/A")
    print(f"  MACD Histogram: {macd_histogram:.4f}" if macd_histogram else "  MACD Histogram: N/A")
    print(f"  MA20: {ma20:.2f}" if ma20 else "  MA20: N/A")
    print(f"  MA50: {ma50:.2f}" if ma50 else "  MA50: N/A")
    print(f"  MA200: {ma200:.2f}" if ma200 else "  MA200: N/A")
    print(f"  Volume Ratio: {volume_ratio:.2f}")

    # Generate trading signal
    signal_result = generate_signal(
        ticker, company_name, current_price,
        rsi, macd_line, macd_signal, macd_histogram,
        ma20, ma50, ma200, volume_ratio
    )

    print(f"\n{signal_result['title']}")
    print(f"Confidence: {signal_result['confidence_score']}/100")

    return signal_result

def main():
    """Main execution with real market data"""
    print("="*80)
    print("MARKET WATCHER PEA - Real Market Data Analysis")
    print(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

    # Parse watchlist
    print("\nStep 1: Loading watchlist...")
    active_tickers, previous_indicators = parse_watchlist(EXCEL_FILE)

    if len(active_tickers) == 0:
        print("WARNING: No active tickers found!")
        sys.exit(0)

    # Analyze each ticker with real data
    print(f"\nStep 2: Analyzing {len(active_tickers)} tickers with real market data...")

    results = []
    for idx, ticker_row in active_tickers.iterrows():
        try:
            ticker = ticker_row['Ticker']
            market_data = load_yahoo_finance_data(ticker)

            if market_data:
                signal_result = analyze_ticker_with_real_data(ticker_row, market_data)
                if signal_result:
                    results.append(signal_result)
        except Exception as e:
            print(f"ERROR analyzing {ticker_row['Ticker']}: {e}")
            continue

    # Summary
    print(f"\n{'='*80}")
    print(f"Analysis Complete: {len(results)} tickers processed")
    print(f"{'='*80}")

    high_confidence_signals = [r for r in results if r['confidence_score'] >= 60]

    print(f"\nHigh-confidence signals (score >= 60): {len(high_confidence_signals)}")
    for signal in high_confidence_signals:
        print(f"  - {signal['ticker']}: {signal['signal_type'].upper()} (Score: {signal['confidence_score']})")

    # Save results
    output_data = {
        "execution_time": datetime.now().isoformat(),
        "total_tickers_analyzed": len(results),
        "high_confidence_signals": len(high_confidence_signals),
        "signals": results
    }

    with open(OUTPUT_JSON, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\nResults saved to: {OUTPUT_JSON}")

    return results, high_confidence_signals

if __name__ == "__main__":
    main()
