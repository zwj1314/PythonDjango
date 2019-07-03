# -*- coding: utf-8 -*-
import scrapy
from DongGuan01.items import Dongguan01Item


class DongguanV1Spider(scrapy.Spider):
    name = 'dongguan_v1'
    allowed_domains = ['wz.sun0769.com']
    url = 'http://wz.sun0769.com/index.php/question/report?page='
    offset = 0
    start_urls = [url + str(offset)]

    def parse(self, response):
        # 进来首页第一步是拿到每个帖子的URL链接地址，
        for link in response.xpath('//div[@class="greyframe"]/table//td/a[@class="news14"]/@href').extract():
            # 对每一个帖子的链接地址都调用内容解析函数来解析
            yield scrapy.Request(link, callback= self.parse_content)

        # 判断是否是最后一页，如不是则递增的URL放入URL队列中，继续调用URL解析函数，重复此过程
        if self.offset <= 71160:
            self.offset += 30
            yield scrapy.Request(self.url+str(self.offset), callback= self.parse)

    def parse_content(self, response):
        for each in response.xpath('//div[@class="wzy1"]'):
            item = Dongguan01Item()
            # 标题
            item['title'] = each.xpath('.//span[@class="niae2_top"]/text()').extract()[0]
            # 编号
            number = each.xpath('./table[1]/tr/td[2]/span[2]/text()').extract()
            if len(number) != 0:
                item['number'] = number[0].split(':')[-1]
            else:
                pass
            # 内容 有图片的内容与无图片的内容显示位置不一致，先判断图片的内容是否为空，若不为空则显示有图片的content，若为空则显示无图片的content
            content = each.xpath('.//div[@class="contentext"]/text()').extract()
            if len(content) == 0:
                # 若无图片，则提取无图片的内容
                item['content'] = "".join(each.xpath('.//td[@class="txt16_3"]/text()').extract()).strip()
            else:
                item['content'] = "".join(content).strip()

            item['url'] = response.url

            yield item









