import requests
from bs4 import BeautifulSoup
from lxml import etree

s = requests.Session()
for id in range(0, 251, 25):
    url = 'https://movie.douban.com/top250/?start=' + str(id)
    r = s.get(url)
    r.encoding = 'utf-8'
    root = etree.HTML(r.content)
    items = root.xpath('/html/body/div[3]/div[1]/div/div[1]/ol/li/div')
    #print(len(items))
    for item in items:
        title = item.xpath('div[2]/div[1]/a/span[1]/text()')[0]
        rank = item.xpath('div[2]/div[2]/div/span[2]/text()')[0]
        print(title, rank)

