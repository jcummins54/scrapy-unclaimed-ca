# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UnclaimedItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    recid = scrapy.Field()
    date = scrapy.Field()
    source = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    type = scrapy.Field()
    cash = scrapy.Field()
    reportedby = scrapy.Field()
    pass
