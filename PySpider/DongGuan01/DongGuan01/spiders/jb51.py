# -*- coding: utf-8 -*-
import scrapy
from DongGuan01.items import Jb51Item



class Jb51Spider(scrapy.Spider):
    name = 'jb51'
    allowed_domains = ['jb51.net']
    start_urls = [
        "http://www.jb51.net/list/index_1.htm"
    ]
    url = 'https://www.jb51.net/'
    list_url = "http://www.jb51.net/list/list_%d_%d.htm"

    def parse(self, response):
        # 进入start_urls后，首先拿到其他要爬取页面的链接
        for link in response.xpath('//div[@class="artlistBar border"]//span/a/@href').extract():
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        # 处理第一页
        for link in response.xpath('//div[@class="artlist clearfix"]//dt/a/@href').extract():
            article_url = self.url + link
            yield scrapy.Request(article_url, callback=self.parse_content)

        # 处理其他页
        #_params = response.selector.xpath('//div[@class="dxypage clearfix"]/a[last()]/@href').re('(\d+)')
        _params = response.xpath('//div[@class="dxypage clearfix"]/a[last()]/@href').extract_first().split('.')[0].split('_')
        if len(_params) == 3:
            cate_id = int(_params[1]) #分类编号
            count = int(_params[2]) #总页数
            for page in range(1, count):
                url = (self.list_url % (cate_id, page + 1))
                yield scrapy.Request(url, callback=self.parse_list)


    def parse_list(self, response):
        for link in response.xpath('//div[@class="artlist clearfix"]//dt/a/@href').extract():
            article_url = self.url + link
            yield scrapy.Request(article_url, callback=self.parse_content)


    def parse_content(self, response):
        item = Jb51Item()
        item['title'] = response.xpath('//div[@class="title"]/h1/text()').extract()[0]
        item['content'] = response.xpath('//div[@id="content"]').extract()[0]
        item['url'] = response.url
        item['tags'] = ','.join(response.xpath('//ul[@class="meta-tags items"]//a/text()').extract())
        yield item


        # #使用正则表达式去除标点符号
        # pattern = re.compile(r'[\u4e00-\u9fa5]+')
        # filterdata = re.findall(pattern, comments)
        # cleaned_comments = ''.join(filterdata)





