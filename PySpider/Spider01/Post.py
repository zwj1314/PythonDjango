from flask import Flask
import urllib

url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"

headers = {
    "Host" : "fanyi.youdao.com",
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "Accept-Language" : "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With" : "XMLHttpRequest",
    "Cookie" : "YOUDAO_MOBILE_ACCESS_TYPE=1; OUTFOX_SEARCH_USER_ID=-1951093456@10.168.8.61; JSESSIONID=aaa88SoAmwlKBdTP7WLHw; ___rl__test__cookies=1547906748870; OUTFOX_SEARCH_USER_ID_NCOO=235863903.83871564",
    "DNT" : "1",
    "Connection" : "keep-alive"
}

key = input("请输入要翻译的内容:")

formdata = {
    "i" : key,
    "from" : "AUTO",
    "to" : "AUTO",
    "smartresult" : "dict",
    "client" : "fanyideskweb",
    "salt" : "15479067488829",
    "sign" : "15ac18de994d6be5efef5ece0f4496ed",
    "ts" : "1547906748882",
    "bv" : "abf85f8020851128b561472c8a7b924d",
    "doctype" : "json",
    "version" : "2.1",
    "keyfrom" : "fanyi.web",
    "action" : "FY_BY_CLICKBUTTON",
    "typoResult" : "true"
}



data = urllib.parse.urlencode(formdata)

request = urllib.request.Request(url, data = data.encode(encoding='UTF8'), headers = headers)

print(urllib.request.urlopen(request).read())