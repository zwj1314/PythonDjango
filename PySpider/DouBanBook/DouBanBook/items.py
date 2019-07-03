# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouBanbookItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    edition_year = scrapy.Field()
    publisher = scrapy.Field()
    ratings = scrapy.Field()


class LagouItem(scrapy.Item):
    salary = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    city = scrapy.Field()
    workYear = scrapy.Field()
    education = scrapy.Field()
    industryField = scrapy.Field()
    companySize = scrapy.Field()
    positionName = scrapy.Field()

class DoubanMailItem(scrapy.Item):
    sender_time = scrapy.Field()
    sender_from = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()