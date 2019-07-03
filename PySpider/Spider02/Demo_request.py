import requests
from PIL import Image
from io import BytesIO

"""
二进制数据
"""

r = requests.get('https://img.alicdn.com/bao/uploaded/i2/527378066/O1CN0129SH8RRPlXGb7Uf_!!527378066.jpg_250x250.jpg')
image = Image.open(BytesIO(r.content))
image.save('sw.jpg')


"""
原始数据处理
"""
r = requests.get('https://img.alicdn.com/imgextra/i4/763807986/TB2uW0JaWigSKJjSsppXXabnpXa_!!763807986.png_250x250.jpg')
with open('sw2.jpg', 'wb+') as f:
    for chunk in r.iter_content(1024):
        f.write(chunk)


"""
提交表单
"""
form = {'username':'user', 'password':'pass'}
r = requests.post('http://httpbin.org/post', data=form)
print(r.text)

"""
cookie
"""
url = 'http://www.baidu.com'
r = requests.get(url)
cookies = r.cookies
for k, v in cookies.get_dict().items():
    print(k, v)

"""
代理
"""
proxies = {'http': ',,,', 'https': ',,,'}
r = requests.get('http://www.baidu.com', proxies=proxies)

