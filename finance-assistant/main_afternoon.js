/**
 * 午间任务 - 14:40 中国时间
 * 分析市场并发送投资建议
 */

const MarketAnalyzer = require('./analyzer');
const { FeishuSender, formatAfternoonAnalysis } = require('./sender');

async function main() {
  console.log('='.repeat(50));
  console.log('📊 午间市场分析任务启动');
  console.log('='.repeat(50));

  // 1. 分析市场
  const analyzer = new MarketAnalyzer();
  const analysisData = await analyzer.analyze();

  // 2. 格式化消息
  const message = formatAfternoonAnalysis(analysisData);
  console.log('\n消息内容:');
  console.log(message.substring(0, 500) + '...');

  // 3. 发送到飞书
  const sender = new FeishuSender();
  const success = await sender.sendMessage(message);

  if (success) {
    console.log('\n✅ 分析发送成功!');
  } else {
    console.log('\n❌ 分析发送失败');
  }

  return success;
}

main().then(result => {
  process.exit(result ? 0 : 1);
}).catch(err => {
  console.error(err);
  process.exit(1);
});
