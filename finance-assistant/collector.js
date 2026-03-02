/**
 * 金融资讯收集器
 * 收集国内外热点经济新闻
 */

const axios = require('axios');

class FinanceNewsCollector {
  constructor() {
    this.headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    };
  }

  async fetchWallstreetCN() {
    try {
      const response = await axios.get(
        'https://api.wallstreetcn.com/apiv1/content/articles',
        {
          params: { channel: 'global-market', client: 'pc', limit: 5 },
          timeout: 10000
        }
      );
      const articles = response.data?.data?.articles || [];
      return articles.slice(0, 5).map(a => ({
        title: a.title || '',
        summary: (a.summary || '').substring(0, 100),
        source: '华尔街见闻'
      }));
    } catch (e) {
      console.log('WallstreetCN error:', e.message);
      return [];
    }
  }

  async fetchCLS() {
    try {
      const response = await axios.get(
        'https://www.cls.cn/nodeapi/updateTelegraph',
        {
          params: { app: 'CailianpressWeb', os: 'web', sv: '8.1.0', limit: 5 },
          timeout: 10000
        }
      );
      const articles = response.data?.data?.articles || [];
      return articles.slice(0, 5).map(a => ({
        title: a.title || '',
        summary: (a.summary || '').substring(0, 100),
        source: '财联社'
      }));
    } catch (e) {
      console.log('CLS error:', e.message);
      return [];
    }
  }

  async fetchTechCrunch() {
    try {
      const response = await axios.get(
        'https://techcrunch.com/wp-json/wp/v2/posts',
        {
          params: { per_page: 5 },
          timeout: 10000
        }
      );
      return response.data.slice(0, 5).map(post => ({
        title: post.title?.rendered || '',
        summary: (post.excerpt?.rendered || '').replace(/<[^>]+>/g, '').substring(0, 100),
        source: 'TechCrunch'
      }));
    } catch (e) {
      console.log('TechCrunch error:', e.message);
      return [];
    }
  }

  async fetchReuters() {
    try {
      const response = await axios.get(
        'https://www.reutersagency.com/wp-json/wp/v2/posts',
        {
          params: { per_page: 5, 'categories__in': 179 },
          timeout: 10000
        }
      );
      return response.data.slice(0, 5).map(post => ({
        title: post.title?.rendered || '',
        summary: '',
        source: 'Reuters'
      }));
    } catch (e) {
      console.log('Reuters error:', e.message);
      return [];
    }
  }

  async collectAll() {
    console.log(`[${new Date().toISOString()}] 开始收集金融资讯...`);

    const results = await Promise.allSettled([
      this.fetchWallstreetCN(),
      this.fetchCLS(),
      this.fetchTechCrunch(),
      this.fetchReuters()
    ]);

    const allNews = [];
    for (const result of results) {
      if (result.status === 'fulfilled' && Array.isArray(result.value)) {
        allNews.push(...result.value);
      }
    }

    console.log(`[${new Date().toISOString()}] 收集完成，共 ${allNews.length} 条资讯`);

    return {
      news: allNews,
      collectedAt: new Date().toISOString()
    };
  }
}

module.exports = FinanceNewsCollector;
