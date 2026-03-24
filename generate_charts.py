#!/usr/bin/env python3
"""
Generate stock price candlestick charts for the invest-research project.
Uses yfinance for data and mplfinance for candlestick charts.
"""

import yfinance as yf
import mplfinance as mpf
import pandas as pd
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib backend for non-interactive use
import matplotlib
matplotlib.use('Agg')

# Company to ticker mapping (Corrected for Yahoo Finance!)
companies = {
    "alibaba": ["BABA", "09988.HK"],
    "anker": ["300866.SZ"],
    "arm": ["ARM"],
    "cambricon": ["688256.SS"],
    # Cambridge Technology: 603083.SS is correct on Yahoo Finance (03083.SS is wrong)
    "cambridgetechnology": ["603083.SS"], 
    "coin": ["COIN"],
    "ctrip": ["TCOM"],
    "dongpeng": ["05499.SS"],
    "fenjiu": ["00809.SS"],
    "google": ["GOOGL"],
    # GuMing: 01364.HK is correct but missing on Yahoo. Will handle error.
    "guming": ["01364.HK"], 
    "hims": ["HIMS"],
    "hood": ["HOOD"],
    "hygon": ["688041.SS"],
    # Jiaxin International: 03858.HK works as 3858.HK
    "jiaxininternational": ["03858.HK"], 
    "laopugold": ["06181.HK"],
    "maotai": ["600519.SS"],
    "meta": ["META"],
    "microsoft": ["MSFT"],
    "nvidia": ["NVDA"],
    "pinduoduo": ["PDD"],
    "popmart": ["09992.HK"],
    "sanhua": ["002050.SZ", "002050.HK"],
    "sofi": ["SOFI"],
    "tencent": ["0700.HK"],
    "tencentmusic": ["TME"],
    "tsmc": ["TSM"],
    "zijinmining": ["601899.SS"],
    # Mingming: 02383.HK is missing on Yahoo
    "mingming": ["02383.HK"],
}

# Get date range - last 1 year for better visibility
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

print(f"Fetching data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

def create_candlestick_chart(ticker, company_name, output_path):
    """Create a candlestick chart for a stock"""
    try:
        # Download data
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)
        
        if df.empty:
            print(f"  ⚠️ No data for {ticker} ({company_name})")
            return False
        
        # Rename columns for mplfinance (requires lowercase)
        df = df.rename(columns={
            'Open': 'Open', 'High': 'High', 'Low': 'Low', 
            'Close': 'Close', 'Volume': 'Volume'
        })
        
        # Ensure index name is 'Date'
        df.index = df.index.rename('Date')
        
        # Create figure
        mc = mpf.make_marketcolors(
            up='#ff2400', down='#00aa00',
            edge='inherit',
            wick='inherit',
            volume='in'
        )
        s = mpf.make_mpf_style(
            marketcolors=mc,
            gridstyle='-',
            gridcolor='#e0e0e0',
            facecolor='white',
            edgecolor='black'
        )
        
        # Plot candlestick
        mpf.plot(df,
                 type='candle',
                 style=s,
                 title=f'{company_name} ({ticker})',
                 ylabel='Price',
                 ylabel_lower='Volume',
                 figratio=(16, 9),
                 mav=(5, 10, 20),
                 volume=True,
                 savefig=dict(fname=output_path, dpi=100, bbox_inches='tight'),
                 tight_layout=True)
        
        print(f"  ✅ Created: {output_path}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error creating chart for {ticker} ({company_name}): {e}")
        return False

# Create charts directory if needed
os.makedirs('charts', exist_ok=True)

# Generate charts for each company
success_count = 0
for company_name, tickers in companies.items():
    if not tickers:
        print(f"\n{company_name}: No ticker (skipping)")
        continue
    
    ticker = tickers[0]  # Use primary ticker
    
    # Ensure A-share tickers end in .SS (Shanghai) or .SZ (Shenzhen)
    # Ensure HK tickers are 5 digits and end in .HK
        
    # A-shares usually need .SS for Shanghai? yfinance uses .SS for A-shares usually or just the code?
    # yfinance usually auto-detects. But explicit is better. 
    # e.g. 600519.SS
    
    output_file = f"charts/{company_name.lower()}.png"
    
    print(f"\n{company_name} ({ticker}):")
    if create_candlestick_chart(ticker, company_name.title(), output_file):
        success_count += 1

print(f"\n\n🎉 Successfully created {success_count} charts!")
