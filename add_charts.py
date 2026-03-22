#!/usr/bin/env python3
"""Add stock chart sections to company pages that don't have them."""

import os
import re

# Mapping of company names to their chart filenames
# Based on existing charts in the charts/ directory
chart_mapping = {
    "alibaba": "alibaba.png",  # or BABA.png or 09988.HK.png
    "anker": "anker.png",
    "cambricon": "cambricon.png",
    "dongpeng": "dongpeng.png",
    "fenjiu": "fenjiu.png",
    "google": "google.png",  # or GOOGL.png
    "guming": "guming.png",
    "hygon": "hygon.png",
    "jiaxininternational": "jiaxininternational.png",
    "maotai": "maotai.png",
    "meta": "meta.png",  # or META.png
    "tsmc": "tsmc.png",  # or TSM.png
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
chart_template = '''
<section><h2>📈 一年股价走势</h2>
<div class="chart-container" style="background:var(--card-bg);border-radius:12px;padding:20px;margin-bottom:30px;">
<img alt="{chinese_name}一年股价走势" src="charts/{chart_file}" style="width:100%;max-width:900px;display:block;margin:0 auto;border-radius:8px;"/>
<p style="text-align:center;color:var(--text-muted);font-size:0.85em;margin-top:15px;">数据来源: Yahoo Finance | 过去52周周线走势</p>
</div>
</section>
'''

# Companies to add charts to (files that don't have chart sections)
companies_without_charts = [
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

# Verify charts exist
print("Verifying chart files exist:")
for company in companies_without_charts:
    chart_file = chart_mapping.get(company)
    if chart_file:
        chart_path = f"charts/{chart_file}"
        exists = os.path.exists(chart_path)
        print(f"  {company}: {chart_path} - {'EXISTS' if exists else 'MISSING'}")
    else:
        print(f"  {company}: NO MAPPING")

# Now let's check which files already have charts by looking for the pattern
print("\nChecking which files need charts added:")
for company in companies_without_charts:
    html_file = f"{company}.html"
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has a chart section
        if 'charts/' in content:
            print(f"  {company}: Already has chart reference")
        else:
            print(f"  {company}: NEEDS chart added")
    else:
        print(f"  {company}: FILE NOT FOUND")
