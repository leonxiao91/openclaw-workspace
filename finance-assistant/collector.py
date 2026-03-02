#!/usr/bin/env python3
"""
金融资讯收集器
收集国内外热点经济新闻和金融市场大事件
"""

import asyncio
import aiohttp
from datetime import datetime
from typing import List, Dict
import re

class FinanceNewsCollector:
    def __init__(self):
        self.news_sources = [
            {
                "name": "华尔街见闻",
                "url": "https://api.wallstreetcn.com/apiv1/content/articles?channel=global-market&client=pc&limit=10",
            },
            {
                "name": "财联社",
                "url": "https://www.cls.cn/nodeapi/updateTelegraph?app=CailianpressWeb&os=web&sv=8.1.0",
            },
            {
                "name": "东方财富财经",
                "url": "https://news.eastmoney.com/kbjg/default_1.htm",
            },
            {
                "name": "新浪财经",
                "url": "https://finance.sina.com.cn/stock/",
            },
        ]
        
    async def fetch_wallstreetcn(self) -> List[Dict]:
        """华尔街见闻"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.wallstreetcn.com/apiv1/content/articles",
                    params={"channel": "global-market", "client": "pc", "limit": 5},
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        articles = data.get("data", {}).get("articles", [])
                        return [
                            {
                                "title": a.get("title", ""),
                                "summary": a.get("summary", "")[:100],
                                "source": "华尔街见闻"
                            }
                            for a in articles[:5]
                        ]
        except Exception as e:
            print(f"WallstreetCN error: {e}")
        return []
    
    async def fetch_cls(self) -> List[Dict]:
        """财联社"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://www.cls.cn/nodeapi/updateTelegraph",
                    params={"app": "CailianpressWeb", "os": "web", "sv": "8.1.0", "limit": 5},
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        articles = data.get("data", {}).get("articles", [])
                        return [
                            {
                                "title": a.get("title", ""),
                                "summary": a.get("summary", "")[:100] if a.get("summary") else "",
                                "source": "财联社"
                            }
                            for a in articles[:5]
                        ]
        except Exception as e:
            print(f"CLS error: {e}")
        return []
    
    async def fetch_techcrunch(self) -> List[Dict]:
        """TechCrunch 科技/商业新闻"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://techcrunch.com/wp-json/wp/v2/posts",
                    params={"per_page": 5, "_embed": True},
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return [
                            {
                                "title": post.get("title", {}).get("rendered", ""),
                                "summary": re.sub(r'<[^>]+>', '', post.get("excerpt", {}).get("rendered", ""))[:100],
                                "source": "TechCrunch"
                            }
                            for post in data[:5]
                        ]
        except Exception as e:
            print(f"TechCrunch error: {e}")
        return []
    
    async def fetch_reuters(self) -> List[Dict]:
        """Reuters 路透财经"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://www.reutersagency.com/wp-json/wp/v2/posts",
                    params={"per_page": 5, "categories__in": "179"},
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return [
                            {
                                "title": post.get("title", {}).get("rendered", ""),
                                "summary": "",
                                "source": "Reuters"
                            }
                            for post in data[:5]
                        ]
        except Exception as e:
            print(f"Reuters error: {e}")
        return []
    
    async def collect_all(self) -> Dict:
        """收集所有来源的新闻"""
        print(f"[{datetime.now()}] 开始收集金融资讯...")
        
        tasks = [
            self.fetch_wallstreetcn(),
            self.fetch_cls(),
            self.fetch_techcrunch(),
            self.fetch_reuters(),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_news = []
        for result in results:
            if isinstance(result, list):
                all_news.extend(result)
        
        print(f"[{datetime.now()}] 收集完成，共 {len(all_news)} 条资讯")
        
        return {
            "news": all_news,
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

async def main():
    collector = FinanceNewsCollector()
    result = await collector.collect_all()
    print(f"收到 {len(result['news'])} 条新闻")
    for i, n in enumerate(result["news"][:5], 1):
        print(f"{i}. {n['title'][:50]}...")

if __name__ == "__main__":
    asyncio.run(main())
