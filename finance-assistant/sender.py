#!/usr/bin/env python3
"""
飞书消息推送
"""

import os
import json
import aiohttp
from datetime import datetime
from typing import Dict, List

class FeishuSender:
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or os.environ.get("FEISHU_WEBHOOK", "")
        self.app_id = os.environ.get("FEISHU_APP_ID", "")
        self.app_secret = os.environ.get("FEISHU_APP_SECRET", "")
    
    async def get_access_token(self) -> str:
        """获取飞书应用access_token"""
        if not self.app_id or not self.app_secret:
            return ""
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
                    json={
                        "app_id": self.app_id,
                        "app_secret": self.app_secret
                    }
                ) as resp:
                    data = await resp.json()
                    return data.get("tenant_access_token", "")
        except Exception as e:
            print(f"Get token error: {e}")
            return ""
    
    async def send_message(self, user_id: str, message: str) -> bool:
        """发送私信"""
        token = await self.get_access_token()
        if not token:
            print("No token available")
            return False
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://open.feishu.cn/open-apis/im/v1/messages",
                    params={"receive_id_type": "open_id"},
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json; charset=utf-8"
                    },
                    json={
                        "receive_id": user_id,
                        "msg_type": "text",
                        "content": json.dumps({"text": message})
                    }
                ) as resp:
                    return resp.status == 200
        except Exception as e:
            print(f"Send message error: {e}")
            return False
    
    async def send_card(self, user_id: str, card: Dict) -> bool:
        """发送卡片消息"""
        token = await self.get_access_token()
        if not token:
            return False
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://open.feishu.cn/open-apis/im/v1/messages",
                    params={"receive_id_type": "open_id"},
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json; charset=utf-8"
                    },
                    json={
                        "receive_id": user_id,
                        "msg_type": "interactive",
                        "content": json.dumps(card)
                    }
                ) as resp:
                    return resp.status == 200
        except Exception as e:
            print(f"Send card error: {e}")
            return False

def format_morning_news(news_data: Dict) -> str:
    """格式化早间新闻"""
    news = news_data.get("news", [])
    
    lines = [
        "📈 **今日金融早报**",
        f"*{datetime.now().strftime('%Y年%m月%d日')}*",
        "",
        "### 🔥 热点新闻",
        ""
    ]
    
    for i, n in enumerate(news[:8], 1):
        title = n.get("title", "")[:40]
        source = n.get("source", "")
        lines.append(f"{i}. {title}... [{source}]")
    
    lines.extend([
        "",
        "⚠️ *以上仅供参考，不构成投资建议*"
    ])
    
    return "\n".join(lines)

def format_afternoon_analysis(analysis: Dict) -> str:
    """格式化午间分析"""
    fund_flow = analysis.get("fund_flow", {})
    net = fund_flow.get("net", 0)
    trend = analysis.get("trend", "未知")
    recommendation = analysis.get("recommendation", "")
    
    # 资金流向格式化
    net_str = f"{net/1e8:.1f}亿" if net > 0 else f"{net/1e8:.1f}亿"
    
    lines = [
        "📊 **午间市场分析**",
        f"*{datetime.now().strftime('%Y年%m月%d日 %H:%M') }*",
        "",
        f"**资金流向**: {net_str}",
        f"**市场趋势**: {trend}",
        "",
        "### 💰 投资建议",
        "",
        recommendation,
        "",
        "### 📈 热门板块",
        ""
    ]
    
    sector_flow = analysis.get("sector_flow", [])[:5]
    for s in sector_flow:
        name = s.get("name", "")
        change = s.get("change", 0)
        emoji = "🟢" if change > 0 else "🔴"
        lines.append(f"{emoji} {name}: {change:.2f}%")
    
    lines.extend([
        "",
        "⚠️ *以上仅供参考，不构成投资建议*"
    ])
    
    return "\n".join(lines)

async def send_morning_news(user_id: str, news_data: Dict):
    """发送早间新闻"""
    sender = FeishuSender()
    message = format_morning_news(news_data)
    await sender.send_message(user_id, message)

async def send_afternoon_analysis(user_id: str, analysis_data: Dict):
    """发送午间分析"""
    sender = FeishuSender()
    message = format_afternoon_analysis(analysis_data)
    await sender.send_message(user_id, message)

if __name__ == "__main__":
    # Test
    test_news = {
        "news": [
            {"title": "测试新闻1", "source": "华尔街见闻"},
            {"title": "测试新闻2", "source": "财联社"},
        ]
    }
    print(format_morning_news(test_news))
