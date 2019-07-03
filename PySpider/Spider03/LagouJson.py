import requests
import json
import jsonpath

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
url = "http://www.lagou.com/lbs/getAllCitySearchLabels.json"
response = requests.get(url, headers=headers)
#print(response.text)
#取出json文件中的字符串内容，返回的格式是字符串
html = response.text

#把json形式的字符串转化为python格式的Unicode字符串
unicodestr = json.loads(html)

city_list = jsonpath.jsonpath(unicodestr, "$..name")
for city in city_list:
    print(city)

# 返回的Unicode字符串
array = json.dumps(city_list, ensure_ascii=False)

with open("lagou.json", "w") as f:
    f.write(array.encode("utf-8"))