import requests
from lxml import etree
import json

url = "https://www.qiushibaike.com/text/page/1/"

headers = {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"}

response = requests.get(url, headers=headers).text

# 响应返回的是字符串，解析为HTML_DOM模式
text = etree.HTML(response)

"""
模糊查询，作为根节点
//*[@id="qiushi_tag_121791125"]
//*[@id="qiushi_tag_121794574"]
//*[@id="qiushi_tag_121793316"]

//div[contains(@id, "qiushi_tag")] contains()模糊查询方法，第一个参数是要匹配的标签，第二个参数是标签名部分内容
"""
node_list = text.xpath('//div[contains(@id, "qiushi_tag")]')
item = {}
for node in node_list:
    # 用户名
    username = node.xpath('./div/a[2]/h2/text()')[0].strip()
    # 段子内容
    content = node.xpath('./a/div/span/text()')
    # 点赞
    image = node.xpath('./div/a[1]/img/@src')
    # 评论
    item = {
        "username" : username,
        "content" : content,
        "image" : image
    }

    with open("qiushi.json", "a+") as f:
        f.write(json.dumps(item, ensure_ascii=False))


