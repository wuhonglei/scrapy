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

## 开源库
响应特征：
1. 文件头部含有多行注释，说明了库的基本信息和版本
    - 压缩版本，可能在一行，也可能在多行显示注释信息
    - 未压缩版，在多行显示注释信息

以 `vue` 为例进行说明。
文件 vue.esm.browser.js 的响应内容如下：

```javascript
/*!
 * Vue.js v2.6.10
 * (c) 2014-2019 Evan You
 * Released under the MIT License.
 */
/*  */
```

文件 vue.esm.browser.min.js 的响应内容如下：

```javascript
/*!
 * Vue.js v2.6.10
 * (c) 2014-2019 Evan You
 * Released under the MIT License.
 */
```

思路：提取文件多行注释内容，将注释作为文件的唯一特征，如果注释内容相同，证明是同一文件，在 webvpn 优化时，可以使用外网 CDN 代替内容资源的域名，尤其是外文站点可以进行优化。

## 如何爬取开源库
> 将以下 API 链接中的 .min 字样去掉之后，获取到的 JSON 格式的返回信息是经过良好格式化的，便于人眼查看。

1. 获取开源库名称列表：`https://api.bootcdn.cn/names.min.json`
格式如下：该列表是一个 json 数组（Array），包含了所有开源库的名称（name）。
```json
// 20191105001042
// https://api.bootcdn.cn/names.min.json

[
  "twitter-bootstrap",
  "vue",
  "react",
  "react-dom",
  "d3",
  "angular.js",
  "angular-touch",
  ...
]
```

2. 获取某个开源库的详细信息
> https://api.bootcdn.cn/libraries/[name].min.json

通过此接口获取到的是开源库的 JSON 对象（Object）格式的详细信息，包括所有版本以及文件列表。`[name]` 是开源库的名称，可从`[开源库简要信息列表]` 或 `[开源库名称列表]`中获取。其中，`asset` 属性是所有版本及对应文件的列表。
以 `jquery` 为例，该请求为 `https://api.bootcdn.cn/libraries/jquery.min.json` 的响应内容如下, 3.3.1 版本的 `core.js` 文件的下载路径是：`https://cdn.bootcss.com/jquery/3.3.1/core.js`


```json
{
  "name": "jquery",
  "npmName": "jquery",
  "version": "3.3.1",
  "description": "JavaScript library for DOM operations",
  "homepage": "http://jquery.com/",
  "keywords": [
    "jquery",
    "library",
    "ajax",
    "framework",
    "toolkit",
    "popular"
  ],
  "namespace": "jQuery",
  "repository": {
    "type": "git",
    "url": "https://github.com/jquery/jquery.git"
  },
  "license": "MIT",
  "assets": [
    {
      "version": "3.3.1",
      "files": [
        "core.js",
        "jquery.js",
        "jquery.min.js",
        "jquery.slim.js",
        "jquery.slim.min.js"
      ]
    },
    ...
  ]
```
