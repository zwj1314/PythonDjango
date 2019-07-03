import scrapy
from Tencent.items import TencentItem

class TencentJob(scrapy.Spider):
    name = "tencentJob"
    allowed_domain = ["tencent.com"]
    start_urls = ["http://www.tencent.com"]

    def parse(self, response):
        pass

