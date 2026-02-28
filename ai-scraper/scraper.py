#!/usr/bin/env python3
"""
小红书笔记爬虫
使用 Playwright 抓取用户抱怨内容
"""

import asyncio
import json
import re
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path("xiaohongshu_data")
OUTPUT_DIR.mkdir(exist_ok=True)

# 搜索关键词 - 可以自定义
SEARCH_KEYWORDS = [
    "吐槽", "抱怨", "避雷", "踩坑", "后悔", "千万别买", 
    "太难了", "求助", "怎么办", "烦恼"
]

async def search_xiaohongshu(keyword: str, page, limit: int = 30):
    """搜索小红书关键词"""
    notes = []
    
    try:
        # 搜索URL
        url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}&type=51"
        await page.goto(url, timeout=30000)
        await page.wait_for_load_state("networkidle", timeout=15000)
        
        # 等待内容加载
        await asyncio.sleep(3)
        
        # 获取笔记元素
        for i in range(limit):
            try:
                # 使用更通用的选择器
                note_card = page.locator('.note-item, .feed-list .item, [class*="note"]').nth(i)
                if await note_card.is_visible():
                    title = await note_card.locator('.title, [class*="title"]').inner_text(timeout=2000)
                    content = await note_card.locator('.content, [class*="content"]').inner_text(timeout=2000)
                    
                    # 尝试获取作者
                    try:
                        author = await note_card.locator('.author, [class*="author"]').inner_text(timeout=1000)
                    except:
                        author = "未知"
                    
                    # 尝试获取点赞数
                    try:
                        likes = await note_card.locator('.liked, [class*="like"]').inner_text(timeout=1000)
                    except:
                        likes = "0"
                    
                    notes.append({
                        "keyword": keyword,
                        "title": title.strip() if title else "",
                        "content": content.strip()[:500] if content else "",
                        "author": author.strip() if author else "未知",
                        "likes": likes.strip() if likes else "0",
                        "url": ""
                    })
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"搜索 {keyword} 失败: {e}")
    
    return notes

async def main():
    """主函数"""
    print("🔍 开始抓取小红书...")
    
    all_notes = []
    
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.0"
        )
        page = await context.new_page()
        
        # 搜索每个关键词
        for keyword in SEARCH_KEYWORDS:
            print(f"📌 搜索: {keyword}")
            notes = await search_xiaohongshu(keyword, page)
            all_notes.extend(notes)
            print(f"   获取到 {len(notes)} 条")
            await asyncio.sleep(2)
        
        await browser.close()
    
    # 去重
    unique_notes = []
    seen = set()
    for note in all_notes:
        key = note["title"][:30]
        if key not in seen:
            seen.add(key)
            unique_notes.append(note)
    
    print(f"\n📊 共获取 {len(unique_notes)} 条笔记")
    
    # 保存
    date = datetime.now().strftime("%Y-%m-%d")
    output_file = OUTPUT_DIR / f"complaints_{date}.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(unique_notes, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已保存到 {output_file}")
    
    # 生成分析报告
    generate_report(unique_notes, date)
    
    return unique_notes

def generate_report(notes, date):
    """生成简单的分析报告"""
    
    # 统计关键词出现频率
    keyword_count = {}
    for note in notes:
        kw = note.get("keyword", "")
        keyword_count[kw] = keyword_count.get(kw, 0) + 1
    
    report = f"""# 小红书用户抱怨分析 - {date}

## 统计概览

- 总笔记数: {len(notes)}
- 关键词分布:

"""
    for kw, count in sorted(keyword_count.items(), key=lambda x: -x[1]):
        report += f"- {kw}: {count} 条\n"
    
    report += """
## 热门抱怨内容 (按点赞排序)

"""
    # 按点赞排序
    sorted_notes = sorted(notes, key=lambda x: int(x.get("likes", "0").replace("w", "").replace("+", "")) if x.get("likes", "0").replace("w", "").replace("+", "").isdigit() else 0, reverse=True)
    
    for i, note in enumerate(sorted_notes[:20], 1):
        report += f"### {i}. {note.get('title', '')[:50]}\n"
        report += f"- 关键词: {note.get('keyword', '')}\n"
        report += f"- 点赞: {note.get('likes', '0')}\n"
        if note.get('content'):
            report += f"- 内容: {note.get('content', '')[:100]}...\n"
        report += "\n"
    
    # 保存报告
    report_file = OUTPUT_DIR / f"report_{date}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"📝 报告已保存到 {report_file}")

if __name__ == "__main__":
    asyncio.run(main())
