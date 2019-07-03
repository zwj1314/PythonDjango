import time
from selenium import webdriver


browser = webdriver.Firefox()
browser.set_page_load_timeout(30)


#有多少页商品
#browser.get('http://www.17huo.com/newsearch/?k=%E4%B8%9D%E8%A2%9C')
browser.get('http://www.17huo.com/?mod=search&keyword=%E4%B8%9D%E8%A2%9C')
#page_info = browser.find_element_by_xpath('/html/body/div[6]/div[2]/div[2]/div[2]/a[1]')
page_info = browser.find_element_by_xpath('/html/body/div[5]/div[5]/div')
#print(page_info.text)
pages = int(page_info.text.split(', ')[0].split(' ')[1])
print('商品总共有%d页' % pages)
for i in range(pages):
    url = 'http://www.17huo.com/?mod=search&keyword=%E4%B8%9D%E8%A2%9C' + '&page=' + str(i + 1)
    # url = 'http://www.17huo.com/?mod=search&keyword=%E4%B8%9D%E8%A2%9C&page=2'
    browser.get(url)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    #goods = browser.find_elements_by_class_name('item_title')
    #goods = browser.find_element_by_xpath('/html/body/div[5]/div[2]/div[4]/ul/li[*]/a[1]/p[2]')
    #for j in range(len(goods)):
    #print(goods.text)
    #goods = browser.find_element_by_tag_name('ul').find_elements_by_tag_name('li')
    #print(goods[i].text for i in range(len(goods)))
    goods = browser.find_element_by_css_selector('body > div.wrap > div:nth-child(2) > div.p_main > ul').find_elements_by_tag_name('li')
    print('第%d页有%d件商品' % ((i + 1), len(goods)))
    for good in goods:
        title = good.find_element_by_css_selector('a:nth-child(1) > p:nth-child(2)').text
        #pic = good.find_element_by_css_selector('a:nth-child(1) > p:nth-child(1) > img:nth-child(1)')
        price = good.find_element_by_css_selector('a:nth-child(1) > span:nth-child(1)').text
        print(title, price)


#browser.quit()