#!/usr/bin/env python3
"""
AI News Collector - 每日AI资讯收集器
从多个来源收集AI资讯，整理后推送到GitHub和飞书
"""

import os
import json
import datetime
import hashlib
import re
from pathlib import Path
from typing import List, Dict, Any
import urllib.request
import urllib.error
import ssl

# ============ 配置 ============
CONFIG = {
    "github_repo": "leonxiao91/openclaw-workspace",
    "github_branch": "main",
    "news_dir": "ai-news",
    "feishu_webhook": os.environ.get("FEISHU_WEBHOOK", ""),
    "sources": {
        # 主流AI公司博客
        "hackernews": {
            "url": "https://hn.algolia.com/api/v1/search_by_date?query=ai%20OR%20llm%20OR%20openai%20OR%20anthropic%20OR%20claude%20OR%20machine%20learning&tags=story&hitsPerPage=20",
            "enabled": True
        },
        "openai_blog": {
            "url": "https://openai.com/blog/rss.xml",
            "enabled": True
        },
        "anthropic_news": {
            "url": "https://www.anthropic.com/news/rss.xml",
            "enabled": True
        },
        "deepmind_blog": {
            "url": "https://deepmind.google/blog/rss.xml",
            "enabled": True
        },
        # 科技媒体
        "techcrunch_ai": {
            "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
            "enabled": True
        },
        "venturebeat_ai": {
            "url": "https://venturebeat.com/category/ai/feed/",
            "enabled": True
        },
        # AI 知名博主 (Substack)
        "AINews": {
            "url": "https://AINews.substack.com/feed",
            "enabled": True
        },
        "the_ai_breaker": {
            "url": "https://theaibreaker.com/feed/",
            "enabled": True
        },
        "interconnects": {
            "url": "https://interconnects.ai/feed/",
            "enabled": True
        }
    }
}

NEWS_CACHE_FILE = Path("/tmp/ai_news_cache.json")

def fetch_url(url: str, timeout: int = 30) -> str:
    """获取URL内容"""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def parse_hackernews(html: str) -> List[Dict]:
    """解析HackerNews JSON API"""
    try:
        data = json.loads(html)
        news = []
        for item in data.get("hits", [])[:10]:
            news.append({
                "title": item.get("title", ""),
                "url": item.get("url", f"https://news.ycombinator.com/item?id={item.get('objectID')}"),
                "source": "Hacker News",
                "points": item.get("points", 0)
            })
        return news
    except:
        return []

def parse_rss(xml: str, source_name: str) -> List[Dict]:
    """简单解析RSS"""
    news = []
    try:
        # 提取 item 标签内容
        items = re.findall(r'<item>(.*?)</item>', xml, re.DOTALL)
        for item in items[:8]:
            title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
            if not title_match:
                title_match = re.search(r'<title>(.*?)</title>', item)
            
            link_match = re.search(r'<link>(.*?)</link>', item)
            
            if title_match:
                news.append({
                    "title": title_match.group(1).strip(),
                    "url": link_match.group(1).strip() if link_match else "",
                    "source": source_name,
                    "points": 0
                })
    except Exception as e:
        print(f"Error parsing RSS from {source_name}: {e}")
    return news

def search_twitter(query: str, limit: int = 5) -> List[Dict]:
    """搜索Twitter/X - 需要API或网页抓取"""
    # 简化版本：使用Nitter或免费API
    # 这里可以后续添加
    return []

def load_cache() -> Dict:
    """加载缓存"""
    if NEWS_CACHE_FILE.exists():
        try:
            return json.loads(NEWS_CACHE_FILE.read_text())
        except:
            pass
    return {"news": [], "last_update": ""}

def save_cache(data: Dict):
    """保存缓存"""
    NEWS_CACHE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

def deduplicate_news(all_news: List[Dict]) -> List[Dict]:
    """去重"""
    seen = set()
    unique = []
    
    for item in all_news:
        # 用标题哈希去重
        key = hashlib.md5(item["title"].lower().encode()).hexdigest()
        if key not in seen:
            seen.add(key)
            unique.append(item)
    
    return unique

def format_news_markdown(news: List[Dict], date: str) -> str:
    """格式化新闻为Markdown"""
    md = f"""# 🤖 AI资讯每日推送 - {date}

> 自动收集，多源整合

## 今日要闻

"""
    
    # 按来源分组
    by_source = {}
    for item in news:
        src = item.get("source", "Other")
        if src not in by_source:
            by_source[src] = []
        by_source[src].append(item)
    
    # 输出
    for source, items in by_source.items():
        md += f"### 📰 {source}\n\n"
        for item in items:
            title = item["title"]
            url = item["url"]
            md += f"- [{title}]({url})\n"
        md += "\n"
    
    md += """---

*由 AI 自动收集整理*  
*来源: Hacker News, Anthropic, OpenAI, DeepMind, TechCrunch 等*
"""
    return md

def main():
    """主函数"""
    print("🤖 开始收集AI资讯...")
    
    all_news = []
    
    # 收集各来源
    for name, config in CONFIG["sources"].items():
        if not config.get("enabled", True):
            continue
            
        print(f"📡 获取 {name}...")
        url = config["url"]
        html = fetch_url(url)
        
        if not html:
            continue
            
        if name == "hackernews":
            news = parse_hackernews(html)
        else:
            news = parse_rss(html, name.replace("_", " ").title())
        
        all_news.extend(news)
        print(f"   获取到 {len(news)} 条")
    
    # 去重
    all_news = deduplicate_news(all_news)
    print(f"\n📊 共 {len(all_news)} 条新闻")
    
    # 生成日期
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 保存到文件
    news_dir = Path(CONFIG["news_dir"])
    news_dir.mkdir(parents=True, exist_ok=True)
    
    md = format_news_markdown(all_news, date)
    file_path = news_dir / f"{date}.md"
    file_path.write_text(md, encoding='utf-8')
    
    print(f"✅ 已保存到 {file_path}")
    
    # 生成简洁摘要用于飞书
    summary = format_feishu_message(all_news, date)
    
    return md, summary, str(file_path)

def format_feishu_message(news: List[Dict], date: str) -> str:
    """格式化飞书消息"""
    msg = f"# 🤖 AI资讯每日推送 - {date}\n\n"
    
    # 按来源分组
    by_source = {}
    for item in news:
        src = item.get("source", "Other")
        if src not in by_source:
            by_source[src] = []
        by_source[src].append(item)
    
    # 输出每来源前3条
    for source, items in list(by_source.items())[:5]:
        msg += f"### 📰 {source}\n"
        for item in items[:3]:
            title = item["title"][:60] + "..." if len(item["title"]) > 60 else item["title"]
            url = item["url"]
            msg += f"- [{title}]({url})\n"
        msg += "\n"
    
    msg += "---\n*自动收集于 ai-news/{date}*"
    return msg

if __name__ == "__main__":
    main()
