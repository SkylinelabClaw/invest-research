import os
import shutil

# Mapping: new name (based on HTML filename) -> old name (actual file)
mapping = {
    "alibaba.png": "BABA.png",
    "anker.png": None,  # Need to check
    "arm.png": "ARM.png",
    "cambricon.png": "688368.SH.png",
    "cambridgetechnology.png": None,  # Need to check
    "coin.png": "COIN.png",
    "ctrip.png": "TCOM.png",
    "dongpeng.png": "002050_SZ.png",
    "fenjiu.png": None,
    "geekplus.png": "2590_HK.png",
    "google.png": "GOOGL.png",
    "guming.png": None,
    "hims.png": "HIMS.png",
    "hood.png": "HOOD.png",
    "hygon.png": "601899.SZ.png",
    "jacobiopharma.png": "0117_HK.png",
    "jiaxininternational.png": "03858.HK.png",
    "laopugold.png": "6181.HK.png",
    "maogeping.png": "1318_HK.png",
    "maotai.png": None,
    "meta.png": "META.png",
    "microsoft.png": "MSFT.png",
    "mingming.png": None,
    "nbis.png": "NBR.png",
    "nvidia.png": "NVDA.png",
    "osl.png": "0863_HK.png",
    "pinduoduo.png": "PDD.png",
    "popmart.png": "9992.HK.png",
    "sanhua.png": None,
    "sofi.png": "SOFI.png",
    "tencent.png": "0700.HK.png",
    "tencentmusic.png": "TME.png",
    "zijinmining.png": None,
}

charts_dir = "charts"
missing = []

for new_name, old_name in mapping.items():
    if old_name is None:
        missing.append(new_name)
        print(f"MISSING: {new_name} (no source file)")
        continue
    
    old_path = os.path.join(charts_dir, old_name)
    new_path = os.path.join(charts_dir, new_name)
    
    if os.path.exists(old_path):
        # If new file already exists, remove it first
        if os.path.exists(new_path) and new_path != old_path:
            os.remove(new_path)
        if new_path != old_path:
            shutil.copy2(old_path, new_path)
            print(f"COPIED: {old_name} -> {new_name}")
    else:
        missing.append(new_name)
        print(f"MISSING: {new_name} (source {old_name} not found)")

print(f"\n=== Missing charts ({len(missing)}): ===")
for m in missing:
    print(m)
