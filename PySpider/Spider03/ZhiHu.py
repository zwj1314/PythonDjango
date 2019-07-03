from bs4 import BeautifulSoup
import requests
import time

def captcha(captcha_data):
    with open("captcha.jpg", "wb") as f:
        f.write(captcha_data)
    text = input("请输入验证码：")
    return text

def ZhiHuLogin():
    # 构建一个Session对象，可以保存Cookie
    sess = requests.Session()

    #IE 9 'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);'
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

    #首先获取到登陆页面，找到需要post的数据(_xsrf)，同时回记录当前网页的Cookie值
    html = sess.get("https://www.zhihu.com/signin", headers = headers).text
    soup = BeautifulSoup(html, "lxml")
    _xsrf = soup.find("input", attrs={"name":"_xsrf"}).get("value")
    #print(_xsrf)

    captcha_url = "https://www.zhihu.com/captcha.gif?r=%d&type=login" % (time.time() * 1000)
    # 发送图片的请求，获取图片数据流
    captcha_data = sess.get(captcha_url, headers = headers).content

    # 获取验证码中的文字，需要手动输入
    text = captcha(captcha_data)

    data = {
        "_xsrf":_xsrf,
        "email":"zjusst2016@163.com",
        "password":"zjusst2016@163.com",
        "captcha":text
    }
    response = sess.post("https://www.zhihu.com/login/email", data=data, headers=headers)
    #print(response.text)

    #post之后已经拿到cookie数据，之后访问需要登陆后才可以访问的页面，只需要get就可以了
    response = sess.get("https://www.zhihu.com/people/maozhaojun/activities", headers=headers)
    with open("my.html", "w") as f:
        f.write(response.text).encode("utf-8")



if __name__ == '__main__':
    ZhiHuLogin()