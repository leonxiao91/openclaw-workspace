#!/usr/bin/env python3
"""
AI News Collector - 自动收集AI资讯并保存
"""

import os
import json
from datetime import datetime

# Tavily搜索需要 tavily-python 包
# pip install tavily-python

def search_ai_news():
    """搜索AI资讯"""
    try:
        from tavily import TavilyClient
        
        api_key = os.environ.get("TAVILY_API_KEY")
        if not api_key:
            return {"error": "TAVILY_API_KEY not set"}
        
        client = TavilyClient(api_key=api_key)
        
        # 搜索多个AI相关主题
        topics = [
            "large language models LLM news 2026",
            "AI video generation tools",
            "AI product releases February 2026",
            "open source AI projects",
            "AI industry news"
        ]
        
        all_results = []
        for topic in topics:
            response = client.search(
                query=topic,
                search_depth="basic",
                max_results=5,
                include_answer=True,
                include_images=False
            )
            all_results.extend(response.get("results", []))
        
        return {
            "success": True,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "results": all_results
        }
        
    except ImportError:
        return {"error": "tavily-python not installed"}
    except Exception as e:
        return {"error": str(e)}

def format_news_content(news_data):
    """格式化资讯内容"""
    if "error" in news_data:
        return f"❌ Error: {news_data['error']}"
    
    content = f"# AI资讯总结 - {news_data['date']}\n\n"
    
    for i, item in enumerate(news_data["results"][:15], 1):
        content += f"### {i}. {item.get('title', 'No Title')}\n"
        content += f"🔗 [原文链接]({item.get('url', '#')})\n"
        content += f"\n{item.get('content', 'No content')[:200]}...\n\n"
        content += "---\n\n"
    
    return content

def save_to_github(content):
    """保存到GitHub仓库"""
    from github import Github
    
    token = os.environ.get("GITHUB_TOKEN")
    repo_name = "leonxiao91/openclaw-workspace"
    
    if not token:
        return {"error": "GITHUB_TOKEN not set"}
    
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    # 文件路径
    date_str = datetime.now().strftime("%Y-%m-%d")
    month_str = datetime.now().strftime("%Y-%m")
    file_path = f"ai-news/{month_str}/news-{date_str}.md"
    
    # 检查文件是否存在
    try:
        contents = repo.get_contents(file_path)
        # 更新文件
        repo.update_file(contents.path, f"Update AI news {date_str}", content, contents.sha)
    except Exception:
        # 创建新文件
        repo.create_file(file_path, f"Add AI news {date_str}", content)
    
    return {
        "success": True,
        "file_path": file_path,
        "url": f"https://github.com/{repo_name}/blob/main/{file_path}"
    }

def main():
    """主函数"""
    print("🔍 搜索AI资讯...")
    news_data = search_ai_news()
    
    print("📝 格式化内容...")
    content = format_news_content(news_data)
    
    print("💾 保存到GitHub...")
    save_result = save_to_github(content)
    
    # 输出结果
    print("\n✅ 完成!")
    print(json.dumps(save_result, indent=2))

if __name__ == "__main__":
    main()
