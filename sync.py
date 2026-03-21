import os
import re
import yfinance as yf
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

DIR = "/Users/skyline/Documents/My_AGI/00_OpenClaw_Inbox/invest-research"
INDEX_PATH = os.path.join(DIR, "index.html")

def parse_ticker(code_text):
    code = code_text.split('/')[0].strip()
    # Remove any emoji or spaces
    code = re.sub(r'[^\w\.]', '', code)
    
    if code.endswith('.US'):
        return code[:-3]
    elif code.endswith('.SH') or code.endswith('.SS'):
        return code[:-3] + '.SS'
    elif code.endswith('.SZ'):
        # Fix possible typo: 60/68 should be SS
        digits = re.sub(r'\D', '', code)
        if digits.startswith('60') or digits.startswith('68'):
            return digits + '.SS'
        return code
    elif code.endswith('.HK'):
        digits = re.sub(r'\D', '', code)
        if len(digits) > 4:
            digits = digits[-4:]
        return digits.zfill(4) + '.HK'
    else:
        # Check if it's pure US ticker without .US
        if re.match(r'^[A-Z]+$', code):
            return code
        
        # If it's a Chinese ticker with wrong suffix
        digits = re.sub(r'\D', '', code)
        if digits:
            if digits.startswith('60') or digits.startswith('68'):
                return digits + '.SS'
            elif digits.startswith('00') or digits.startswith('30'):
                return digits + '.SZ'
            elif len(digits) <= 5 and (code.endswith('.HK') or 'HK' in code_text):
                if len(digits) > 4: digits = digits[-4:]
                return digits.zfill(4) + '.HK'
    return code

def get_financial_data(ticker_symbol):
    try:
        t = yf.Ticker(ticker_symbol)
        hist = t.history(period="5d")
        if hist.empty:
            return None
        
        last_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else last_price
        
        daily_change = (last_price - prev_price) / prev_price * 100
        
        # YTD
        try:
            ytd_hist = t.history(period="ytd")
            if not ytd_hist.empty:
                start_price = ytd_hist['Close'].iloc[0]
                ytd_change = (last_price - start_price) / start_price * 100
            else:
                ytd_change = 0
        except:
            ytd_change = 0

        info = t.info
        market_cap = info.get('marketCap', 0)
        if market_cap is None: market_cap = 0
        pe = info.get('trailingPE', 0)
        if pe is None: pe = 0
        
        currency = info.get('currency', 'USD')
        return {
            'price': last_price,
            'change': daily_change,
            'ytd': ytd_change,
            'market_cap': market_cap,
            'pe': pe,
            'currency': currency
        }
    except Exception as e:
        print(f"Error fetching {ticker_symbol}: {e}")
        return None

def format_price(val, cur):
    if cur == 'CNY': return f"¥{val:.2f}"
    elif cur == 'HKD': return f"HK${val:.2f}"
    else: return f"{val:.2f}"

def format_change(val):
    if val > 0: return f"+{val:.1f}%", "bullish"
    elif val < 0: return f"{val:.1f}%", "bearish"
    else: return "0.0%", "neutral"

def format_market_cap(val, cur):
    if val == 0: return "--"
    # Convert to standard Chinese unit: 亿 (10^8)
    # E.g. 1 billion USD = 10 亿
    # But wait, we should show in its own currency usually?
    # Actually, the template uses 亿 based on native currency
    val_in_yi = val / 1e8
    if val_in_yi >= 10000:
        return f"{val_in_yi/10000:.1f}万亿"
    else:
        return f"{val_in_yi:,.0f}亿"

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

cards = soup.select('.company-card')
for card in cards:
    href = card.get('href')
    code_div = card.select_one('.company-code')
    if not code_div: continue
    raw_code = code_div.text
    ticker = parse_ticker(raw_code)
    print(f"Processing {href} ({raw_code}) -> {ticker}")
    
    data = get_financial_data(ticker)
    if not data:
        print(f"Failed to fetch {ticker}")
        continue
        
    price_str = format_price(data['price'], data['currency'])
    change_str, change_cls = format_change(data['change'])
    ytd_str, ytd_cls = format_change(data['ytd'])
    mcap_str = format_market_cap(data['market_cap'], data['currency'])
    
    # Update index.html card
    price_items = card.select('.price-item')
    if len(price_items) >= 4:
        price_items[0].select_one('.price-value').string = price_str
        
        change_el = price_items[1].select_one('.price-change')
        if change_el:
            change_el.string = change_str
            change_el['class'] = ['price-change', change_cls]
        
        ytd_el = price_items[2].select_one('.price-change')
        if ytd_el:
            ytd_el.string = ytd_str
            ytd_el['class'] = ['price-change', ytd_cls]
        
        mcap_el = price_items[3].select_one('.price-value')
        if mcap_el:
            mcap_el.string = mcap_str
        
    pe_info = card.select_one('.pe-info')
    if pe_info and data['pe'] > 0:
        pe_spans = pe_info.select('span')
        if pe_spans:
            if 'PE TTM' in pe_spans[0].text:
                pe_spans[0].string = f"PE TTM: {data['pe']:.1f}x"
                
    # Now update the individual html file
    detail_path = os.path.join(DIR, href)
    if os.path.exists(detail_path):
        with open(detail_path, 'r', encoding='utf-8') as df:
            d_soup = BeautifulSoup(df, 'html.parser')
            
        d_price_items = d_soup.select('.price-item')
        if len(d_price_items) >= 4:
            d_val = d_price_items[0].select_one('.price-value')
            if d_val: d_val.string = price_str
            
            d_change_el = d_price_items[1].select_one('.price-change')
            if d_change_el:
                d_change_el.string = change_str
                d_change_el['class'] = ['price-change', change_cls]
                
            d_ytd_el = d_price_items[2].select_one('.price-change')
            if d_ytd_el:
                d_ytd_el.string = ytd_str
                d_ytd_el['class'] = ['price-change', ytd_cls]
                
            d_mcap_el = d_price_items[3].select_one('.price-value')
            if d_mcap_el:
                d_mcap_el.string = mcap_str
                
        d_pe_info = d_soup.select_one('.pe-info')
        if d_pe_info and data['pe'] > 0:
            d_pe_spans = d_pe_info.select('span')
            if d_pe_spans and 'PE TTM' in d_pe_spans[0].text:
                d_pe_spans[0].string = f"PE TTM: {data['pe']:.1f}x"
                
        with open(detail_path, 'w', encoding='utf-8') as df:
            df.write(str(d_soup))

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Sync complete.")
