import scrapy
from DouBanBook.items import LagouItem
import json


class LaGou(scrapy.Spider):
    name = 'lagou'
    pn = 1
    kd = 'python'
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false'

    headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537',
    #'Cookie': 'JSESSIONID=ABAAABAAADEAAFICA6B17EFEC6D8CE0AAD22E8EF120CEF7; _ga=GA1.2.744426291.1559353239; _gid=GA1.2.1071297619.1559353239; user_trace_token=20190601094039-427f6f58-840e-11e9-a88b-525400f775ce; LGUID=20190601094039-427f7215-840e-11e9-a88b-525400f775ce; index_location_city=%E4%B8%8A%E6%B5%B7; X_MIDDLE_TOKEN=dba82ba417de704ca532b4279fbe5c1f; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1559353239,1559353511; X_HTTP_TOKEN=c121ce0e3996cde3207373955104baa94f1f798fb5; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1559373702; LGSID=20190601152142-e7a9ad65-843d-11e9-a197-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGRID=20190601152142-e7a9b0c5-843d-11e9-a197-5254005c3644; TG-TRACK-CODE=index_search; SEARCH_ID=1d1fcf59dd5d458b9710a08936d0531d',
    'Cookie':'JSESSIONID=ABAAABAAADEAAFICA6B17EFEC6D8CE0AAD22E8EF120CEF7; _ga=GA1.2.744426291.1559353239; _gid=GA1.2.1071297619.1559353239; user_trace_token=20190601094039-427f6f58-840e-11e9-a88b-525400f775ce; LGUID=20190601094039-427f7215-840e-11e9-a88b-525400f775ce; index_location_city=%E4%B8%8A%E6%B5%B7; X_MIDDLE_TOKEN=dba82ba417de704ca532b4279fbe5c1f; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1559353239,1559353511; LGSID=20190601152142-e7a9ad65-843d-11e9-a197-5254005c3644; LG_LOGIN_USER_ID=fce4175a4fabd7bccc86dca6251bad5b6566de9f0f80585fd9d044bf6c090cca; LG_HAS_LOGIN=1; _putrc=72BC98F4C48442A9123F89F2B170EADC; login=true; unick=%E5%BC%A0%E5%89%91; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=4; gate_login_token=bf5d7c58b8c1672f8a0edc3a74f6e34085988c3fdad5703f71275953250eac03; SEARCH_ID=e50c63dda23944b18bd954f5f46e7118; X_HTTP_TOKEN=c121ce0e3996cde3174973955104baa94f1f798fb5; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1559379471; LGRID=20190601165752-568ca325-844b-11e9-a197-5254005c3644; TG-TRACK-CODE=search_code',
    'Host':'www.lagou.com',
    'Referer':'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': 'None',
    'X-Requested-With': 'XMLHttpRequest'
    }

    def start_requests(self):
        data = {
            "first" : "true",
            "pn": str(self.pn),
            "kd": self.kd
        }

        yield scrapy.FormRequest(
            url = self.url,
            headers=self.headers,
            formdata=data,
            callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        print(data)
        data_position = data['content']['positionResult']
        data_result = data_position['result']
        # self.total_page = data_position['totalCount']
        for i in range(len(data_result)):
            item = LagouItem()
            item['salary'] = data_result[i]['salary']
            item['city'] = data_result[i]['city']
            item['workYear'] = data_result[i]['workYear']
            item['education'] = data_result[i]['education']
            item['industryField'] = data_result[i]['industryField']
            item['companySize'] = data_result[i]['companySize']
            item['positionName'] = data_result[i]['positionName']
            sal = data_result[i]['salary']
            sal = sal.split('-')
            if len(sal)==1:
                item['salary_min'] = sal[0][:sal[0].find('k')]
                item['salary_max'] = sal[0][:sal[0].find('k')]
            else:
                item['salary_min'] = sal[0][:sal[0].find('k')]
                item['salary_max'] = sal[1][:sal[1].find('k')]
            yield item

        #当前页数小于总页数，那么我们就继续请求下一页，再爬取
        if self.pn <= 30:
            print("pn：{}    运行中请勿打断...".format(self.pn+1))
            self.pn +=1
            yield scrapy.FormRequest(
                url = self.url,
                headers=self.headers,
                formdata=data,
                callback=self.parse)



