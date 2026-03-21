# Read current index.html and extract the CSS/style section
with open("index.html", "r", encoding="utf-8") as f:
    current = f.read()

# Extract CSS from current file (everything between <style> and </style>)
import re
style_match = re.search(r'<style>(.*?)</style>', current, re.DOTALL)
if style_match:
    css = style_match.group(1)
    print("Found CSS, length:", len(css))
else:
    print("No CSS found")
    css = ""

# Company data with correct sorting
companies_data = {
    "A": [
        {"file": "alibaba.html", "name": "阿里巴巴", "code": "BABA/09988.HK", "price": "$122.41", "change": "-2.0%", "ytd": "-21.4%", "mktcap": "$2,922亿", "pe": "21.7x", "rating": "观察", "summary": "中国电商龙头，AI云计算第二增长曲线"},
        {"file": "anker.html", "name": "安克创新", "code": "300866.SZ", "price": "¥168.5", "change": "+1.2%", "ytd": "+18.5%", "mktcap": "¥650亿", "pe": "28x", "rating": "买入", "summary": "出海消费电子龙头，充电宝品牌Anker"},
        {"file": "arm.html", "name": "ARM Holdings", "code": "ARM", "price": "$118.5", "change": "+3.5%", "ytd": "+45%", "mktcap": "$1,230亿", "pe": "65x", "rating": "买入", "summary": "全球芯片架构霸主，AI算力最大受益者"},
    ],
    "C": [
        {"file": "cambridgetechnology.html", "name": "剑桥科技", "code": "603083.SH", "price": "¥58.2", "change": "+2.1%", "ytd": "+35%", "mktcap": "¥155亿", "pe": "22x", "rating": "观察", "summary": "光模块出海龙头，800G/1.6T放量"},
        {"file": "coin.html", "name": "Coinbase", "code": "COIN", "price": "$245", "change": "+5.2%", "ytd": "+38%", "mktcap": "$620亿", "pe": "28x", "rating": "观察", "summary": "美国加密货币交易所龙头，ETF托管"},
    ],
    "D": [
        {"file": "dongpeng.html", "name": "东鹏特饮", "code": "605499.SZ", "price": "¥48.5", "change": "-1.5%", "ytd": "+12%", "mktcap": "¥580亿", "pe": "32x", "rating": "买入", "summary": "中国功能饮料龙头，全国化+电解质水"},
    ],
    "F": [
        {"file": "fenjiu.html", "name": "山西汾酒", "code": "600809.SS", "price": "¥285", "change": "+0.8%", "ytd": "-8%", "mktcap": "¥3,500亿", "pe": "25x", "rating": "买入", "summary": "清香型白酒龙头，青花系列高端化"},
    ],
    "G": [
        {"file": "google.html", "name": "谷歌", "code": "GOOGL", "price": "$175", "change": "+1.8%", "ytd": "+28%", "mktcap": "$2.1万亿", "pe": "26x", "rating": "买入", "summary": "全球搜索+AI龙头，云计算高增长"},
        {"file": "guming.html", "name": "古茗", "code": "01364.HK", "price": "HK$18.5", "change": "+2.5%", "ytd": "+15%", "mktcap": "¥280亿", "pe": "18x", "rating": "买入", "summary": "下沉市场茶饮万店，加盟模式高效"},
        {"file": "geekplus.html", "name": "极智嘉", "code": "2590.HK", "price": "HK$32", "change": "+4.2%", "ytd": "+55%", "mktcap": "¥180亿", "pe": "35x", "rating": "买入", "summary": "全球AMR机器人龙头，出海70%收入"},
    ],
    "H": [
        {"file": "cambricon.html", "name": "寒武纪", "code": "688256.SH", "price": "¥520", "change": "+8.5%", "ytd": "+120%", "mktcap": "¥2,200亿", "pe": "210x", "rating": "观察", "summary": "国产AI芯片龙头，思元590/690放量"},
        {"file": "hygon.html", "name": "海光信息", "code": "688041.SH", "price": "¥385", "change": "+5.2%", "ytd": "+85%", "mktcap": "¥1,800亿", "pe": "200x", "rating": "观察", "summary": "国产x86 CPU+DCU，信创市场主导"},
        {"file": "hims.html", "name": "Hims & Hers", "code": "HIMS", "price": "$32", "change": "+6.8%", "ytd": "+95%", "mktcap": "$68亿", "pe": "85x", "rating": "买入", "summary": "远程医疗+GLP-1减肥药第二曲线"},
        {"file": "hood.html", "name": "Robinhood", "code": "HOOD", "price": "$48", "change": "+3.2%", "ytd": "+42%", "mktcap": "$420亿", "pe": "45x", "rating": "观察", "summary": "散户交易平台，加密+期权收入爆发"},
    ],
    "J": [
        {"file": "jacobiopharma.html", "name": "加科思", "code": "0117.HK", "price": "HK$4.2", "change": "-2.5%", "ytd": "-15%", "mktcap": "¥45亿", "pe": "N/A", "rating": "观察", "summary": "KRAS靶点创新药，AZ授权大单"},
        {"file": "jiaxininternational.html", "name": "佳鑫国际", "code": "03858.HK", "price": "HK$118", "change": "+12%", "ytd": "+139%", "mktcap": "¥150亿", "pe": "15x", "rating": "观察", "summary": "巴库塔钨矿投产，钨价超级周期"},
    ],
    "L": [
        {"file": "laopugold.html", "name": "老铺黄金", "code": "06181.HK", "price": "HK$980", "change": "+1.5%", "ytd": "+180%", "mktcap": "¥900亿", "pe": "85x", "rating": "观察", "summary": "中国奢侈品黄金品牌，单店效率最高"},
    ],
    "M": [
        {"file": "meta.html", "name": "Meta", "code": "META", "price": "$580", "change": "+2.8%", "ytd": "+65%", "mktcap": "$1.5万亿", "pe": "32x", "rating": "买入", "summary": "全球社交+元宇宙+AI广告爆发"},
        {"file": "microsoft.html", "name": "微软", "code": "MSFT", "price": "$425", "change": "+1.5%", "ytd": "+18%", "mktcap": "$3.2万亿", "pe": "38x", "rating": "买入", "summary": "全球云+AI霸主，Copilot生态"},
        {"file": "maotai.html", "name": "贵州茅台", "code": "600519.SS", "price": "¥1,680", "change": "-0.5%", "ytd": "-5%", "mktcap": "¥2.1万亿", "pe": "28x", "rating": "买入", "summary": "A股价值投资标杆，奢侈品属性"},
        {"file": "maogeping.html", "name": "毛戈平", "code": "1318.HK", "price": "HK$98", "change": "+3.2%", "ytd": "+45%", "mktcap": "¥380亿", "pe": "42x", "rating": "买入", "summary": "中国高端美妆龙头，彩妆教育闭环"},
        {"file": "mingming.html", "name": "鸣鸣很忙", "code": "02383.HK", "price": "HK$42", "change": "+1.8%", "ytd": "N/A", "mktcap": "¥350亿", "pe": "25x", "rating": "观察", "summary": "零食很忙+赵一鸣合并，万店下沉"},
    ],
    "N": [
        {"file": "nbis.html", "name": "Nabors", "code": "NBR", "price": "$92", "change": "+2.5%", "ytd": "+15%", "mktcap": "$45亿", "pe": "12x", "rating": "观察", "summary": "全球钻井平台龙头，沙特项目高利用率"},
        {"file": "nvidia.html", "name": "英伟达", "code": "NVDA", "price": "$890", "change": "+4.5%", "ytd": "+125%", "mktcap": "$2.2万亿", "pe": "65x", "rating": "买入", "summary": "全球AI算力芯片霸主，数据中心爆发"},
    ],
    "O": [
        {"file": "osl.html", "name": "OSL集团", "code": "0863.HK", "price": "HK$18.5", "change": "+8.2%", "ytd": "+85%", "mktcap": "¥180亿", "pe": "N/A", "rating": "观察", "summary": "香港加密货币持牌龙头，ETF托管64%份额"},
    ],
    "P": [
        {"file": "pinduoduo.html", "name": "拼多多", "code": "PDD", "price": "$155", "change": "-1.2%", "ytd": "+8%", "mktcap": "$1,720亿", "pe": "18x", "rating": "观察", "summary": "下沉市场电商龙头，TEMU出海"},
        {"file": "popmart.html", "name": "泡泡玛特", "code": "09992.HK", "price": "HK$68", "change": "+5.5%", "ytd": "+95%", "mktcap": "¥920亿", "pe": "38x", "rating": "买入", "summary": "潮玩盲盒龙头，LABUBU出海破圈"},
    ],
    "S": [
        {"file": "sanhua.html", "name": "三花智控", "code": "002050.SZ", "price": "¥38", "change": "+1.8%", "ytd": "+25%", "mktcap": "¥1,380亿", "pe": "45x", "rating": "买入", "summary": "新能源热管理龙头，特斯拉+机器人"},
        {"file": "sofi.html", "name": "SoFi", "code": "SOFI", "price": "$14", "change": "+2.8%", "ytd": "+35%", "mktcap": "$145亿", "pe": "N/A", "rating": "观察", "summary": "美国Fintech全牌照，存款成本优势"},
    ],
    "T": [
        {"file": "tencent.html", "name": "腾讯", "code": "00700.HK", "price": "HK$385", "change": "+1.2%", "ytd": "+22%", "mktcap": "¥3.6万亿", "pe": "18x", "rating": "买入", "summary": "中国互联网龙头，AI+游戏复苏"},
        {"file": "tencentmusic.html", "name": "腾讯音乐", "code": "1698.HK", "price": "HK$88", "change": "+2.5%", "ytd": "+48%", "mktcap": "¥950亿", "pe": "22x", "rating": "买入", "summary": "在线音乐订阅ARPPU持续提升"},
    ],
    "X": [
        {"file": "ctrip.html", "name": "携程", "code": "TCOM/9961.HK", "price": "$68", "change": "+1.8%", "ytd": "+15%", "mktcap": "$450亿", "pe": "22x", "rating": "买入", "summary": "中国OTA龙头，出境游+高星酒店"},
    ],
    "Z": [
        {"file": "zijinmining.html", "name": "紫金矿业", "code": "2899.HK", "price": "HK$25", "change": "+3.5%", "ytd": "+45%", "mktcap": "¥4,800亿", "pe": "14x", "rating": "买入", "summary": "全球矿业龙头，铜金量价双击"},
    ],
}

# Quick index
quick_index = ""
for letter in sorted(companies_data.keys()):
    comps = companies_data[letter]
    names = "/".join([c["name"] for c in comps[:3]])
    if len(comps) > 3:
        names += f"/{len(comps)-3}家"
    quick_index += f'''<a class="quick-index-item" href="#section-{letter}"><span class="quick-index-letter">{letter}</span><span class="quick-index-count">{names}</span></a>'''

# Content
content = ""
for letter in sorted(companies_data.keys()):
    comps = companies_data[letter]
    title = f"{letter} — {' / '.join([c['name'] for c in comps])}"
    cards = ""
    for c in comps:
        change_class = "bullish" if "+" in c["change"] else "bearish"
        rating_class = "rating-buy" if c["rating"] == "买入" else "rating-watch"
        chart_file = c["file"].replace(".html", ".png")
        cards += f'''<a class="company-card" href="{c["file"]}">
<img alt="{c["name"]}股价走势" src="charts/{chart_file}" style="width:100%;height:120px;object-fit:cover;border-radius:8px;margin-bottom:10px;"/>
<div class="company-header">
<div class="company-name">{c["name"]}</div>
<span class="company-code">{c["code"]}</span>
</div>
<div class="company-price">{c["price"]}</div>
<div class="company-change {change_class}">{c["change"]} (YTD: {c["ytd"]})</div>
<div class="company-metrics">
<div class="metric"><span class="metric-label">市值:</span> {c["mktcap"]}</div>
<div class="metric"><span class="metric-label">PE:</span> {c["pe"]}</div>
</div>
<div class="company-summary">{c["summary"]}</div>
<span class="rating-badge {rating_class}">{c["rating"]}</span>
</a>'''
    content += f'''<div class="section-title" id="section-{letter}">{title}</div>
<div class="company-grid">
{cards}
</div>'''

# Replace in template
new_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Sky Buffy 价投之路 - 投资研究目录</title>
<style>
{css}
</style>
</head>
<body>
<div class="container">
<header>
<h1>🧭 Sky Buffy 价投之路</h1>
<p class="subtitle">33家优质公司深度投资研究 (A-Z)</p>
</header>
<div class="quick-index">
{quick_index}
</div>
{content}
<footer>
<p>Powered by OpenClaw | 投资研究仅供参考，不构成投资建议</p>
</footer>
</div>
</body>
</html>'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("Done! Index regenerated with correct sorting.")
