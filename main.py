#!/usr/bin/env python3
"""
TradingAgents - Multi-Agent Financial Trading System
Main entry point for running standard trading analysis.

Usage:
    python main.py [TICKER] [DATE]
    
Examples:
    python main.py                    # Analyze NVDA on default date
    python main.py AAPL               # Analyze AAPL on default date  
    python main.py TSLA 2024-01-15    # Analyze TSLA on specific date
"""

import sys
from datetime import datetime, timedelta

# Load environment variables from .env file
import tradingagents.env_loader

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG


def main():
    """Run TradingAgents analysis with command line arguments."""
    
    # Parse command line arguments
    ticker = sys.argv[1] if len(sys.argv) > 1 else "NVDA"
    
    # Default to a recent trading date if none provided
    if len(sys.argv) > 2:
        trade_date = sys.argv[2]
    else:
        # Use a date from a few days ago (to ensure market data is available)
        default_date = datetime.now() - timedelta(days=3)
        trade_date = default_date.strftime("%Y-%m-%d")
    
    print(f"🚀 TradingAgents Analysis")
    print(f"📊 Ticker: {ticker}")
    print(f"📅 Date: {trade_date}")
    print("=" * 50)
    
    try:
        # Initialize TradingAgents system
        ta = TradingAgentsGraph(debug=False, config=DEFAULT_CONFIG)
        
        print("🤖 Running multi-agent analysis...")
        
        # Run the complete analysis pipeline
        final_state, decision = ta.propagate(ticker, trade_date)
        
        # Display results
        print("\n" + "=" * 50)
        print("📋 FINAL TRADING DECISION")
        print("=" * 50)
        print(decision)
        
        # Optional: Save results for later review
        # ta.reflect_and_remember(1000)  # Implement after backtesting
        
        print(f"\n✅ Analysis complete for {ticker} on {trade_date}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        print("\n💡 Troubleshooting:")
        print("   - Check your API keys in .env file")
        print("   - Verify internet connection for data sources")
        print("   - Try: python -m cli.main for interactive mode")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
