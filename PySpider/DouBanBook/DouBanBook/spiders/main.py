from scrapy import cmdline

# cmdline.execute("scrapy crawl teacher -o itcast.json".split())
# cmdline.execute("scrapy runspider BookSpider.py -o book_info.csv".split())
# cmdline.execute("scrapy crawl douban_book_v3".split())
# cmdline.execute("scrapy crawl douban_book".split())
#cmdline.execute("scrapy crawl lagou".split())
cmdline.execute("scrapy crawl douban-mailv2 -o douyou.json".split())