import os
import yfinance as yf
from bs4 import BeautifulSoup
import re

DIR = "/Users/skyline/Documents/My_AGI/00_OpenClaw_Inbox/invest-research"
INDEX_PATH = os.path.join(DIR, "index.html")

def parse_ticker(code_text):
    code = code_text.split('/')[0].strip()
    code = re.sub(r'[^\w\.]', '', code)
    if code.endswith('.US'): return code[:-3]
    elif code.endswith('.SH') or code.endswith('.SS'): return code[:-3] + '.SS'
    elif code.endswith('.SZ'):
        digits = re.sub(r'\D', '', code)
        if digits.startswith('60') or digits.startswith('68'): return digits + '.SS'
        return code
    elif code.endswith('.HK'):
        digits = re.sub(r'\D', '', code)
        if len(digits) > 4: digits = digits[-4:]
        return digits.zfill(4) + '.HK'
    else:
        if re.match(r'^[A-Z]+$', code): return code
        digits = re.sub(r'\D', '', code)
        if digits:
            if digits.startswith('60') or digits.startswith('68'): return digits + '.SS'
            elif digits.startswith('00') or digits.startswith('30'): return digits + '.SZ'
            elif len(digits) <= 5 and (code.endswith('.HK') or 'HK' in code_text):
                if len(digits) > 4: digits = digits[-4:]
                return digits.zfill(4) + '.HK'
    return code

def get_data(ticker_symbol):
    try:
        t = yf.Ticker(ticker_symbol)
        hist = t.history(period="5d")
        if hist.empty: return None
        last_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else last_price
        change = (last_price - prev_price) / prev_price * 100
        try:
            ytd_hist = t.history(period="ytd")
            if not ytd_hist.empty:
                start_price = ytd_hist['Close'].iloc[0]
                ytd = (last_price - start_price) / start_price * 100
            else: ytd = 0
        except: ytd = 0
        info = t.info
        mc = info.get('marketCap', 0)
        pe = info.get('trailingPE', 0)
        cur = info.get('currency', 'USD')
        return {'price': last_price, 'change': change, 'ytd': ytd, 'mc': mc, 'pe': pe, 'cur': cur}
    except: return None

def format_price(val, cur):
    if cur == 'CNY': return f"¥{val:.2f}"
    elif cur == 'HKD': return f"HK${val:.2f}"
    else: return f"${val:.2f}" if cur=='USD' else f"{val:.2f}"

def format_change(val):
    if val > 0: return f"+{val:.1f}%", "bullish"
    elif val < 0: return f"{val:.1f}%", "bearish"
    else: return "0.0%", "neutral"

def format_mc(val):
    if val == 0 or val is None: return "--"
    v = val / 1e8
    if v >= 10000: return f"{v/10000:.2f}万亿"
    else: return f"{v:,.0f}亿"

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

cards = soup.select('.company-card')
for card in cards:
    href = card.get('href')
    code_div = card.select_one('.company-code')
    if not code_div: continue
    ticker = parse_ticker(code_div.text)
    print(f"[{ticker}] {href}")
    
    data = get_data(ticker)
    if not data: continue
    
    p_str = format_price(data['price'], data['cur'])
    c_str, c_cls = format_change(data['change'])
    y_str, y_cls = format_change(data['ytd'])
    m_str = format_mc(data['mc'])
    if m_str != "--":
        prefix = "¥" if data['cur']=='CNY' else ("HK$" if data['cur']=='HKD' else "$")
        m_str = prefix + m_str
        
    # Detail HTML
    detail_path = os.path.join(DIR, href)
    if os.path.exists(detail_path):
        with open(detail_path, 'r', encoding='utf-8') as df:
            d_soup = BeautifulSoup(df, 'html.parser')
            
        d_cards = d_soup.select('.snapshot-card')
        price_updated = False
        for dc in d_cards:
            lbl_el = dc.select_one('.snapshot-label')
            val_el = dc.select_one('.snapshot-value')
            chg_el = dc.select_one('.snapshot-change')
            if not lbl_el or not val_el: continue
            
            lbl = lbl_el.text
            if '股' in lbl and '市值' not in lbl and not price_updated:
                # E.g. 当前股价, 美股, etc.
                val_el.string = p_str
                if chg_el:
                    chg_el.string = f"前一天: {c_str} | YTD: {y_str}"
                    # remove old colors
                    chg_el['class'] = ['snapshot-change']
                lbl_el.string = f"当前股价 (2026-03-20)"
                price_updated = True
                
            elif '市值' in lbl:
                val_el.string = m_str
                
            elif 'PE' in lbl.upper() or 'P/E' in lbl.upper():
                if data['pe'] and data['pe'] > 0:
                    val_el.string = f"{data['pe']:.1f}x"
                    
        with open(detail_path, 'w', encoding='utf-8') as df:
            df.write(str(d_soup))
            
print("Detail HTMLs updated.")
