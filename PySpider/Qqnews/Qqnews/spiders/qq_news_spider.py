import scrapy
#from Qqnews.Qqnews.items import QqnewsItem

class QQNewsSpider(scrapy.Spider):
    name = 'qqnews'
    start_urls = ['https://new.qq.com/ch/emotion/']
    #start_urls = ['https://new.qq.com/omn/20190418/20190418A0K3FX.html']

    def parse(self, response):
        for url in response.xpath('//*[@id="List"]/div/div[2]/ul/li/a/@href'):
            print(url)
             #full_url = response.urljoin(url.extract())
            full_url = url.extract()
            yield scrapy.Request(full_url, callback=self.parse_news())


    def parse_news(self, response):
        #item = QqnewsItem()
        print(response.xpath('/html/body/div[3]/div[1]/h1/text()').extract()[0])

        # item['title'] = response.xpath('')
        # item['source'] = response.xpath('')
        # item['text'] = response.xpath('')


#scrapy runspider qq_news_spider.py