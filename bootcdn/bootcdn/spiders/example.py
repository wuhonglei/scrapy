# -*- coding: utf-8 -*-
import scrapy
import json


class ExampleSpider(scrapy.Spider):
    name = 'example'
    # allowed_domains = ['example.com']
    start_urls = ['https://api.bootcdn.cn/names.min.json']

    def parse(self, response):
        name_list = json.loads(response.body)
        for name in name_list:
            yield response.follow(self.get_next_page(name), callback=self.parse_lib)

    def parse_lib(self, response):
        '''解析具体某个库信息'''
        info = json.loads(response.body)
        yield info

    def get_next_page(self, name):
        '''获取某个库的请求地址'''
        return 'https://api.bootcdn.cn/libraries/{name}.min.json'.format(name=name)
