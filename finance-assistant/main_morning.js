/**
 * 早间任务 - 8:30 中国时间
 * 收集新闻并发送早报
 */

const FinanceNewsCollector = require('./collector');

async function main() {
  console.log('📈 早间金融简报');
  console.log('---');

  // 1. 收集新闻
  const collector = new FinanceNewsCollector();
  const newsData = await collector.collectAll();

  // 2. 格式化消息
  const now = new Date();
  const news = newsData.news || [];
  
  const lines = [
    '📈 **今日金融早报**',
    `*${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日*`,
    '',
    '### 🔥 热点新闻',
    ''
  ];

  for (let i = 0; i < Math.min(news.length, 8); i++) {
    const n = news[i];
    const title = (n.title || '').substring(0, 40);
    const source = n.source || '';
    lines.push(`${i+1}. ${title}... [${source}]`);
  }

  lines.push('');
  lines.push('⚠️ *以上仅供参考，不构成投资建议*');

  const message = lines.join('\n');
  
  console.log(message);
}

main().catch(console.error);
