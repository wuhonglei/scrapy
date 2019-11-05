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
            print(name)

    def parse_lib(self, response):
        '''解析具体某个库信息'''
