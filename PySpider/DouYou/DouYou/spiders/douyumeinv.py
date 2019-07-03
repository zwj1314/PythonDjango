# -*- coding: utf-8 -*-
import scrapy
import json
from DouYou.items import DouyouItem

class DouyumeinvSpider(scrapy.Spider):
    name = 'douyumeinv'
    allowed_domains = ['capi.douyucdn.cn']
    offset = 0
    url = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset="

    start_urls = [url + str(offset)]

    def parse(self, response):
        # json -> python loads /data是列表
        data = json.loads(response.text)["data"]
        for each in data:
            # 现在循环遍历的是列表的第一个
            item = DouyouItem()
            item["nickname"] = each["nickname"]
            item["imageLink"] = each["vertical_src"]


            yield item

        self.offset += 20
        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
