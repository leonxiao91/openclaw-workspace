/**
 * 早间任务 - 8:30 中国时间
 * 收集新闻并发送早报
 */

const FinanceNewsCollector = require('./collector');
const { FeishuSender, formatMorningNews } = require('./sender');

async function main() {
  console.log('='.repeat(50));
  console.log('📈 早间金融简报任务启动');
  console.log('='.repeat(50));

  // 1. 收集新闻
  const collector = new FinanceNewsCollector();
  const newsData = await collector.collectAll();

  // 2. 格式化消息
  const message = formatMorningNews(newsData);
  console.log('\n消息内容:');
  console.log(message.substring(0, 500) + '...');

  // 3. 发送到飞书
  const sender = new FeishuSender();
  const success = await sender.sendMessage(message);

  if (success) {
    console.log('\n✅ 早报发送成功!');
  } else {
    console.log('\n❌ 早报发送失败');
  }

  return success;
}

main().then(result => {
  process.exit(result ? 0 : 1);
}).catch(err => {
  console.error(err);
  process.exit(1);
});
