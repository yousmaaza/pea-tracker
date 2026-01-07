#!/usr/bin/env python3
"""
Market Watcher PEA - Autonomous Technical Analysis Engine
Analyzes PEA-eligible securities and generates trading signals
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import sys

# File paths
EXCEL_FILE = '/Users/yousrimaazaoui/Documents/projets/test-debile/claude-project/PEA_Watchlist_Indicateurs.xlsx'
OUTPUT_JSON = '/Users/yousrimaazaoui/Documents/projets/test-debile/claude-project/market_analysis_results.json'

def parse_watchlist(excel_file):
    """Parse the Excel watchlist and return active tickers"""
    try:
        # Read all sheets
        watchlist_df = pd.read_excel(excel_file, sheet_name='Watchlist')
        indicateurs_df = pd.read_excel(excel_file, sheet_name='Indicateurs')

        # Filter active tickers
        active_tickers = watchlist_df[watchlist_df['Actif'] == True].copy()

        print(f"Loaded {len(active_tickers)} active tickers from watchlist")
        print(f"Active tickers: {', '.join(active_tickers['Ticker'].tolist())}")

        return active_tickers, indicateurs_df
    except Exception as e:
        print(f"ERROR parsing Excel file: {e}")
        sys.exit(1)

def calculate_rsi(prices, periods=14):
    """Calculate Relative Strength Index"""
    if len(prices) < periods + 1:
        return None

    deltas = np.diff(prices)
    gain = np.where(deltas > 0, deltas, 0)
    loss = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.mean(gain[:periods])
    avg_loss = np.mean(loss[:periods])

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def calculate_ema(prices, periods):
    """Calculate Exponential Moving Average"""
    if len(prices) < periods:
        return None

    multiplier = 2 / (periods + 1)
    ema = [np.mean(prices[:periods])]

    for price in prices[periods:]:
        ema.append((price - ema[-1]) * multiplier + ema[-1])

    return ema[-1]

def calculate_macd(prices):
    """Calculate MACD (12, 26, 9)"""
    if len(prices) < 26:
        return None, None, None

    ema12 = calculate_ema(prices, 12)
    ema26 = calculate_ema(prices, 26)

    if ema12 is None or ema26 is None:
        return None, None, None

    macd_line = ema12 - ema26

    # Calculate signal line (9-period EMA of MACD)
    # For simplicity, using last 9 MACD values
    macd_values = []
    for i in range(len(prices) - 26):
        e12 = calculate_ema(prices[:26+i+1], 12)
        e26 = calculate_ema(prices[:26+i+1], 26)
        if e12 and e26:
            macd_values.append(e12 - e26)

    if len(macd_values) < 9:
        signal_line = macd_line
    else:
        signal_line = calculate_ema(np.array(macd_values[-9:]), 9)
        if signal_line is None:
            signal_line = macd_line

    histogram = macd_line - signal_line

    return macd_line, signal_line, histogram

def calculate_moving_average(prices, periods):
    """Calculate Simple Moving Average"""
    if len(prices) < periods:
        return None
    return np.mean(prices[-periods:])

def analyze_ticker(ticker_info, historical_data):
    """Perform complete technical analysis on a ticker"""

    ticker = ticker_info['Ticker']
    company_name = ticker_info['Nom']

    print(f"\n{'='*60}")
    print(f"Analyzing: {company_name} ({ticker})")
    print(f"{'='*60}")

    # Mock historical data for demonstration
    # In production, this would come from Yahoo Finance MCP
    np.random.seed(hash(ticker) % 2**32)
    base_price = 100 + np.random.random() * 200

    # Generate realistic price history (250 trading days)
    trend = np.linspace(0, np.random.randn() * 20, 250)
    noise = np.random.randn(250) * 5
    prices = base_price + trend + noise
    prices = np.maximum(prices, 1)  # Ensure positive prices

    # Generate volume data
    base_volume = 100000 + np.random.random() * 500000
    volumes = base_volume * (1 + np.random.randn(250) * 0.3)
    volumes = np.maximum(volumes, 1000)

    current_price = prices[-1]
    current_volume = volumes[-1]

    print(f"Current price: {current_price:.2f}")
    print(f"Current volume: {current_volume:.0f}")

    # Calculate technical indicators
    rsi = calculate_rsi(prices)
    macd_line, macd_signal, macd_histogram = calculate_macd(prices)
    ma20 = calculate_moving_average(prices, 20)
    ma50 = calculate_moving_average(prices, 50)
    ma200 = calculate_moving_average(prices, 200)
    avg_volume_20 = np.mean(volumes[-20:])
    volume_ratio = current_volume / avg_volume_20

    print(f"\nTechnical Indicators:")
    print(f"  RSI(14): {rsi:.2f}" if rsi else "  RSI(14): N/A")
    print(f"  MACD: {macd_line:.2f}" if macd_line else "  MACD: N/A")
    print(f"  MACD Signal: {macd_signal:.2f}" if macd_signal else "  MACD Signal: N/A")
    print(f"  MACD Histogram: {macd_histogram:.2f}" if macd_histogram else "  MACD Histogram: N/A")
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

    return signal_result

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
        "key_points": signal_reasons[:5],  # Limit to 5 key points
        "risks": risk_factors[:3],  # Limit to 3 risks
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

    print(f"\n{signal_emoji} SIGNAL: {signal_type.upper()} (Confidence: {confidence_score}/100)")
    print(f"Summary: {summary}")

    return result

def main():
    """Main execution function"""
    print("="*80)
    print("MARKET WATCHER PEA - Technical Analysis Engine")
    print(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

    # Step 1: Parse watchlist
    print("\nStep 1: Loading watchlist from Excel file...")
    active_tickers, previous_indicators = parse_watchlist(EXCEL_FILE)

    if len(active_tickers) == 0:
        print("WARNING: No active tickers found in watchlist!")
        sys.exit(0)

    # Step 2: Analyze each ticker
    print(f"\nStep 2: Analyzing {len(active_tickers)} tickers...")

    results = []
    for idx, ticker_row in active_tickers.iterrows():
        try:
            # In production, fetch historical data from Yahoo Finance MCP here
            historical_data = None

            signal_result = analyze_ticker(ticker_row, historical_data)
            results.append(signal_result)

        except Exception as e:
            print(f"ERROR analyzing {ticker_row['Ticker']}: {e}")
            continue

    # Step 3: Save results
    print(f"\n{'='*80}")
    print(f"Analysis Complete: {len(results)} tickers processed")
    print(f"{'='*80}")

    # Filter high-confidence signals (score >= 60)
    high_confidence_signals = [r for r in results if r['confidence_score'] >= 60]

    print(f"\nHigh-confidence signals (score >= 60): {len(high_confidence_signals)}")
    for signal in high_confidence_signals:
        print(f"  - {signal['ticker']}: {signal['signal_type'].upper()} (Score: {signal['confidence_score']})")

    # Save all results to JSON
    output_data = {
        "execution_time": datetime.now().isoformat(),
        "total_tickers_analyzed": len(results),
        "high_confidence_signals": len(high_confidence_signals),
        "signals": results
    }

    with open(OUTPUT_JSON, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\nResults saved to: {OUTPUT_JSON}")
    print("\nNext steps:")
    print("  1. Update Excel file with new indicators")
    print("  2. Generate Markdown reports for high-confidence signals")
    print("  3. Upload reports to Google Drive")
    print("  4. Send email alerts via Gmail")

if __name__ == "__main__":
    main()
