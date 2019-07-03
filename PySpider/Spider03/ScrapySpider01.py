import scrapy

class ScrapySpider(scrapy.Spider):
    name = 'spider'
    start_urls = ['https://www.julyedu.com/category/index']

    def parse(self, response):
        for julyedu_class in response.xpath('/html/body/div[1]/div[3]/div/div/div/div/div'):
            title = julyedu_class.xpath('a[1]/h4/text()').extract_first().strip()
            describe = julyedu_class.xpath('a[1]/p[1]/text()').extract_first().strip()
            time = julyedu_class.xpath('a[1]/p[2]/text()').extract_first().strip()
            #print(title)
            yield {'title': title, 'describe': describe, 'time': time}


 

#scrapy runspider ScrapySpider01.py -o julyedu_class.json