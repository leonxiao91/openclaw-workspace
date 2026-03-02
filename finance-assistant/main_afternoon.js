/**
 * 午间任务 - 14:40 中国时间
 * 分析市场并发送投资建议
 */

const MarketAnalyzer = require('./analyzer');

async function main() {
  console.log('📊 午间市场分析');
  console.log('---');

  // 1. 分析市场
  const analyzer = new MarketAnalyzer();
  const analysisData = await analyzer.analyze();

  // 2. 格式化消息
  const fundFlow = analysisData.fundFlow || {};
  const net = fundFlow.net || 0;
  const trend = analysisData.trend || '未知';
  const recommendation = analysisData.recommendation || '';
  
  const netStr = net > 0 ? `${(net/1e8).toFixed(1)}亿` : `${(net/1e8).toFixed(1)}亿`;
  const now = new Date();

  const lines = [
    '📊 **午间市场分析**',
    `*${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日 ${now.getHours()}:${String(now.getMinutes()).padStart(2,'0')}*`,
    '',
    `**资金流向**: ${netStr}`,
    `**市场趋势**: ${trend}`,
    '',
    '### 💰 投资建议',
    '',
    recommendation,
    '',
    '### 📈 热门板块',
    ''
  ];

  const sectorFlow = analysisData.sectorFlow || [];
  for (const s of sectorFlow.slice(0, 5)) {
    const name = s.name || '';
    const change = s.change || 0;
    const emoji = change > 0 ? '🟢' : '🔴';
    lines.push(`${emoji} ${name}: ${change.toFixed(2)}%`);
  }

  lines.push('');
  lines.push('⚠️ *以上仅供参考，不构成投资建议*');

  const message = lines.join('\n');
  
  console.log(message);
}

main().catch(console.error);
