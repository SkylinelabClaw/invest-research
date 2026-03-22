#!/usr/bin/env python3
"""Add stock chart sections to company pages that don't have them."""

import os
import re

# Mapping of company names to their chart filenames
chart_mapping = {
    "alibaba": "alibaba.png",
    "anker": "anker.png",
    "cambricon": "cambricon.png",
    "dongpeng": "dongpeng.png",
    "fenjiu": "fenjiu.png",
    "google": "google.png",
    "guming": "guming.png",
    "hygon": "hygon.png",
    "jiaxininternational": "jiaxininternational.png",
    "maotai": "maotai.png",
    "meta": "meta.png",
    "tsmc": "tsmc.png",
}

# Chinese name mapping for alt text
chinese_names = {
    "alibaba": "阿里巴巴",
    "anker": "安克创新",
    "cambricon": "寒武纪",
    "dongpeng": "东鹏特饮",
    "fenjiu": "山西汾酒",
    "google": "谷歌",
    "guming": "古茗",
    "hygon": "海光信息",
    "jiaxininternational": "佳鑫国际",
    "maotai": "茅台",
    "meta": "Meta",
    "tsmc": "台积电",
}

# Chart HTML template
chart_template = '''<section><h2>📈 一年股价走势</h2>
<div class="chart-container" style="background:var(--card-bg);border-radius:12px;padding:20px;margin-bottom:30px;">
<img alt="{chinese_name}一年股价走势" src="charts/{chart_file}" style="width:100%;max-width:900px;display:block;margin:0 auto;border-radius:8px;"/>
<p style="text-align:center;color:var(--text-muted);font-size:0.85em;margin-top:15px;">数据来源: Yahoo Finance | 过去52周周线走势</p>
</div>
</section>
'''

# Companies to add charts to
companies = [
    "alibaba",
    "anker", 
    "cambricon",
    "dongpeng",
    "fenjiu",
    "google",
    "guming",
    "hygon",
    "jiaxininternational",
    "maotai",
    "meta",
    "tsmc",
]

for company in companies:
    html_file = f"{company}.html"
    if not os.path.exists(html_file):
        print(f"Skipping {html_file} - not found")
        continue
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has a chart section
    if 'charts/' in content:
        print(f"Skipping {company} - already has chart")
        continue
    
    chart_file = chart_mapping.get(company)
    chinese_name = chinese_names.get(company)
    
    if not chart_file or not chinese_name:
        print(f"Skipping {company} - no mapping")
        continue
    
    # Insert chart after the snapshot section
    # Find the pattern </section> that follows the snapshot
    # We'll insert after the first </section> that comes after the snapshot
    
    # Find position after the snapshot section ends
    snapshot_end = content.find('<section><h2>📊 股票快照')
    if snapshot_end == -1:
        # Try alternative pattern
        snapshot_end = content.find('<section><h2>📈')
        if snapshot_end == -1:
            print(f"Could not find snapshot section in {company}")
            continue
    
    # Find the closing </section> after snapshot
    next_section_start = content.find('<section>', snapshot_end + 10)
    if next_section_start == -1:
        print(f"Could not find next section in {company}")
        continue
    
    # Insert chart section before the next section
    chart_html = chart_template.format(chinese_name=chinese_name, chart_file=chart_file)
    new_content = content[:next_section_start] + chart_html + content[next_section_start:]
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added chart to {company}")

print("\nDone!")
