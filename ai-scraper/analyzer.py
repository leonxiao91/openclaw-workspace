#!/usr/bin/env python3
"""
小红书用户抱怨分析
通过不同来源收集用户痛点
"""

import json
import re
import urllib.request
import urllib.parse
import ssl
from datetime import datetime
from pathlib import Path
from collections import Counter

OUTPUT_DIR = Path("xiaohongshu_data")
OUTPUT_DIR.mkdir(exist_ok=True)

def fetch_url(url, headers=None):
    """获取URL内容"""
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
    
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error: {e}")
        return ""

def parse_sogou_weibo():
    """尝试抓取微博热搜/抱怨"""
    print("📌 抓取微博...")
    
    # 微博热搜
    url = "https://weibo.com/ajax/side/hotSearch"
    html = fetch_url(url)
    
    if html:
        try:
            data = json.loads(html)
            if data.get("ok") == 1:
                realtime = data.get("data", {}).get("realtime", [])
                topics = []
                for item in realtime[:50]:
                    word = item.get("word", "")
                    raw_hot = item.get("raw_hot", 0)
                    topics.append({
                        "keyword": word,
                        "hot": raw_hot,
                        "source": "微博热搜"
                    })
                return topics
        except:
            pass
    
    return []

def parse_zhihu():
    """抓取知乎热榜"""
    print("📌 抓取知乎...")
    
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50"
    html = fetch_url(url)
    
    if html:
        try:
            data = json.loads(html)
            items = data.get("data", [])
            topics = []
            for item in items:
                title = item.get("detail_text", "")
                hot = item.get("hot", {})
                score = hot.get("score", 0)
                topics.append({
                    "keyword": title[:50],
                    "hot": score,
                    "source": "知乎"
                })
            return topics
        except:
            pass
    
    return []

def parse_douyin():
    """抓取抖音热榜"""
    print("📌 抓取抖音...")
    
    url = "https://www.douyin.com/aweme/v1/web/hot/search/list/"
    html = fetch_url(url)
    
    if html:
        try:
            data = json.loads(html)
            word_list = data.get("data", {}).get("word_list", [])
            topics = []
            for item in word_list[:30]:
                word = item.get("word", "")
                hot = item.get("hot_value", 0)
                topics.append({
                    "keyword": word,
                    "hot": hot,
                    "source": "抖音"
                })
            return topics
        except:
            pass
    
    return []

def parse_36kr():
    """抓取36氪文章标题"""
    print("📌 抓取36氪...")
    
    url = "https://36kr.com/pp/api/pc-article-feed"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Referer': 'https://36kr.com/'
    }
    html = fetch_url(url, headers)
    
    if html:
        try:
            data = json.loads(html)
            items = data.get("data", {}).get("items", [])
            topics = []
            for item in items[:20]:
                title = item.get("title", "")
                topics.append({
                    "keyword": title[:50],
                    "hot": 0,
                    "source": "36氪"
                })
            return topics
        except:
            pass
    
    return []

def analyze_pain_points(topics):
    """分析用户痛点"""
    
    # 常见抱怨关键词
    pain_keywords = [
        "难", "贵", "坑", "骗", "假", "烂", "差", "慢", "烦", "累",
        "不懂", "不会", "怎么办", "求助", "吐槽", "抱怨", "避雷",
        "后悔", "踩坑", "失望", "崩溃", "焦虑", "压力"
    ]
    
    pain_points = []
    for topic in topics:
        keyword = topic.get("keyword", "").lower()
        for pain in pain_keywords:
            if pain in keyword:
                pain_points.append({
                    "pain_keyword": pain,
                    "topic": topic.get("keyword", ""),
                    "source": topic.get("source", ""),
                    "hot": topic.get("hot", 0)
                })
    
    return pain_points

def generate_report(pain_points, topics):
    """生成分析报告"""
    
    date = datetime.now().strftime("%Y-%m-%d")
    
    # 统计痛点关键词
    pain_counter = Counter([p["pain_keyword"] for p in pain_points])
    top_pains = pain_counter.most_common(20)
    
    # 按来源统计
    source_counter = Counter([t["source"] for t in topics])
    
    report = f"""# 用户痛点分析报告 - {date}

## 📊 数据概览

- 总话题数: {len(topics)}
- 涉及来源: {", ".join(source_counter.keys())}

---

## 🔥 最常见的痛点

"""
    for pain, count in top_pains:
        report += f"- **{pain}**: {count} 个相关话题\n"
    
    report += """
---

## 💡 主要抱怨方向

"""
    # 分类痛点
    categories = {
        "学习/工作": ["学", "考", "试", "工作", "上班", "面试", "求职"],
        "生活": ["钱", "房", "车", "婚", "孩子", "家"],
        "情感": ["爱", "分手", "单身", "结婚"],
        "健康": ["病", "身体", "睡眠", "减肥"],
        "技术": ["代码", "编程", "电脑", "手机", "网络"]
    }
    
    for cat, keywords in categories.items():
        cat_topics = [t for t in topics if any(k in t.get("keyword", "") for k in keywords)]
        if cat_topics:
            report += f"### {cat} ({len(cat_topics)} 个话题)\n"
            for t in cat_topics[:5]:
                report += f"- {t.get('keyword', '')[:60]}\n"
            report += "\n"
    
    report += """---

## 🎯 可切入的应用方向

基于以上分析，以下是潜在的应用机会：

1. **效率工具** - 帮助解决"忙"、"累"、"烦"的问题
2. **学习辅助** - 针对"学不懂"、"考不过"
3. **心理健康** - 针对"焦虑"、"压力"、"崩溃"
4. **理财助手** - 针对"钱不够"、"花销大"
5. **情感咨询** - 针对恋爱、婚姻困惑

---

*报告生成时间: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """*
"""
    
    # 保存报告
    report_file = OUTPUT_DIR / f"pain_points_{date}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    # 保存原始数据
    data_file = OUTPUT_DIR / f"data_{date}.json"
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump({
            "topics": topics,
            "pain_points": pain_points
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 已保存:")
    print(f"   - 报告: {report_file}")
    print(f"   - 数据: {data_file}")
    
    return report

def main():
    print("🔍 开始分析用户痛点...\n")
    
    all_topics = []
    
    # 从各平台抓取
    all_topics.extend(parse_sogou_weibo())
    all_topics.extend(parse_zhihu())
    all_topics.extend(parse_douyin())
    all_topics.extend(parse_36kr())
    
    print(f"\n📊 共获取 {len(all_topics)} 个话题")
    
    # 分析痛点
    pain_points = analyze_pain_points(all_topics)
    print(f"📌 找到 {len(pain_points)} 个痛点相关话题")
    
    # 生成报告
    report = generate_report(pain_points, all_topics)
    print("\n" + "="*50)
    print(report[:1500] + "...")

if __name__ == "__main__":
    main()
