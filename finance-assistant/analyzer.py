#!/usr/bin/env python3
"""
市场分析器
分析市场资金流向，提供投资建议
"""

import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List
import json

class MarketAnalyzer:
    def __init__(self):
        self.eastmoney_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    async def get_fund_flow(self) -> Dict:
        """获取资金流向数据"""
        try:
            async with aiohttp.ClientSession() as session:
                # 主力资金流向
                async with session.get(
                    "https://push2.eastmoney.com/api/qt/clist/get",
                    params={
                        "pn": 1,
                        "pz": 5,
                        "po": 1,
                        "np": 1,
                        "fltt": 2,
                        "invt": 2,
                        "fid": "f3",
                        "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23",
                        "fields": "f1,f2,f3,f4,f12,f13,f14",
                        "_": int(datetime.now().timestamp() * 1000)
                    },
                    headers=self.eastmoney_headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        diff = data.get("data", {}).get("diff", [])
                        
                        total_inflow = 0
                        total_outflow = 0
                        
                        for item in diff:
                            change = item.get("f3", 0) or 0
                            if change > 0:
                                total_inflow += change
                            else:
                                total_outflow += abs(change)
                        
                        return {
                            "inflow": total_inflow,
                            "outflow": total_outflow,
                            "net": total_inflow - total_outflow,
                            "stocks": [
                                {"code": s.get("f12"), "name": s.get("f14"), "change": s.get("f3")}
                                for s in diff[:5]
                            ]
                        }
        except Exception as e:
            print(f"Fund flow error: {e}")
        
        return {"inflow": 0, "outflow": 0, "net": 0, "stocks": []}
    
    async def get_sector_flow(self) -> List[Dict]:
        """获取板块资金流向"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://push2.eastmoney.com/api/qt/clist/get",
                    params={
                        "pn": 1,
                        "pz": 10,
                        "po": 1,
                        "np": 1,
                        "fltt": 2,
                        "invt": 2,
                        "fid": "f3",
                        "fs": "m:90+t:2,m:90+t:23",
                        "fields": "f1,f2,f3,f4,f12,f13,f14",
                        "_": int(datetime.now().timestamp() * 1000)
                    },
                    headers=self.eastmoney_headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        diff = data.get("data", {}).get("diff", [])
                        
                        return [
                            {
                                "name": s.get("f14"),
                                "change": s.get("f3")
                            }
                            for s in diff[:10]
                        ]
        except Exception as e:
            print(f"Sector flow error: {e}")
        
        return []
    
    async def get_fund_hot(self) -> List[Dict]:
        """获取热门基金"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://fund.eastmoney.com/data/rankhandler.aspx",
                    params={
                        "op": "ph",
                        "dt": "kf",
                        "ft": "all",
                        "rs": "",
                        "gs": 0,
                        "sc": "rzdf",
                        "st": "desc",
                        "sd": datetime.now().strftime("%Y-%m-%d"),
                        "ed": datetime.now().strftime("%Y-%m-%d"),
                        "qdii": "",
                        "tabSubtype": ",,,,,",
                        "pi": 1,
                        "pn": 10,
                        "dx": 1",
                        "v": ""
                    },
                    headers=self.eastmoney_headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    text = await resp.text()
                    # 解析数据
                    import re
                    match = re.search(r'datas:\[(.*?)\]', text)
                    if match:
                        funds = match.group(1).split('","')
                        result = []
                        for f in funds[:10]:
                            parts = f.split('|')
                            if len(parts) > 3:
                                result.append({
                                    "name": parts[1],
                                    "change": parts[3]
                                })
                        return result
        except Exception as e:
            print(f"Fund hot error: {e}")
        
        return []
    
    async def analyze(self) -> Dict:
        """综合分析"""
        print(f"[{datetime.now()}] 开始市场分析...")
        
        fund_flow = await self.get_fund_flow()
        sector_flow = await self.get_sector_flow()
        
        # 生成投资建议
        net = fund_flow.get("net", 0)
        
        if net > 5000000000:  # 50亿+
            trend = "强势上涨"
            recommendation = "建议适度增持，把握趋势行情"
        elif net > 1000000000:  # 10亿+
            trend = "小幅流入"
            recommendation = "建议观望，关注板块轮动"
        elif net > 0:
            trend = "中性"
            recommendation = "建议轻仓操作，注意风险"
        else:
            trend = "流出"
            recommendation = "建议减仓或保持观望"
        
        analysis = {
            "fund_flow": fund_flow,
            "sector_flow": sector_flow,
            "trend": trend,
            "recommendation": recommendation,
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        print(f"[{datetime.now()}] 分析完成: {trend}")
        
        return analysis

async def main():
    analyzer = MarketAnalyzer()
    result = await analyzer.analyze()
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
