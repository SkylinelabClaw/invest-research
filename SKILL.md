# 投研分析报告 Skill

## 概述
这个skill用于管理和更新投资分析网页，包括公司研究、行业研究、股价数据更新等。

**核心原则：所有判断和信息都要有数据支撑，论述尽可能详实。**

## 目录结构
```
invest-research/
├── index.html          # 投研目录首页（所有公司卡片）
├── *.html              # 各公司独立报告 (alibaba.html, nvidia.html, ...)
├── charts/             # 股价走势图 (PNG格式)
└── SKILL.md           # 本skill文件
```

## 核心规则

### 1. 公司排序规则（重要！必须严格遵守）
- **核心原则：每家公司只出现一次**
- **中国公司（含中国总部/在香港或A股上市的公司）→ 中文拼音首字母**
- **外国公司（总部在美/欧/日等）→ 英文单词首字母**
- A-Z顺序，每个字母一个section，每个公司只出现在一个字母下

**正确排序示例（2026-03-22更新）：**
- A: 阿里巴巴(A)、安克创新(A→Anke)、ARM(英国/日本→A)
- C: 剑桥科技(Jian→J 移动到J!)、Coinbase(美国→C) → 实际C段: 剑桥科技、Coinbase
- D: 东鹏特饮(Dong→D)
- G: 谷歌(Google→G)、古茗(Guming→G)、极智嘉(Ji→J 移动到J!)
- H: 寒武纪(Han→H)、海光信息(Hai→H)、Hims(美国→H)、Robinhood(美国→H)
- J: 剑桥科技(Jian→J)、极智嘉(Ji→J)、加科思(Jia→J)、佳鑫国际(Jia→J)
- M: Meta(美国→M)、微软(美国→M)、贵州茅台(Mao→M)、毛戈平(Mao→M)、鸣鸣很忙(Ming→M)
- N: Nabors(美国→N)、英伟达(US Nvidia→N)
- T: 腾讯(Ten→T)、腾讯音乐(Tencent Music→T)
- X: 携程(Xie→X) ← 注意：携程是总部在上海的中国公司，按拼音Xietu的X排序，不在C段
- Z: 紫金矿业(Zi→Z)

**注意**：携程(Ctrip)的英文名是C开头，但中文名"携程"拼音是Xietu→X，所以归入X段，不再在C段出现。

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

### 4. 公司详情页模板（必须严格遵循）
参考 `tencentmusic.html` 的完整结构，每个section都必须完整：

#### 4.1 股票快照
- 当前股价（注明日期）
- 前一天涨跌幅
- YTD涨跌幅
- 市值
- PE/PS等估值指标
- 目标价及评级

#### 4.2 股价走势图
- 52周周线图
- 时间标注：`(2025-03 ~ 2026-03)` 格式
- 数据来源标注

#### 4.3 核心警示/亮点
- 用bullet points列出
- **每个观点都要有数据支撑**
- 例如："Q4营收$681亿 (+73%)" 而不是 "营收大幅增长"

#### 4.4 财务指标（季度/年度）
- 最新季度 + 全年数据
- 营收、净利润、毛利率、净利率
- 同比/环比增长率

#### 4.5 五季度财务明细表
- 至少5个季度的关键数据对比
- 表格形式，包含：
  - 营收
  - 净利润
  - 毛利率
  - 营业利润
  - EPS
  - 用户数据（如适用）

#### 4.6 业务深度解析（重点！）
**这是最重要的section，必须详细到每个业务线：**

对于每项业务，必须包含：
- **收入金额**（具体数值）
- **同比增长率**（百分比）
- **占总营收比例**
- **毛利率/盈利情况**
- **趋势分析**

示例格式：
```html
<div class="analysis-card">
    <h3>🎵 在线音乐订阅 — 稳定引擎</h3>
    <span class="tag tag-bullish">利好</span>
    <ul style="margin-top:15px;padding-left:20px;">
        <li>Q4 RMB 45.6亿，YoY +13.2%；全年 RMB 176.6亿，+16%</li>
        <li>付费用户 1.274亿 (+5.3% YoY)，连续稳步增长</li>
        <li>ARPPU RMB 11.9 (+7.2%)——SVIP 拉升是核心驱动</li>
        <li>SVIP 用户突破 2000万（全年末），Q2 时为 1500万</li>
    </ul>
</div>
```

**禁止使用：**
- "业务增长良好" ❌
- "利润提升" ❌

**必须使用：**
- "Q4营收$681亿，同比增长73%" ✅
- "毛利率提升2.3个百分点至74.5%" ✅

#### 4.7 管理层发言/Q&A
- 引用管理层原话
- 标注发言人职位
- 解读关键信息

#### 4.8 DCF折现估值（三情景）
- 乐观/中性/悲观三种情景
- 详细假设参数
- 目标价及上涨空间

#### 4.9 巴菲特评分
对以下6项进行评分（带数据支撑）：
- 护城河
- 管理层
- 财务健康
- 盈利质量
- 可预测性
- 资本配置

#### 4.10 综合裁决
- 明确的买卖建议
- 触发条件
- 仓位建议
- 止损线

#### 4.11 主要风险
- 具体风险点
- 量化影响（如可能）

#### 4.12 免责声明

### 5. 数据要求（核心！）

**每项论述必须包含：**
- 具体数值（营收、利润、增长率等）
- 同比/环比变化
- 时间周期
- 数据来源

**数据完整性检查清单：**
- [ ] 营收数据（最新季度 + 全年）
- [ ] 净利润数据
- [ ] 毛利率、净利率
- [ ] 各业务分部收入及占比
- [ ] 用户数据（MAU、付费用户、ARPPU）
- [ ] 管理层指引
- [ ] 竞争对手对比（如有）

### 6. 股价走势图
- **统一使用本地静态图**：使用 yfinance 获取数据，用 matplotlib 生成静态 PNG 图
- 时间标注：`(2025-03 ~ 2026-03)` 格式
- **禁止使用外部 iframe 链接**

#### 6.1 图表文件名规范（重要！避免大小写匹配问题）
- **所有图表文件名必须使用小写**：`alibaba.png`、`arm.png`、`coin.png`、`google.png`
- **禁止使用大写或混合大小写**：`ARM.png`、`COIN.png`、`GOOGL.png` ❌
- **生成图表后必须验证**：确保 HTML 中的 `src="charts/xxx.png"` 与实际文件名完全匹配（区分大小写）
- **本地调试建议**：在 Mac/Linux 上开发时，由于文件系统默认不区分大小写，建议用 `ls -la` 确认文件确实存在

### 7. GitHub Pages
- 仓库：https://github.com/SkylinelabClaw/invest-research
- 网页：https://skylinelabclaw.github.io/invest-research/
- 每次更新后执行：`git add -A && git commit -m "描述" && git push`

## 添加新公司流程

1. **创建公司报告**
   - 复制 `tencentmusic.html` 作为模板
   - 重命名为 `{公司名拼音}.html`
   - 填写完整的投资分析内容

2. **获取股价数据**
   - 使用Yahoo Finance获取历史数据
   - 生成52周周线图

3. **获取财务数据**
   - 从财报电话会议获取
   - 从Yahoo Finance、Reuters等获取
   - 确保数据最新（Q4 2025或最新）

4. **业务分析（重点！）**
   - 列出所有业务线
   - 每条业务线必须有：收入、增长率、占比
   - 如有亏损业务，单独列出

5. **添加股价走势图**
   - 下载图表到 `charts/` 目录
   - 在报告HTML中添加：`<img src="charts/{代码}.png">`

6. **更新首页**
   - 在index.html中找到对应字母的section
   - 按拼音顺序插入公司卡片
   - 更新quick-index导航
   - 更新公司总数 (在header的subtitle中)

7. **推送更新**
   ```bash
   cd invest-research
   git add -A
   git commit -m "Add {公司名} investment report"
   git push
   ```

## 更新现有公司流程

1. 找到对应的HTML文件
2. 获取最新财报数据（通过web_search/web_fetch）
3. 更新业务分析section（确保每项业务都有数据）
4. 更新时间戳和数据来源
5. 重新生成股价走势图（如需要）
6. 提交推送

## 评级说明
- **买入 (Buy)**: 推荐买入，目标价有20%+上涨空间，有详细数据支撑
- **观察 (Watch)**: 关注但暂不推荐买入，等待更好时机或更多数据验证

## 版本管理与更新日志

### 版本命名规则
- 格式：v主版本.次版本 (如 v1.0, v1.1, v2.0)
- 主版本：重大功能变更、新增公司超过5家
- 次版本：小幅更新、财报数据刷新、修复等

### 更新日志要求
每次更新必须在 `CHANGELOG.md` 中记录：
1. 版本号和发布日期
2. 新增/删除的公司
3. 主要更新内容（如：财务数据刷新、页面优化等）
4. 重要Bug修复

### 更新日志格式示例
```markdown
## v1.1 (2026-06-15)

### 新增公司
- 苹果 (AAPL)
- 亚马逊 (AMZN)

### 更新内容
- 更新NVIDIA Q1财报数据
- 优化移动端显示效果

### Bug修复
- 修复股价图加载失败问题
```

### CHANGELOG.md位置
- 文件位置：`/invest-research/CHANGELOG.md`
- 每次commit前更新
- 推送时同步到GitHub

## 注意事项
- 所有数据必须注明来源（如：Yahoo Finance, 公司财报等）
- 所有数据必须标注时间周期（如：Q4 2025, FY2025等）
- 投资分析仅供研究参考，不构成投资建议
- 定期更新股价和财报数据（每季度财报季结束后更新）
- **禁止空泛的定性描述，所有结论必须有数据支撑**

## A+H股 / 港股+美股 双重上市规则

对于在两个资本市场上市的公司（如A+H股、港股+美股），必须：

1. **股票代码标注**
   - 列出所有市场的股票代码
   - 例如：阿里巴巴 (BABA.US / 09988.HK)

2. **双重股价展示**
   - 展示每个市场的当前股价
   - 分别标注涨跌幅和YTD

3. **AH/H股折价计算**
   - 计算折价/溢价比例
   - 标注折价计算公式和数据日期

4. **双重股价走势图**
   - 为每个市场分别生成股价走势图
   - 或在一个图中叠加显示两个市场的走势

5. **数据来源**
   - 标注每个市场的数据来源

**示例格式：**
```html
<div class="dual-listings">
    <div class="listing-item">
        <span class="market">🇺🇸 美股</span>
        <span class="code">BABA.US</span>
        <span class="price">$124.9</span>
        <span class="change bearish">-8.0%</span>
    </div>
    <div class="listing-item">
        <span class="market">🇭🇰 港股</span>
        <span class="code">09988.HK</span>
        <span class="price">HK$72.5</span>
        <span class="change bearish">-6.5%</span>
    </div>
    <div class="ah-premium">
        <span>AH折价: -15.2%</span>（以2026-03-20汇率计算）
    </div>
</div>
```

## 链接验证规则（重要！）

在添加外部链接时，必须验证链接的有效性和正确性：

1. **验证链接有效性**
   - 点击链接确认可以正常访问
   - 确认链接指向的内容与描述相符

2. **验证内容对应**
   - 链接描述必须与实际内容一致
   - 避免死链接、失效链接

3. **验证公众号/社交媒体**
   - 公众号文章链接需确认账号主体正确
   - 雪球等社区链接需确认用户ID正确

4. **定期检查**
   - 定期检查重要链接是否仍然有效
   - 及时修复失效链接

## 公司报告页面格式规范

每个公司报告页面必须包含以下统一格式：

1. **导航栏 (nav-bar)**
   - 回到目录按钮
   - 上一家公司/下一家公司链接

2. **头部横幅 (header)**
   - 公司名称 + 图标 (h1)
   - 股票代码标注
   - 报告日期、分析师、评级

3. **股票快照 (snapshot)**
   - 当前股价
   - 市值
   - PE/PS等估值指标
   - 目标价

4. **股价走势图**
5. **核心亮点/警示**
6. **财务指标**
7. **业务深度解析**
8. **其他sections...**

所有新建公司报告必须遵循此模板格式。

### 9. 首页(index.html)模板规范 (2026-03-22 新增)

#### 9.1 必须包含的模块
1. **顶部标题区域**：
```html
<header>
<h1>🧭 Sky Buffy 价投之路</h1>
</header>
```

2. **搜索栏区域**（必须在quick-index之前）：
```html
<div class="search-section">
<div class="search-box">
<input type="text" class="search-input" placeholder="搜索公司名称..." id="searchInput">
</div>
</div>
```

3. **拼音首字母快速索引**（必须在搜索栏之后）：
```html
<div class="quick-index">
<a class="quick-index-item" href="#section-A"><span class="quick-index-letter">A</span><span class="quick-index-count">公司名/公司名/公司名</span></a>
...
</div>
```

4. **搜索功能JavaScript**（必须在body结束前）：
```html
<script>
document.getElementById('searchInput').addEventListener('input', function(e) {
    var searchTerm = e.target.value.toLowerCase();
    var cards = document.querySelectorAll('.company-card');
    cards.forEach(function(card) {
        var name = card.querySelector('.company-name').textContent.toLowerCase();
        var code = card.querySelector('.company-code').textContent.toLowerCase();
        if (name.indexOf(searchTerm) !== -1 || code.indexOf(searchTerm) !== -1) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});
</script>
```

#### 9.2 快速索引更新规则
- **每次新增公司后必须更新quick-index**
- 格式：`<span class="quick-index-count">公司名/公司名/公司名</span>`
- 如果一个字母下超过3家公司，用"/数字"表示剩余数量，例如：`Meta/微软/茅台/毛戈平/5家`
- 同时更新section-title，例如：`M — Meta / 微软 / 贵州茅台 / 毛戈平 / 鸣鸣很忙`

为了保证所有34家公司详情页的极致统一和专业度，必须严格执行以下模块化标准：

#### 8.1 统一顶部导航栏 (Top Navigation)
- **每个公司详情页必须在最顶部添加导航栏**
- **格式**：使用 `<div class="nav-bar">` 样式（与首页保持一致）
- **左上角**：必须是「回到目录」的链接。
- **右上角**：必须是「上一家」和「下一家」的链接（按照首页A-Z的字母顺序闭环排列）。
- **代码结构标准**：
```html
<div class="nav-bar" style="background:var(--card-bg);padding:15px 20px;margin:20px auto;max-width:1160px;border-radius:12px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
<a href="index.html" style="display:flex;align-items:center;gap:8px;color:var(--text);text-decoration:none;padding:10px 20px;background:var(--secondary);border-radius:8px;font-size:0.95em;">🏠 回到目录</a>
<div style="display:flex;gap:10px;">
<a href="prev_company.html" style="display:flex;align-items:center;gap:8px;color:var(--text);text-decoration:none;padding:10px 20px;background:var(--secondary);border-radius:8px;font-size:0.95em;">⬅️ 上一家</a>
<a href="next_company.html" style="display:flex;align-items:center;gap:8px;color:var(--text);text-decoration:none;padding:10px 20px;background:var(--secondary);border-radius:8px;font-size:0.95em;">下一家 ➡️</a>
</div>
</div>
```

#### 8.2 统一页脚声明 (Footer)
- 在每个公司详情页的 `</body>` 标签前，必须显式包含统一的页脚：
```html
<footer style="text-align: center; padding: 20px; color: #888; font-size: 0.9em; border-top: 1px solid #333; margin-top: 40px;">
    Powered by OpenClaw
</footer>
```

#### 8.3 财务与预测数据溯源 (Data Sourcing)
- 对于任何**预测性数据**（如未来两年的营收、净利预期），必须明确标注 Source。
- **区分口径**：明确标出哪些是「管理层给出的前瞻指引 (Management Guidance)」，哪些是「投行/券商的一致性预期平均 (Consensus Estimates)」。

#### 8.4 估值倍数矩阵 (Valuation Multiples)
- 在「财务数据趋势与预测」的表格或模块中，除了基础的营收和利润，**必须增加三行核心估值指标：PE、PS、PB**。
- **动态估值推算**：不仅要计算当下的静态估值倍数（基于最新市值），还要结合未来两年预测的财务数据，计算并列出对应的 **Forward PE / Forward PS**。

#### 8.5 必备的深度模块检查 (Mandatory Sections)
在日常维护和新建公司时，必须自查以下模块是否缺失：
1. **管理层电话会议摘要 (Earnings Call Q&A)**：必须摘录最新财报发布后的管理层核心发言、指引和分析师问答（美股公司可直接使用英文原话摘录，或中英对照，视语境灵活变动）。
2. **投行评级与目标价 (Analyst Ratings)**：必须包含华尔街/主流券商的最新评级分布、平均目标价以及最高/最低看法的多空分歧点。
3. **最新业务分部数据 (Latest Segments)**：业务拆解必须穷尽最新披露的财报数据。如果公司更新了财务分类口径，必须以最新的口径为准（例如全面淘汰 2023/2024 的旧口径，替换为最新的季度/年度细项披露）。
