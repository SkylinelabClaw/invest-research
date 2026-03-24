#!/usr/bin/env python3
"""
Generate stock price candlestick charts for the invest-research project.
Uses yfinance for data and mplfinance for candlestick charts.
Includes fallback to akshare for HK/A stocks.
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
import matplotlib.pyplot as plt

# Company to ticker mapping (Corrected for Yahoo Finance!)
companies = {
    "alibaba": ["BABA", "09988.HK"],
    "anker": ["300866.SZ"],
    "arm": ["ARM"],
    "cambricon": ["688256.SS"],
    "cambridgetechnology": ["603083.SS"], 
    "coin": ["COIN"],
    "ctrip": ["TCOM"],
    "dongpeng": ["05499.SS"],
    "fenjiu": ["00809.SS"],
    "google": ["GOOGL"],
    "guming": ["01364.HK"], 
    "hims": ["HIMS"],
    "hood": ["HOOD"],
    "hygon": ["688041.SS"],
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
    "mingming": ["02383.HK"],
}

# Get date range - last 1 year for better visibility
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

print(f"Fetching data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

def get_akshare_data(ticker, market):
    """Try to fetch data using akshare"""
    try:
        import akshare as ak
        if market == "HK":
            # Akshare HK ticker is usually 5 digits, e.g. 01364
            symbol = ticker.replace(".HK", "")
            df = ak.stock_hk_hist(symbol=symbol, start_date=start_date.strftime("%Y%m%d"), end_date=end_date.strftime("%Y%m%d"), adjust="qfq")
            # Rename columns
            df = df.rename(columns={
                '日期': 'Date', '开盘': 'Open', '收盘': 'Close',
                '最高': 'High', '最低': 'Low', '成交量': 'Volume'
            })
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.set_index('Date')
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
            return df
    except Exception as e:
        print(f"  ⚠️ Akshare failed for {ticker}: {e}")
        return None

def create_candlestick_chart(ticker, company_name, output_path):
    """Create a candlestick chart for a stock"""
    df = None
    source = ""

    # Try yfinance first
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)
        if not df.empty:
            source = "yfinance"
    except Exception as e:
        print(f"  ⚠️ yfinance failed for {ticker}: {e}")

    # If yfinance failed or empty, try akshare (for HK/A stocks)
    if df is None or df.empty:
        if ".HK" in ticker or ".SZ" in ticker or ".SS" in ticker:
            market = "HK" if ".HK" in ticker else "A"
            print(f"  🔄 Retrying {ticker} with akshare ({market})...")
            df = get_akshare_data(ticker, market)
            if df is not None and not df.empty:
                source = "akshare"

    # If still no data, generate placeholder
    if df is None or df.empty:
        print(f"  ⚠️ No data found for {ticker} ({company_name}). Generating placeholder.")
        create_placeholder_chart(company_name, ticker, output_path)
        return True

    try:
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
                 title=f'{company_name} ({ticker}) - {source}',
                 ylabel='Price',
                 ylabel_lower='Volume',
                 figratio=(16, 9),
                 mav=(5, 10, 20),
                 volume=True,
                 savefig=dict(fname=output_path, dpi=100, bbox_inches='tight'),
                 tight_layout=True)
        
        print(f"  ✅ Created: {output_path} (via {source})")
        return True
        
    except Exception as e:
        print(f"  ❌ Error plotting chart for {ticker} ({company_name}): {e}")
        return False

def create_placeholder_chart(company_name, ticker, output_path):
    """Generate a placeholder chart saying 'No Data'"""
    try:
        fig, ax = plt.subplots(figsize=(12, 6), facecolor='#1a1a2e')
        ax.set_facecolor('#1a1a2e')
        
        ax.text(0.5, 0.5, f'No Data Available\n\n{company_name} ({ticker})', 
                horizontalalignment='center', verticalalignment='center', 
                transform=ax.transAxes, color='#ff5555', fontsize=20, fontweight='bold')
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=100, facecolor='#1a1a2e', edgecolor='none')
        plt.close()
        print(f"  🟡 Generated placeholder: {output_path}")
    except Exception as e:
        print(f"  ❌ Error creating placeholder: {e}")

# Create charts directory if needed
os.makedirs('charts', exist_ok=True)

# Generate charts for each company
success_count = 0
for company_name, tickers in companies.items():
    if not tickers:
        print(f"\n{company_name}: No ticker (skipping)")
        continue
    
    ticker = tickers[0]  # Use primary ticker
    
    # Yahoo Finance format cleanup (only for A-shares .SS/.SZ, NOT for HK)
    if ticker.endswith('.SS') or ticker.endswith('.SZ'):
        # A-shares handling if needed
        pass
    
    output_file = f"charts/{company_name.lower()}.png"
    
    print(f"\n{company_name} ({ticker}):")
    if create_candlestick_chart(ticker, company_name.title(), output_file):
        success_count += 1

print(f"\n\n🎉 Successfully created {success_count} charts!")
