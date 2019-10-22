# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging

class WebvpnPipeline(object):
    def process_item(self, item, spider):
        logging.info('--------------------------wuhonglei-------------------start-------------------')
        logging.info(spider)
        logging.info('--------------------------wuhonglei-------------------end-------------------')
        return item
