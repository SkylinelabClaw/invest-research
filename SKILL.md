# 投研分析报告 Skill

## 概述
这个skill用于管理和更新投资分析网页，包括公司研究、行业研究、股价数据更新等。

## 目录结构
```
invest-research/
├── index.html          # 投研目录首页（所有公司卡片）
├── *.html              # 各公司独立报告 (alibaba.html, nvidia.html, ...)
├── charts/             # 股价走势图 (PNG格式)
└── SKILL.md           # 本skill文件
```

## 核心规则

### 1. 公司排序规则（重要！）
- **首页目录按拼音/单词首字母排序**
- A-Z顺序，每个字母一个section
- 如果同一字母下公司过多，可使用 C, C2, C3 细分
- 示例：section-A, section-C, section-C2

### 2. 首页快速导航 (quick-index)
- 搜索框下方显示字母导航
- 每个字母链接到对应 section
- 格式：`<a href="#section-A">`

### 3. 公司卡片内容
每个公司卡片必须包含：
- 公司名称 + 代码 (使用emoji图标)
- 评级标签 (买入/观察)
- **股价走势图缩略图** (必须有!)
- 股价信息：当前价、前一天涨跌幅、YTD、市值
- PE/PS等估值指标
- 一句话总结

### 4. 公司详情页模板
参考 `tencentmusic.html` 的完整结构：
1. 股票快照
2. 股价走势图（含时间标注）
3. 核心警示/亮点
4. 财务指标（季度/年度）
5. 五季度财务明细表
6. 业务深度解析
7. 管理层发言/Q&A
8. DCF估值（三情景）
9. 巴菲特评分
10. 综合裁决
11. 主要风险
12. 免责声明

### 5. 股价走势图
- 美股/港股：使用Yahoo Finance图表 → 保存到 charts/ 目录
- A股：使用新浪财经 GIF图表
- 时间标注：`(2025-03 ~ 2026-03)` 格式

### 6. GitHub Pages
- 仓库：https://github.com/SkylinelabClaw/invest-research
- 网页：https://skylinelabclaw.github.io/invest-research/
- 每次更新后执行：`git add -A && git commit -m "描述" && git push`

## 添加新公司流程

1. **创建公司报告**
   - 复制 `tencentmusic.html` 作为模板
   - 重命名为 `{公司名拼音}.html`
   - 填写完整的投资分析内容

2. **获取股价数据**
   - 美股：`https://query1.finance.yahoo.com/v7/finance/download/{股票代码}?period1=...&interval=1wk&events=history`
   - 或使用Python脚本生成图表

3. **添加股价走势图**
   - 下载图表到 `charts/` 目录
   - 在报告HTML中添加：`<img src="charts/{代码}.png">`

4. **更新首页**
   - 在index.html中找到对应字母的section
   - 按拼音顺序插入公司卡片
   - 更新quick-index导航
   - 更新公司总数 (在header的subtitle中)

5. **推送更新**
   ```bash
   cd invest-research
   git add -A
   git commit -m "Add {公司名} investment report"
   git push
   ```

## 更新现有公司流程

1. 找到对应的HTML文件
2. 更新股价、财报数据
3. 更新时间戳
4. 重新生成股价走势图（如需要）
5. 提交推送

## 评级说明
- **买入 (Buy)**: 推荐买入，目标价有20%+上涨空间
- **观察 (Watch)**: 关注但暂不推荐买入，等待更好时机

## 注意事项
- 所有数据需要注明来源和时间
- 投资分析仅供研究参考，不构成投资建议
- 定期更新股价和财报数据
