import re
import requests
import time
import json
from PIL import Image
import http.cookiejar

headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    "Host":"www.zhihu.com",
    "Referer":"https://www.zhihu.com"
}

# 建立一个会话，可以把同一用户的不同请求联系起来，直到会话结束都会自动处理cookie
session = requests.Session()

# 建立LWPCookieJar实例，可以存Set-Cookie3类型的文件
# MozillaCookieJar类是存为'/.txt'格式的文件
session.cookies = http.cookiejar.LWPCookieJar("cookie")

# 若本地有cookie则不用post数据
try:
    session.cookies.load(ignore_discard=True)
except IOError:
    print('Cookie未加载')

def get_xsrf():
    """
    获取post参数_xsrf
    :return:
    """
    response = session.get('https://www.zhihu.com', headers=headers)
    content = response.text
    get_xsrf_pattern = re.compile(r'<input type="hidden" name="_xsrf" value=(.*?)"')
    _xsrf = re.findall(get_xsrf_pattern, content)[0]
    return _xsrf

def get_captcha():
    """
    获取验证码，手动输入后返回
    :return:
    """
    t = str(int(time.time() * 1000)) # 返回当前时间戳
    captcha_url = "http://www.zhihu.com/captcha.gif?r=" + t + "&type=login"
    response = session.get(captcha_url, headers=headers)
    with open('cptcha.gif', 'wb') as f:
        f.write(response.content)
    # pillow显示验证码
    image = Image.open('cptcha.gif')
    image.show()
    captcha = input("本次登陆需要输入验证码：")
    return captcha

def login(username, password):
    """
    输入自己的账号密码，模拟登陆知乎
    :param username:
    :param password:
    :return:
    """
    if re.match(r'\d{11}$', username):
        url = 'http://www.zhihu.com/login/phone_num'
        data = {
            '_xsrf':get_xsrf(),
            'password':password,
            'remember_me':'true',
            'phone_num':username
        }

    else:
        url = 'http://www.zhihu.com/login/email'
        data = {
            '_xsrf':get_xsrf(),
            'password':password,
            'remember_me':'true',
            'phone_num':username
        }

    # 若不用验证码，则直接登陆
    result = session.post(url, data=data, headers=headers)
    # 打印返回的响应结果，r=1代表响应失败，msg里是失败的原因。loads可以反序列化内置的数据类型，而load可以从文件读取
    if (json.loads(result.text))["r"] == 1:
        # 要用验证码登陆，post后登陆
        data['captcha'] = get_captcha()
        result = session.post(url, data=data, headers=headers)
        print((json.loads(result.text))['msg'])

    # 保存cookie到本地
    session.cookies.save(ignore_discard=True, ignore_expires=True)

def is_login():
    # 通过查看需要用户登陆后才能显示的信息来判断该用户是否已经登陆
    url = "https://www.zhihu.com/settings/profile"

    # 禁止重定向，否则登陆失败跳转到登陆界面，返回200
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code

    return True if login_code == 200 else False


if __name__ == '__main__':
    if is_login():
        print("您已经登陆")
    else:
        username = input("请输入账号：")
        password = input("请输入密码：")
        login(username, password)



