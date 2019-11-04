## 背景
1. webvpn 方案大量涉及 url 地址的处理，即需要对 HTML、CSS 文件内容使用正则表达式匹配其中的 url，因此合适的正则能够优化反向代理服务器的性能。
2. 对于 location 的处理需要依赖后台进行替换，即匹配拥有属性 protocol、hostname、host、port、origin的对象，同样这需要准确的正则来进行匹配。

从背景可以看出，我们需要大量的站点样本来验证正则的有效性，因此该爬虫程序用于爬取站点HTML、CSS、JS 文件，提供后续分析。

## 结构说明
数据使用 mongodb 存储，字段如下

```python
domain # 请求主机地址, list 类型
filetype # 文件类型
filepath # 文件路径
filename # 文件名称
filesize #文件大小
body # 文件内容
md5 # 文件 hash 值，用于唯一区分文件
count # 文件使用次数（以站点为单位）
```

## TODO
1. 将爬虫在线部署，同时使用在线数据库
2. 开发一个查询页面，可以进行内容检索
3. 数据存储时，根据文件 md5 值进行去重
4. 如何统计

## 使用
1. 运行爬虫程序
```bash
scrapy crawl example
```