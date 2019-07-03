from flask import Flask
import urllib


#url = "http://www.baidu.com/"
# headers = "User-Agent":"Morl.."
#
# request = urllib.request.Request(url)
#
# response = urllib.request.urlopen(request)
#
#
# print(response.read())
#
# print(urllib.parse.urlencode({"wd":"唱着"}))

def loadPage(url, filename):
    """
    :param url: 需要爬取的url地址
    :return: 根据url获取请求，得到服务器的响应文件
    """
    print("正在下载" + filename)
    headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X "}
    request = urllib.request.Request(url, headers = headers)
    return urllib.request.urlopen(request).read()

def writePage(html, filename):
    """
    :param html: 服务器响应文件内容
    :return: 将html内容写入到本地
    """
    print("正在保存" + filename)
    with open(filename, "wb+") as f:
        f.write(html)
    print("--"*30)


def tiebaSpider(url, beginPage, endPage):
    """
    :param url:贴吧的url
    :param beginPage:起始页
    :param endPage:结束页
    :return:贴吧爬虫调度器，负责处理组合每个页面的url
    """
    for page in range(beginPage, endPage+1):
        pn = (page-1)*50
        filename = "第" + str(page) + "页.html"
        fullurl = url + "&pn=" + str(pn)
        # print(fullurl)
        html = loadPage(fullurl, filename)
        # print(html)
        writePage(html, filename)


if __name__ == '__main__':
    kw = input("请输入要爬取的贴吧关键字:")
    beginPage = int(input("请输入起始页:"))
    endPage = int(input("请输入结束页:"))

    url = "http://tieba.baidu.com/f?"
    key = urllib.parse.urlencode({"kw": kw})
    fullurl = url + key
    tiebaSpider(fullurl, beginPage, endPage)





