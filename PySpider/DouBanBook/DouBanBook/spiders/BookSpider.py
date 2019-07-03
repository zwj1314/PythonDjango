import scrapy
from DouBanBook.items import DouBanbookItem



class BookSpider(scrapy.Spider):
    """docs for BookSpider"""
    name = 'douban_book'
    allowed_domain = ['douban.com']
    start_urls = ['https://book.douban.com/top250?start=0']

    """
    从初始页开始，需要完成两件事：
    1.对当前页进行解析
    2.获取下一页的URL，递归解析
    """
    def parse(self, response):
        #完成第一件事：对当前的页面调用解析函数进行解析.response.url='https://book.douban.com/top250'
        yield scrapy.Request(response.url, callback=self.parse_page)

        #完成第二件事：获取所有后面页面的URL地址，调用解析函数进行解析
        # for page in response.xpath('//*[@id="content"]/div/div[1]/div/div/a'):
        #     link = page.xpath('@href').extract()[0]
        #     yield scrapy.Request(link, callback=self.parse_page)
        nextPage = response.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract()
        if len(nextPage) != 0:
            yield scrapy.Request(nextPage[0], callback=self.parse, dont_filter=True) # 第二页在第一页执行到这里的时候已经发送到URL队列中，然后第二页在调用self.parse的时候又会发送请求


    def parse_page(self, response):
        for item in response.xpath('//tr[@class="item"]'): #每本书都对应一个class="item",response.xpath('//tr[@class="item"]')的返回结果有多个
            book = DouBanbookItem()
            #book['name'] = item.xpath('td[2]/div[1]/a/text()').extract()[0]
            book['name'] = item.xpath('td[2]/div[1]/a/@title').extract()[0] #extract是为了只提取想要的信息，[0]是每次
            book['ratings'] = item.xpath('td[2]/div[2]/span[2]/text()').extract()[0]
            book_info = item.xpath('td[2]/p[1]/text()').extract()[0]
            book_info_contents = book_info.strip().split(' / ')
            if len(book_info_contents) == 5:
                book['author'] = book_info_contents[0]
                book['publisher'] = book_info_contents[2]
                book['edition_year'] = book_info_contents[3]
                book['price'] = book_info_contents[4]
            elif len(book_info_contents) == 4:
                book['author'] = book_info_contents[0]
                book['publisher'] = book_info_contents[1]
                book['edition_year'] = book_info_contents[2]
                book['price'] = book_info_contents[-1]
            else:
                book['author'] = ''
                book['publisher'] = book_info_contents[-3]
                book['edition_year'] = book_info_contents[-2]
                book['price'] = book_info_contents[-1]

            yield book


    def parse_book(self, response):
        #TODO 解析每一本书的详细信息
        pass


# cd DouBanBook/DouBanBook -- scrapy runspider qq_news_spider.py


