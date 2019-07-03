# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Dongguan01Item(scrapy.Item):
    title = scrapy.Field()
    number = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()


class Jb51Item(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()

