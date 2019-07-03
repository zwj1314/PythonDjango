# -*- coding: utf-8 -*-
import scrapy
from AVList.items import AvlistItem


class AvmeinvSpider(scrapy.Spider):
    name = 'avmeinv_v2'
    allowed_domains = ['99zxtg.com']
    #url = "https://99zxtg.com/"
    start_urls = ['https://99zxtg.com/jjzy/?s=vod-show-id-11-p-1.html']

    def parse(self, response):
        for each in response.xpath('/html/body/div[13]/ul/li'):
            item = AvlistItem()
            item["title"] = each.xpath('./div[1]/p/a/text()').extract()[0]
            item["imageLink"] = each.xpath('./div[1]/a/img/@src').extract()[0]
            yield item

        # 完成第二件事：获取所有后面页面的URL地址，调用解析函数进行解析
        for page in response.xpath('//a[@class="next pagegbk"]'):
            link = response.urljoin(page.xpath('./@href').extract()[0])


        # 完成第一件事：对当前的页面调用解析函数进行解析.
        yield scrapy.Request(link, callback=self.parse)





