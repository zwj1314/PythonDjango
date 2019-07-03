import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


def get_province_entry(url):
    content = requests.get(url).content.decode('gb2312')
    #print(content)
    start = content.find('<map name=\"map_86\" id=\"map_86\">')
    end = content.find('</map>')
    #print(start, end)
    content = content[start:end + len('</map>')].strip()
    #print(content)


provinces = get_province_entry('http://www.ip138.com/post')
print(provinces)