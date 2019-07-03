# -*- coding: utf-8 -*-
import scrapy
from AVList.items import AvlistItem


class AvmeinvSpider(scrapy.Spider):
    name = 'avmeinv_9570'
    allowed_domains = ['9570.site']
    #url = "https://99zxtg.com/"
    #start_urls = ['http://9570.site/zaixianshipin/qiangjianluanlun/list_24_1.html']
    start_urls = ['http://9570.site/zaixianshipin/zhongwenzimu/list_25_1.html']

    def parse(self, response):
        for each in response.xpath('//div[@class="vod_list clearfix"]/a'): #这里是一个列表
            item = AvlistItem()
            item["title"] = each.xpath('./h2/text()').extract()[0]
            item["imageLink"] = each.xpath('./div/img/@src').extract()[0]
            yield item

        # 完成第二件事：获取所有后面页面的URL地址，调用解析函数进行解析
        for page in response.xpath('//div[@class="page"]'):
            link = response.urljoin(page.xpath('./li[last()-1]/a/@href').extract()[0])


        # 完成第一件事：对当前的页面调用解析函数进行解析.
        yield scrapy.Request(link, callback=self.parse)





