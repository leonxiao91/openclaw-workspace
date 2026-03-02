#!/usr/bin/env python3
"""
早间任务 - 8:30 中国时间
收集新闻并发送早报
"""

import asyncio
import os
import sys
import aiohttp

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collector import FinanceNewsCollector
from sender import format_morning_news, FeishuSender

USER_ID = os.environ.get("FEISHU_USER_ID", "ou_532375939ab4ab7fa3a503c6f6a207e2")

async def main():
    print("=" * 50)
    print("📈 早间金融简报任务启动")
    print("=" * 50)
    
    # 1. 收集新闻
    collector = FinanceNewsCollector()
    news_data = await collector.collect_all()
    
    # 2. 格式化消息
    message = format_morning_news(news_data)
    print("\n消息内容:")
    print(message[:500] + "...")
    
    # 3. 发送到飞书
    sender = FeishuSender()
    success = await sender.send_message(USER_ID, message)
    
    if success:
        print("\n✅ 早报发送成功!")
    else:
        print("\n❌ 早报发送失败")
    
    return success

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
