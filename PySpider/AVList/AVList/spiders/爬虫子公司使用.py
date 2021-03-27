#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-10-7

@author: zhangjian
"""

import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import pymysql
from tqdm import tqdm
import numpy as np

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='119911', db='sys',charset='utf8')
cur = db.cursor()

url = 'https://www.tianyancha.com/login'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)
driver.find_element_by_xpath("//div[@tyc-event-ch='Login.PasswordLogin']").click()
driver.find_elements_by_xpath("//input[@placeholder='请输入11位手机号码']")[-2].send_keys('13515818605')
driver.find_element_by_xpath("//input[@placeholder='请输入登录密码']").send_keys('dingtian2014')
driver.find_element_by_xpath("//div[@tyc-event-ch='Login.PasswordLogin.Login']").click()
time.sleep(10)


# In[]
def per_co(original_company_name, company_name):
    time.sleep(3)
    url1 = 'http://www.tianyancha.com/search?key=%s&checkFrom=searchBox' % company_name
    driver.get(url1)
    time.sleep(1)
    content = driver.page_source.encode('utf-8')
    soup1 = BeautifulSoup(content, 'lxml')
    try:
        driver.find_element_by_class_name('captcha-title').text
        con = input("请进行验证，结束后请回车")
    except:
        pass
    try:
        url2 = soup1.find('div',class_='header').find('a', class_="name ").attrs['href']
    except:
        url2 = driver.find_element_by_xpath("//div[@class='content']/div[@class='header']/a[@class='name ']").get_attribute('href')
    driver.get(url2)
    returnCompany = driver.find_element_by_xpath('//*[@id="company_web_top"]/div[2]/div[3]/div[1]/h1').text
    originalCompanyName = original_company_name
    attachmentLink = url2
    time.sleep(2)
    ###确定子公司的数量
    try:
        columns = driver.find_element_by_xpath('//*[@id="nav-main-realHoldingCount"]/span[1]').text
    except:
        columns = ''
    if len(columns) > 0:
        try:
            for dataList in driver.find_elements_by_class_name('block-data'):
                if dataList.get_attribute('tyc-event-ch') == 'CompangyDetail.shijikongzhiquan':
                    endPage = dataList.find_element_by_class_name('pagination').find_element_by_class_name("-end").text
                    endPage = endPage.replace('.', '')
                    endPage = int(endPage)
        except:
            endPage = driver.find_element_by_xpath('//*[@id="nav-main-realHoldingCount"]/span[2]').text
            endPage = int(np.ceil(int(endPage)/20))
    
        i = 1
        try:
            while i <= endPage:
                #resultData = []
                pageData = driver.find_element_by_id('_container_companyholding').find_element_by_xpath('./table/tbody')
                companyDataa = pageData.find_elements_by_tag_name('tr')
                for companyData in companyDataa:
                    idNum = companyData.find_element_by_xpath('./td[1]').text
                    if idNum.isdigit():
                        companyName = companyData.find_element_by_xpath('./td[2]').find_elements_by_tag_name('a')[-1].text
                        subAttachLink = companyData.find_element_by_xpath('./td[2]').find_elements_by_tag_name('a')[-1].get_attribute('href')
                        investmentRate = companyData.find_element_by_xpath('./td[3]/span').text
                        stock = companyData.find_element_by_xpath('./td[4]/div').text.replace('\n', '-->')
                        #resultData.append([idNum, companyName, investmentRate, stock])
                        #sql_insert = "insert ignore into sub_central_spider_0529(id, sub_company, central_company, investment_rate, stock_chain, original_company_name, attach_link, return_company)values(" + '"' +idNum+ '","' + companyName + '","' + company_name + '","' + investmentRate + '","' + stock + '","' + originalCompanyName + '","' + attachmentLink + '","' + returnCompany + '");'
                        keys = "%s,%s,%s,%s,%s,%s,%s,%s,%s"%('id', 'sub_company', 'central_company', 'investment_rate', 'stock_chain', 'original_company_name', 'attach_link', 'return_company', 'sub_attachment_link')
                        values = "'%s','%s','%s','%s','%s','%s','%s','%s', '%s'"%(idNum, companyName, returnCompany, investmentRate, stock, originalCompanyName, attachmentLink, company_name, subAttachLink)
                        sql_insert = "insert ignore into sub_central_spider_0529(%s)values(%s)"%(keys, values)
                        cur.execute(sql_insert)
                        db.commit()
                print('已插入第%s页的数据'%i)
                if i != endPage:
                    for dataList in driver.find_elements_by_class_name('block-data'):
                        if dataList.get_attribute('tyc-event-ch') == 'CompangyDetail.shijikongzhiquan':
                            nextPage = dataList.find_element_by_class_name('pagination').find_element_by_class_name("-next")
                    driver.execute_script("arguments[0].click();", nextPage)
                time.sleep(5)
                i = i + 1
                #except Exception as e:
                    #print(e)
        except Exception as e:
            print(e)
        print('%s done'%company_name)
    else:
        print('%s has no data'%company_name)
        pass


# In[]
company_df = pd.read_excel('/Users/zhouxj/Desktop/工作/1700重客公司名单/重客基本信息爬虫结果-stage1.xlsx', sheet_name = '子公司爬虫列表')

# In[]
for line in tqdm(range(1342, len(company_df))):
    original_company_name = company_df.iloc[line, 0]
    company_name = company_df.iloc[line, 1]
    print(line,company_name)
    per_co(original_company_name, company_name)