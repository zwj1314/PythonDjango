import scrapy

class JokeSpider(scrapy.Spider):
    name = 'JokeSpider'
    start_urls = ['http://quotes.toscrape.com/tag/humor/']

    def parse(self, response):
        for joke in response.xpath('/html/body/div/div[2]/div[1]/div'):
            content = joke.xpath('span[1]/text()').extract_first()
            autor = joke.xpath('span[2]/small/text()').extract_first()
            yield {'content': content, 'autor': autor}

        #注意：如果这样写的话，最后一个页面还是会有上一个页面的href，导致第一个页面再会调用一次
        #next_page = response.xpath('/html/body/div/div[2]/div[1]/nav/ul/li/a/@href').extract_first()
        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)




#scrapy runspider JokeSpider.py -o joke.json
