# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
import logging

from posixpath import join as urljoin
import os


class BootcdnPipeline(object):

    lib_name_collection_name = 'lib_name'
    lib_desc_collection_name = 'lib_desc'
    lib_detail_collection_name = 'lib_detail'

    base_url = 'https://cdn.bootcss.com'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.save_lib_name(item)
        self.save_lib_desc(item)
        self.save_download_urls(item)
        return item

    def save_lib_desc(self, item):
        '''保存某开源库的详细信息'''
        self.db[self.lib_desc_collection_name].insert_one(dict(item))

    def save_lib_name(self, item):
        '''保存某库的名称'''
        data = {'name': item.get('name')}
        self.db[self.lib_name_collection_name].insert_one(dict(data))

    def save_download_urls(self, item):
        '''
        保存待爬取的 url 地址，可用于断点爬取
        '''
        name = item.get('name')
        for version_list in item.get('assets'):
            version = version_list.get('version')
            for filename in version_list.get('files'):
                url = urljoin(self.base_url, name, version, filename)
                data = {
                    'url': url,  # 下载链接(唯一)
                    'version': version,  # 版本
                    'library': name,  # 库名称,例如 jquery
                    'filename': os.path.basename(filename),
                    'downloaded': False,  # 标记是否已经被爬取
                    'detail': {  # 详细结果

                    }
                }
                self.db[self.lib_detail_collection_name].insert_one(dict(data))
