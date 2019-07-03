# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from TencentLinkExtract.items import TencentlinkextractItem

class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?&start=0#a']

    # Response中链接的提取规则，返回符合匹配规则的链接匹配对象列表
    rules = (
        Rule(LinkExtractor(allow=("start=\d+")), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=("position?php")), callback='parse_position', follow=True),
    )

    def parse_item(self, response):
        for each in response.xpath('//tr[@class="even"] | //tr[@class="odd"]'):
            item = TencentlinkextractItem()

            yield item
