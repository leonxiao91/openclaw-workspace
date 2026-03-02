# 金融投资助手

每日自动推送金融资讯和投资建议。

## 工作流程

### 早间简报 (8:30 中国时间)
- 国内外热点经济新闻
- 影响金融市场的大事件
- 今日投资建议

### 午间分析 (14:40 中国时间)
- 市场资金流向分析
- 基金买入/卖出建议

## 文件结构

```
finance-assistant/
├── collector.py        # 资讯收集器
├── analyzer.py        # 市场分析
├── sender.py          # 飞书推送
├── main_morning.py    # 早间任务入口
├── main_afternoon.py  # 午间任务入口
└── requirements.txt   # 依赖
```

## Cron 配置

- 早间: 8:30 中国时间 (UTC 00:30)
- 午间: 14:40 中国时间 (UTC 06:40)
