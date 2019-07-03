import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pymysql

conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="abcd1234", db="Lagou", charset="utf8mb4")
cursor = conn.cursor()

class Lagou(object):

    def __init__(self, search_name):
        self.start_url = "https://www.lagou.com/jobs/list_{}?px=default&city=%E4%B8%8A%E6%B5%B7"
        self.search_name = search_name
        self.firefox_options= Options()
        #self.firefox_options.set_headless(True)
        self.firefox_options.add_argument('-headless')
        self.driver = webdriver.Firefox(options=self.firefox_options)

    def get_content_list(self):  # 提取并保存数据
        li_list = self.driver.find_elements_by_xpath('//li[contains(@class, "con_list_item")]')
        for li in li_list:
            item={}
            item["positionName"]=li.find_element_by_tag_name("h3").text
            item["businessZones"]=li.find_element_by_tag_name("em").text
            item["CreateTime"]=li.find_elements_by_xpath(".//span[@class='format-time']")[0].text
            item["companyShortName"]=li.find_elements_by_xpath(".//div[@class='company_name']")[0].text
            item["salary"]=li.find_elements_by_xpath(".//span[@class='money']")[0].text
            item["workYear"]=li.find_elements_by_xpath(".//div[@class='li_b_l']")[0].text
            self.to_mysql(item)

        # 下一页
        next_url = self.driver.find_elements_by_xpath("//span[@class='pager_next ']")
        next_url = next_url[0] if len(next_url) > 0 else None
        return  next_url

    def to_mysql(self, data):
        """
       插入操作，存入数据库
       :param data:
       :return:
       """
        # 构造插入命令
        command = 'insert into lagoudata values("{0}", "{1}", "{2}", "{3}", "{4}", "{5}")'.format( \
            data["positionName"], data["businessZones"], data["CreateTime"], data["companyShortName"], data["salary"], data["workYear"])
        print(command)
        try:
            cursor.execute(command)
        except TypeError as e:
            print(e)
        # 无意外提交数据
        conn.commit()

    def run(self):

        # 发送请求
        self.driver.get(self.start_url.format(self.search_name))
        # 提取数据
        next_url = self.get_content_list()

        # 翻页
        while next_url is not None:
            next_url.click()
            time.sleep(6)
            next_url = self.get_content_list()
            #self.to_mysql(content_list)





if __name__ == '__main__':
    lagou = Lagou("数据分析")
    lagou.run()
    cursor.close()
    conn.close()
    # 翻页