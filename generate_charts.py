#!/usr/bin/env python3
"""Generate 3-year stock price charts for the invest-research project."""

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib backend for non-interactive use
import matplotlib
matplotlib.use('Agg')

# Company to ticker mapping
companies = {
    "alibaba": ["BABA", "09988.HK"],
    "anker": ["300866.SZ"],
    "arm": ["ARM"],
    "cambricon": ["688256.SS"],
    "cambridgetechnology": ["03083.SS", "06166.HK"],
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
}

# Get date range - last 3 years
end_date = datetime.now()
start_date = end_date - timedelta(days=3*365)

print(f"Fetching data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

def create_chart(ticker, company_name, output_path):
    """Create a 3-year price chart for a stock"""
    try:
        # Download data
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)
        
        if df.empty:
            print(f"  No data for {ticker}")
            return False
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6), facecolor='#1a1a2e')
        ax.set_facecolor('#1a1a2e')
        
        # Plot close price
        ax.plot(df.index, df['Close'], color='#00c853', linewidth=1.5, label='Close Price')
        
        # Fill area under the curve
        ax.fill_between(df.index, df['Close'], alpha=0.3, color='#00c853')
        
        # Formatting
        ax.set_title(f'{company_name} ({ticker}) - 3 Year Price Trend', 
                     color='#eaeaea', fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Date', color='#a0a0a0', fontsize=10)
        ax.set_ylabel('Price (USD)' if not ticker.endswith(('.HK', '.SZ', '.SS')) else 'Price (Local)', 
                      color='#a0a0a0', fontsize=10)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
        plt.xticks(rotation=45, color='#a0a0a0')
        plt.yticks(color='#a0a0a0')
        
        # Grid
        ax.grid(True, alpha=0.2, color='#a0a0a0')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#a0a0a0')
        ax.spines['left'].set_color('#a0a0a0')
        
        # Add current price annotation
        current_price = df['Close'].iloc[-1]
        price_change = ((current_price - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100

        ax.annotate(f'Current: {current_price:.2f}\n({price_change:+.1f}% 3Y)', 
                    xy=(df.index[-1], current_price),
                    xytext=(-80, 20), textcoords='offset points',
                    color='#00c853' if price_change >= 0 else '#ff1744',
                    fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a2e', edgecolor='#00c853' if price_change >= 0 else '#ff1744'),
                    arrowprops=dict(arrowstyle='->', color='#a0a0a0'))
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=100, facecolor='#1a1a2e', edgecolor='none')
        plt.close()
        
        print(f"  Created: {output_path}")
        return True
        
    except Exception as e:
        print(f"  Error creating chart for {ticker}: {e}")
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
    output_file = f"charts/{company_name}.png"
    
    print(f"\n{company_name} ({ticker}):")
    if create_chart(ticker, company_name.title(), output_file):
        success_count += 1

print(f"\n\nSuccessfully created {success_count} charts!")
