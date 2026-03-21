# 33 companies with correct sorting rules:
# - Chinese companies: use pinyin first letter
# - Foreign companies: use English first letter
# - Each company appears only once

companies = {
    # A - Alibaba (Chinese), Anker (Chinese), ARM (UK/Japanese)
    "A": [
        {"file": "alibaba.html", "name": "阿里巴巴", "code": "BABA/09988.HK"},
        {"file": "anker.html", "name": "安克创新", "code": "300866.SZ"},
        {"file": "arm.html", "name": "ARM Holdings", "code": "ARM"},
    ],
    # C - Cambridge Technology (Chinese), Coinbase (US)
    "C": [
        {"file": "cambridgetechnology.html", "name": "剑桥科技", "code": "603083.SH"},
        {"file": "coin.html", "name": "Coinbase", "code": "COIN"},
    ],
    # D - Dongpeng
    "D": [
        {"file": "dongpeng.html", "name": "东鹏特饮", "code": "605499.SZ"},
    ],
    # F - Fenjiu
    "F": [
        {"file": "fenjiu.html", "name": "山西汾酒", "code": "600809.SS"},
    ],
    # G - Google (US), Guming (Chinese), Geek+ (Chinese)
    "G": [
        {"file": "google.html", "name": "谷歌", "code": "GOOGL"},
        {"file": "guming.html", "name": "古茗", "code": "01364.HK"},
        {"file": "geekplus.html", "name": "极智嘉", "code": "2590.HK"},
    ],
    # H - Cambricon (Chinese), Hygon (Chinese), Hims (US), Hood (US)
    "H": [
        {"file": "cambricon.html", "name": "寒武纪", "code": "688256.SH"},
        {"file": "hygon.html", "name": "海光信息", "code": "688041.SH"},
        {"file": "hims.html", "name": "Hims & Hers", "code": "HIMS"},
        {"file": "hood.html", "name": "Robinhood", "code": "HOOD"},
    ],
    # J - Jacobio (Chinese), Jiaxin (Chinese)
    "J": [
        {"file": "jacobiopharma.html", "name": "加科思", "code": "0117.HK"},
        {"file": "jiaxininternational.html", "name": "佳鑫国际", "code": "03858.HK"},
    ],
    # L - Laopu Gold
    "L": [
        {"file": "laopugold.html", "name": "老铺黄金", "code": "06181.HK"},
    ],
    # M - Meta (US), Microsoft (US), Maotai (Chinese), Maogeping (Chinese), Mingming (Chinese)
    "M": [
        {"file": "meta.html", "name": "Meta", "code": "META"},
        {"file": "microsoft.html", "name": "微软", "code": "MSFT"},
        {"file": "maotai.html", "name": "贵州茅台", "code": "600519.SS"},
        {"file": "maogeping.html", "name": "毛戈平", "code": "1318.HK"},
        {"file": "mingming.html", "name": "鸣鸣很忙", "code": "02383.HK"},
    ],
    # N - Nabors (US), Nvidia (US)
    "N": [
        {"file": "nbis.html", "name": "Nabors", "code": "NBR"},
        {"file": "nvidia.html", "name": "英伟达", "code": "NVDA"},
    ],
    # O - OSL
    "O": [
        {"file": "osl.html", "name": "OSL集团", "code": "0863.HK"},
    ],
    # P - Pinduoduo (Chinese), Popmart (Chinese)
    "P": [
        {"file": "pinduoduo.html", "name": "拼多多", "code": "PDD"},
        {"file": "popmart.html", "name": "泡泡玛特", "code": "09992.HK"},
    ],
    # S - Sanhua (Chinese), Sofi (US)
    "S": [
        {"file": "sanhua.html", "name": "三花智控", "code": "002050.SZ"},
        {"file": "sofi.html", "name": "SoFi", "code": "SOFI"},
    ],
    # T - Tencent (Chinese), Tencent Music (Chinese), Ctrip (Chinese) - Xietu → X
    "T": [
        {"file": "tencent.html", "name": "腾讯", "code": "00700.HK"},
        {"file": "tencentmusic.html", "name": "腾讯音乐", "code": "1698.HK"},
    ],
    # X - Ctrip (Chinese) - Xietu → X
    "X": [
        {"file": "ctrip.html", "name": "携程", "code": "TCOM/9961.HK"},
    ],
    # Z - Zijin Mining
    "Z": [
        {"file": "zijinmining.html", "name": "紫金矿业", "code": "2899.HK"},
    ],
}

# Print summary
for letter, comps in sorted(companies.items()):
    print(f"{letter}: {len(comps)} companies")
    for c in comps:
        print(f"  - {c['name']} ({c['file']})")
        
print(f"\nTotal: {sum(len(v) for v in companies.values())} companies")
