# -*- coding: utf-8 -*-
import scrapy
from AVList.items import AvlistItem


class AvmeinvSpider(scrapy.Spider):
    name = 'avmeinv'
    allowed_domains = ['99zxtg.com']
    #url = "https://99zxtg.com/"
    start_urls = ['https://99zxtg.com/jjzy/?s=vod-show-id-11-p-%s.html' %p for p in range(1, 175)]

    def parse(self, response):
        for each in response.xpath('/html/body/div[13]/ul/li'):
            item = AvlistItem()
            item["title"] = each.xpath('./div[1]/p/a/text()').extract()[0]
            item["imageLink"] = each.xpath('./div[1]/a/img/@src').extract()[0]

            yield item




