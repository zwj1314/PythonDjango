import scrapy
from Itcast.items import ItcastItem

# 声明一个爬虫类
class TeacherCrawl(scrapy.Spider):
    # 爬虫名称
    name = "teacher"
    allowd_domains = ["http://www.itcast.cn"]
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml#aios', 'http://www.itcast.cn/channel/teacher.shtml#ajavaee']


    def parse(self, response):
            teacherInfo = []
            # xpath返回的一定是一个list类型
            for item in response.xpath('//div[@class="li_txt"]'):
                teacher = ItcastItem()
                # 在scrapy中使用xpath，想取出其中参数的值，使用extract将对象转化为Unicode字符串
                teacher['name'] = item.xpath('./h3/text()').extract()[0]
                teacher['title'] = item.xpath('./h4/text()').extract()[0]
                teacher['info'] = item.xpath('./p/text()').extract()[0]

                teacherInfo.append(teacher)

            return teacherInfo



