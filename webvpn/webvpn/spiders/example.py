# -*- coding: utf-8 -*-
import os
from urlparse import urlparse

import scrapy
from webvpn.items import WebvpnItem


class ExampleSpider(scrapy.Spider):
    name = 'example'
    start_urls = ['http://www.baidu.com/']
    selector = {
        'css': 'link[rel=stylesheet][href]::attr(href)',
        'script': 'script[src]::attr(src)',
        'a': 'a[href]::attr(href)'
    }

    def parse(self, response):
        for link in response.css(self.selector.get('css')).getall():
            yield response.follow(link, callback=self.save_response)
        
        for script in response.css(self.selector.get('script')).getall():
            yield response.follow(script, callback=self.save_response)

        self.save_response(response)
        for next_page in response.css(self.selector.get('a')).getall():
            if 'javascript' not in next_page:
                yield response.follow(next_page, callback=self.parse)


    def save_response(self, response):
        '''保存css，含有 filetype、filepath、filename、filesize和body'''
        item = WebvpnItem()
        item['filetype'] = 'css'
        item['filepath'] = response.url
        item['filename'] = self.get_filename(response.url)
        item['filesize'] = len(response.body)
        item['body'] = response.body
        yield item


    def get_filename(self, url):
        '''从路径中获取文件名'''
        uri = urlparse(url)
        return os.path.basename(uri.path)
