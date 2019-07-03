import scrapy

class CnBlogSpider(scrapy.Spider):
    name = 'cnblog'
    start_urls = ['https://www.cnblogs.com/pick/#p%s' %p for p in range(1, 21)]

    def parse(self, response):
        for blog in response.xpath('/html/body/div/div[4]/div[6]/div'):
            #diggit = blog.xpath('//*[@id="digg_count_*"]/text()').extract_first()
            diggit = blog.xpath('div[@class="digg"]/div/span/text()').extract_first()
            title = blog.xpath('div[@class="post_item_body"]/h3/a/text()').extract_first()
            yield {'diggit': diggit, 'title': title}


#scrapy runspider CnBlogSpider.py -o blog.json