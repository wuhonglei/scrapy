# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebvpnItem(scrapy.Item):
    # define the fields for your item here like:
    filetype = scrapy.Field()
    filepath = scrapy.Field()
    filename = scrapy.Field()
    filesize = scrapy.Field()
    body = scrapy.Field()
