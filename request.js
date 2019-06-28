/**
 * Example1：
 * 获取掘金首页上热门技术标题
 */
const superagent = require('superagent');
const cheerio = require('cheerio')

var feeds = ['https://juejin.im/timeline'], // html 页面
	page;

while (page = feeds.pop()) {
	requestPage('https://www.baidu.com/');
}


/**
 * 请求页面
 * @param {string} url 
 */
function requestPage(url) {
	superagent
		.get(url)
		.end((err, res) => {
			if (err) {
				return console.error('error', err);
			}

			const $ = cheerio.load(res.text);
			console.info($('.mnav').length)
			// console.info('--------------------------------------------')
			// console.info($('.item .title').text());
		});
}