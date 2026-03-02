/**
 * 市场分析器
 * 分析市场资金流向，提供投资建议
 */

const axios = require('axios');

class MarketAnalyzer {
  constructor() {
    this.headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    };
  }

  async getFundFlow() {
    try {
      const response = await axios.get(
        'https://push2.eastmoney.com/api/qt/clist/get',
        {
          params: {
            pn: 1,
            pz: 5,
            po: 1,
            np: 1,
            fltt: 2,
            invt: 2,
            fid: 'f3',
            fs: 'm:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23',
            fields: 'f1,f2,f3,f4,f12,f13,f14',
            _: Date.now()
          },
          headers: this.headers,
          timeout: 10000
        }
      );

      const diff = response.data?.data?.diff || [];
      let totalInflow = 0;
      let totalOutflow = 0;

      for (const item of diff) {
        const change = item.f3 || 0;
        if (change > 0) {
          totalInflow += change;
        } else {
          totalOutflow += Math.abs(change);
        }
      }

      return {
        inflow: totalInflow,
        outflow: totalOutflow,
        net: totalInflow - totalOutflow,
        stocks: diff.slice(0, 5).map(s => ({
          code: s.f12,
          name: s.f14,
          change: s.f3
        }))
      };
    } catch (e) {
      console.log('Fund flow error:', e.message);
    }

    return { inflow: 0, outflow: 0, net: 0, stocks: [] };
  }

  async getSectorFlow() {
    try {
      const response = await axios.get(
        'https://push2.eastmoney.com/api/qt/clist/get',
        {
          params: {
            pn: 1,
            pz: 10,
            po: 1,
            np: 1,
            fltt: 2,
            invt: 2,
            fid: 'f3',
            fs: 'm:90+t:2,m:90+t:23',
            fields: 'f1,f2,f3,f4,f12,f13,f14',
            _: Date.now()
          },
          headers: this.headers,
          timeout: 10000
        }
      );

      const diff = response.data?.data?.diff || [];
      return diff.slice(0, 10).map(s => ({
        name: s.f14,
        change: s.f3
      }));
    } catch (e) {
      console.log('Sector flow error:', e.message);
    }

    return [];
  }

  async analyze() {
    console.log(`[${new Date().toISOString()}] 开始市场分析...`);

    const [fundFlow, sectorFlow] = await Promise.all([
      this.getFundFlow(),
      this.getSectorFlow()
    ]);

    // 生成投资建议
    const net = fundFlow.net || 0;
    let trend, recommendation;

    if (net > 5000000000) { // 50亿+
      trend = '强势上涨';
      recommendation = '建议适度增持，把握趋势行情';
    } else if (net > 1000000000) { // 10亿+
      trend = '小幅流入';
      recommendation = '建议观望，关注板块轮动';
    } else if (net > 0) {
      trend = '中性';
      recommendation = '建议轻仓操作，注意风险';
    } else {
      trend = '流出';
      recommendation = '建议减仓或保持观望';
    }

    const analysis = {
      fundFlow,
      sectorFlow,
      trend,
      recommendation,
      analyzedAt: new Date().toISOString()
    };

    console.log(`[${new Date().toISOString()}] 分析完成: ${trend}`);

    return analysis;
  }
}

module.exports = MarketAnalyzer;
