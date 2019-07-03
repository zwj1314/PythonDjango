import unittest
from selenium import webdriver
from bs4 import BeautifulSoup
import time

class DouYu(unittest.TestCase):
    # 初始化方法
    def setUp(self):
        self.driver  = webdriver.Firefox()
        self.num = 0 # 初始化主播房间数
        self.count = 0 # 初始化观看人数

    # 测试方法必须有test字样开头
    def testDouyu(self):
        self.driver.get("https://www.douyu.com/directory/all")
        while True:
            soup = BeautifulSoup(self.driver.page_source, "lxml")
            # 房间名，返回列表
            names = soup.find_all("h3", {"class" : "DyListCover-intro"})
            # 观看人数，返回列表
            numbers = soup.find_all("span", {"class" : "DyListCover-hot"})

            for name, number in zip(names, numbers):
                print("观众人数：" + number.get_text().strip() + "\t" + "房间名：" + name.get_text().strip())
                self.num += 1
                count = number.get_text().strip()
                if count[-1] == "万":
                    countNum = float(count[:-1]) * 10000
                else:
                    countNum = float(count)
                self.count += countNum
            time.sleep(5)
            if self.driver.page_source.find("dy-Pagination-disabled dy-Pagination-next") != -1:
                break
            #self.driver.find_element_by_class_name(" dy-Pagination-next").click()
            #self.driver.find_element_by_xpath('/html/body/section/main/section[2]/div[2]/div/ul/li[9]').click()
            #self.driver.find_element_by_class_name("dy-Pagination-jump-next").click()
            self.driver.find_element_by_xpath('//li[@class=" dy-Pagination-next"]').click()

    def tearDown(self):
        print(self.num)
        print(self.count)
        self.driver.quit()

if __name__ == '__main__':
    # 启动测试模块
    unittest.main()



