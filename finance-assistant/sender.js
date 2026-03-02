/**
 * 飞书消息推送
 */

const axios = require('axios');
const fs = require('fs');

class FeishuSender {
  constructor() {
    this.appId = process.env.FEISHU_APP_ID || '';
    this.appSecret = process.env.FEISHU_APP_SECRET || '';
    this.userId = process.env.FEISHU_USER_ID || 'ou_532375939ab4ab7fa3a503c6f6a207e2';
    this.token = null;
  }

  async getAccessToken() {
    if (!this.appId || !this.appSecret) {
      console.log('No app credentials configured');
      return null;
    }

    try {
      const response = await axios.post(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        {
          app_id: this.appId,
          app_secret: this.appSecret
        }
      );
      return response.data?.tenant_access_token || null;
    } catch (e) {
      console.log('Get token error:', e.message);
      return null;
    }
  }

  async sendMessage(message) {
    const token = await this.getAccessToken();
    if (!token) {
      console.log('No token available, trying webhook...');
      return this.sendViaWebhook(message);
    }

    try {
      const response = await axios.post(
        'https://open.feishu.cn/open-apis/im/v1/messages',
        {
          receive_id_type: 'open_id',
          receive_id: this.userId,
          msg_type: 'text',
          content: JSON.stringify({ text: message })
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json; charset=utf-8'
          }
        }
      );
      return response.status === 200;
    } catch (e) {
      console.log('Send message error:', e.message);
      return false;
    }
  }

  async sendViaWebhook(message) {
    // 尝试使用环境变量中的webhook
    const webhookUrl = process.env.FEISHU_WEBHOOK;
    if (!webhookUrl) {
      console.log('No webhook configured');
      return false;
    }

    try {
      const response = await axios.post(webhookUrl, {
        msg_type: 'text',
        content: { text: message }
      });
      return response.status === 200;
    } catch (e) {
      console.log('Webhook error:', e.message);
      return false;
    }
  }
}

function formatMorningNews(newsData) {
  const news = newsData.news || [];
  const now = new Date();
  
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

  return lines.join('\n');
}

function formatAfternoonAnalysis(analysis) {
  const fundFlow = analysis.fundFlow || {};
  const net = fundFlow.net || 0;
  const trend = analysis.trend || '未知';
  const recommendation = analysis.recommendation || '';
  
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

  const sectorFlow = analysis.sectorFlow || [];
  for (const s of sectorFlow.slice(0, 5)) {
    const name = s.name || '';
    const change = s.change || 0;
    const emoji = change > 0 ? '🟢' : '🔴';
    lines.push(`${emoji} ${name}: ${change.toFixed(2)}%`);
  }

  lines.push('');
  lines.push('⚠️ *以上仅供参考，不构成投资建议*');

  return lines.join('\n');
}

module.exports = { FeishuSender, formatMorningNews, formatAfternoonAnalysis };
