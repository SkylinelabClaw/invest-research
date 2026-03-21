# 股价走势图自动化生成方案

> 生成日期: 2026-03-22
> 适用环境: 中国大陆

---

## 1. 背景与挑战

在中国大陆运行股价数据获取脚本面临以下主要挑战：

| 挑战 | 说明 |
|------|------|
| **网络访问限制** | Yahoo Finance 等境外网站无法直接访问 |
| **数据源可用性** | 部分数据源需要 VPN 或代理 |
| **API 稳定性** | 爬虫类数据源可能因目标网站改版而失效 |

---

## 2. 数据源对比分析

### 2.1 推荐数据源

| 数据源 | 类型 | 美股 | 港股 | A股 | 中国大陆访问 | 备注 |
|--------|------|:----:|:----:|:---:|:------------:|------|
| **Akshare** | 开源库 | ✅ | ✅ | ✅ | ✅ 正常 | 首选方案，数据来自新浪/腾讯等国内源 |
| **Tushare** | 开源库+API | ❌ | ✅ | ✅ | ✅ 需注册 | Pro版需积分，但基础数据免费 |
| **yfinance** | 开源库 | ✅ | ✅ | ❌ | ❌ 被墙 | Yahoo 已退出中国，不推荐 |

### 2.2 数据源详细说明

#### ✅ Akshare (推荐)

- **官网**: https://akshare.akfamily.xyz/
- **GitHub**: https://github.com/akfamily/akshare
- **优点**: 
  - 完全开源免费
  - 数据来源于新浪财经、腾讯财经等国内源
  - 在中国大陆访问无障碍
  - 支持 A股、港股、美股、基金、期货等
- **缺点**: 依赖网页爬虫，接口可能随源网站变化

#### ✅ Tushare

- **官网**: https://tushare.pro/
- **免费额度**: 注册后送 100 积分，基本够用
- **优点**:
  - 数据稳定性较好
  - 文档完善
- **缺点**:
  - 需要注册获取 Token
  - 美股数据有限

#### ❌ yfinance

- **问题**: Yahoo 于 2021 年退出中国大陆，直接访问会被墙
- **结论**: 不推荐在中国大陆使用

---

## 3. 环境准备

### 3.1 安装依赖

```bash
# 核心依赖
pip install akshare pandas matplotlib mplfinance

# 可选依赖 (交互式图表)
pip install plotly
```

### 3.2 依赖说明

| 包名 | 用途 |
|------|------|
| `akshare` | 获取股票数据 |
| `pandas` | 数据处理 |
| `matplotlib` | 基础绘图 |
| `mplfinance` | K线图/股票专用图表 |
| `plotly` | 交互式图表(可选) |

---

## 4. Python 脚本示例

### 4.1 方案一：使用 mplfinance 生成 K 线图

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股价走势图自动生成工具
支持: A股、港股、美股
输出: PNG 格式 K 线图
"""

import akshare as ak
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os


def get_stock_data(stock_code: str, market: str, days: int = 90) -> pd.DataFrame:
    """
    获取股票历史数据
    
    Args:
        stock_code: 股票代码
        market: 市场类型 ("A", "HK", "US")
        days: 获取天数
    
    Returns:
        DataFrame with OHLCV data
    """
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=days+30)).strftime("%Y%m%d")
    
    if market == "A":
        # A股: 需要根据交易所选择后缀
        # 上海交易所: .SH, 深圳交易所: .SZ
        symbol = stock_code if "." in stock_code else f"{stock_code}.SZ"
        df = ak.stock_zh_a_hist(symbol=symbol, adjust="qfq", 
                                 start_date=start_date, end_date=end_date)
        # 列名映射
        df = df.rename(columns={
            '日期': 'Date', '开盘': 'Open', '收盘': 'Close',
            '最高': 'High', '最低': 'Low', '成交量': 'Volume'
        })
        
    elif market == "HK":
        # 港股: 直接使用数字代码
        df = ak.stock_hk_hist(symbol=stock_code, 
                              start_date=start_date, end_date=end_date,
                              adjust="qfq")
        df = df.rename(columns={
            '日期': 'Date', '开盘': 'Open', '收盘': 'Close',
            '最高': 'High', '最低': 'Low', '成交量': 'Volume'
        })
        
    elif market == "US":
        # 美股
        df = ak.stock_us_hist(symbol=stock_code, period='daily',
                              start_date=start_date, end_date=end_date,
                              adjust='qfq')
        df = df.rename(columns={
            '日期': 'Date', '开盘': 'Open', '收盘': 'Close',
            '最高': 'High', '最低': 'Low', '成交量': 'Volume'
        })
    
    # 转换日期并设为索引
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    
    # 取最近 N 天数据
    df = df.tail(days)
    
    return df


def plot_candlestick(df: pd.DataFrame, title: str, output_path: str):
    """
    绘制并保存 K 线图
    """
    # 设置样式
    mc = mpf.make_marketcolors(
        up='#ff2400', down='#00aa00',
        edge='inherit',
        wick='inherit',
        volume='in'
    )
    s = mpf.make_mpf_style(
        marketcolors=mc,
        gridstyle='-',
        gridcolor='#e0e0e0',
        facecolor='white',
        edgecolor='black'
    )
    
    # 绘制图表
    mpf.plot(df,
             type='candle',
             style=s,
             title=title,
             ylabel='Price',
             ylabel_lower='Volume',
             figratio=(16, 9),
             mav=(5, 10, 20),  # 5/10/20日均线
             volume=True,
             savefig=dict(fname=output_path, dpi=150, bbox_inches='tight'),
             tight_layout=True)
    
    print(f"✅ 图表已保存: {output_path}")


def generate_stock_chart(stock_code: str, market: str, days: int = 90):
    """
    主函数: 生成股票走势图
    """
    # 创建输出目录
    output_dir = "stock_charts"
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取数据
    print(f"📥 正在获取 {market} 股 {stock_code} 数据...")
    try:
        df = get_stock_data(stock_code, market, days)
        print(f"   获取到 {len(df)} 条数据")
        print(df.tail())
    except Exception as e:
        print(f"❌ 获取数据失败: {e}")
        return
    
    # 生成图表
    title = f"{stock_code} {'K线图' if market == 'A' else 'Candlestick'} ({days} days)"
    filename = f"{stock_code}_{market}_{datetime.now().strftime('%Y%m%d')}.png"
    output_path = os.path.join(output_dir, filename)
    
    plot_candlestick(df, title, output_path)
    return output_path


if __name__ == "__main__":
    # 示例: 生成不同市场的股票图表
    
    # A股 - 平安银行 (深圳交易所)
    generate_stock_chart("000001", market="A", days=90)
    
    # 港股 - 腾讯控股 (代码: 00700)
    generate_stock_chart("00700", market="HK", days=90)
    
    # 美股 - Apple
    generate_stock_chart("AAPL", market="US", days=90)
```

### 4.2 方案二：使用 plotly 生成交互式图表

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 Plotly 生成交互式股票走势图
"""

import akshare as ak
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta


def get_stock_data(stock_code: str, market: str, days: int = 90) -> pd.DataFrame:
    """获取股票数据"""
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=days+30)).strftime("%Y%m%d")
    
    if market == "A":
        symbol = stock_code if "." in stock_code else f"{stock_code}.SZ"
        df = ak.stock_zh_a_hist(symbol=symbol, adjust="qfq", 
                                 start_date=start_date, end_date=end_date)
        df = df.rename(columns={
            '日期': 'Date', '开盘': 'Open', '收盘': 'Close',
            '最高': 'High', '最低': 'Low', '成交量': 'Volume'
        })
    elif market == "HK":
        df = ak.stock_hk_hist(symbol=stock_code, 
                              start_date=start_date, end_date=end_date,
                              adjust="qfq")
        df = df.rename(columns={
            '日期': 'Date', '开盘': 'Open', '收盘': 'Close',
            '最高': 'High', '最低': 'Low', '成交量': 'Volume'
        })
    elif market == "US":
        df = ak.stock_us_hist(symbol=stock_code, period='daily',
                              start_date=start_date, end_date=end_date,
                              adjust='qfq')
        df = df.rename(columns={
            '日期': 'Date', '开盘': 'Open', '收盘': 'Close',
            '最高': 'High', '最低': 'Low', '成交量': 'Volume'
        })
    
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.tail(days)
    return df


def plot_interactive_chart(stock_code: str, market: str, days: int = 90):
    """生成交互式图表并保存为 HTML"""
    df = get_stock_data(stock_code, market, days)
    
    # 创建 K 线图
    fig = go.Figure(data=[
        go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='K线'
        )
    ])
    
    # 添加成交量柱状图
    colors = ['#00aa00' if row['Close'] >= row['Open'] else '#ff2400' 
              for _, row in df.iterrows()]
    fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'], 
                         name='成交量', yaxis='y2', marker_color=colors))
    
    # 布局设置
    fig.update_layout(
        title=f"{stock_code} 股票走势 ({market}股)",
        yaxis=dict(title="价格"),
        yaxis2=dict(title="成交量", overlaying='y', side='right'),
        xaxis_rangeslider_visible=False,
        template='plotly_white',
        height=600
    )
    
    # 保存为 HTML
    output_file = f"stock_charts/{stock_code}_{market}_interactive.html"
    fig.write_html(output_file)
    print(f"✅ 交互式图表已保存: {output_file}")
    
    # 可选: 保存为静态 PNG
    # fig.write_image(output_file.replace('.html', '.png'))


if __name__ == "__main__":
    # 示例
    plot_interactive_chart("000001", "A", 90)
    plot_interactive_chart("00700", "HK", 90)
    plot_interactive_chart("AAPL", "US", 90)
```

---

## 5. 股票代码参考

### 5.1 A股

| 股票 | 代码 | 交易所 |
|------|------|--------|
| 平安银行 | 000001 | 深圳 (SZ) |
| 贵州茅台 | 600519 | 上海 (SH) |
| 宁德时代 | 300750 | 深圳 (SZ) |
| 上证指数 | 000001 | 上海 (SH) |

> A股代码规则: 
> - 上海证券交易所: 6位数字 + `.SH`
> - 深圳证券交易所: 6位数字 + `.SZ`

### 5.2 港股

| 股票 | 代码 |
|------|------|
| 腾讯控股 | 00700 |
| 阿里巴巴 | 09988 |
| 美团 | 03690 |

> 港股代码: 5位数字，直接使用

### 5.3 美股

| 股票 | 代码 |
|------|------|
| Apple | AAPL |
| Tesla | TSLA |
| NVIDIA | NVDA |
| Microsoft | MSFT |

> 美股代码: 字母符号，直接使用

---

## 6. 常见问题

### Q1: 运行报错 "Open too fast" 或 "Too many requests"
**A**: 数据源有请求频率限制，在循环中添加延时:
```python
import time
time.sleep(2)  # 每次请求后等待2秒
```

### Q2: 数据获取不完整
**A**: 检查股票代码是否正确，以及是否为交易日。Akshare 只返回交易日数据。

### Q3: 如何批量生成多只股票图表?
**A**: 使用循环:
```python
stocks = [("000001", "A"), ("00700", "HK"), ("AAPL", "US")]
for code, market in stocks:
    generate_stock_chart(code, market)
    time.sleep(3)  # 避免请求过快
```

---

## 7. 扩展建议

1. **定时任务**: 使用 crontab 或 schedule 库实现每日自动生成
2. **技术指标**: 可添加 MACD、RSI、布林带等指标
3. **通知推送**: 生成图表后通过邮件/飞书/钉钉发送
4. **Web 展示**: 使用 Flask + Plotly Dash 搭建简易看板

---

## 8. 总结

| 方案 | 优点 | 适用场景 |
|------|------|----------|
| **Akshare + mplfinance** | 简单稳定，免费 | 批量生成静态图表 |
| **Akshare + Plotly** | 交互性强 | 需要放大/缩小查看细节 |
| **Tushare Pro** | 数据更稳定 | 专业级需求 |

**最终推荐**: 使用 **Akshare** 作为数据源，在国内访问无障碍，完全免费，能够满足 A股、港股、美股的日常需求。

---
