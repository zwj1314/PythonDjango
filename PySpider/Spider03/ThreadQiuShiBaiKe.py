import threading
from queue import Queue
from lxml import etree
import requests
import json

# 重写采集线程
class ThreadCrawl(threading.Thread):
    def __init__(self, threadName, pageQueue, dataQueue):
        # 调用父类初始化方法
        super(ThreadCrawl, self).__init__()
        #super().__init__(ThreadCrawl)
        self.threadName = threadName
        self.pageQueue = pageQueue
        self.dataQueue = dataQueue
        self.headers =  {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"}

    def run(self):
        print("启动" + self.threadName)
        while not CRAWL_EXIT:
            # 取出一个数字，先进先出
            # 可选参数为block，默认值为True
            # 1.如果队列为空，block为True的话，不会结束，会进入阻塞状态，直到队列有新的数据
            # 2.如果队列为空，block为False的话，就会弹出一个Queue.empty()异常
            try:
                page = self.pageQueue.get(False)
                url = "https://www.qiushibaike.com/text/page/" + str(page) + "/"
                #print(url)
                content = requests.get(url, headers = self.headers).text
                #print(content)
                self.dataQueue.put(content)

            except:
                pass
        print("结束" + self.threadName)

# 重写解析线程
class ThreadParse(threading.Thread):
    def __init__(self, threadName, dataQueue, filename, lock):
        super(ThreadParse, self).__init__()
        self.threadName = threadName
        self.dataQueue = dataQueue
        self.filename = filename
        self.lock = lock

    def run(self):
        print("启动" + self.threadName)
        while not PARSE_EXIT:
            try:
                html = self.dataQueue.get(False)
                self.parse(html)
            except:
                pass
        print("结束" + self.threadName)

    def parse(self, html):
        html = etree.HTML(html)
        node_list = html.xpath('//div[contains(@id, "qiushi_tag")]')
        for node in node_list:
            # 用户名
            username = node.xpath('./div/a[2]/h2/text()')[0].strip()
            # 段子内容
            content = node.xpath('./a/div/span/text()')
            # 点赞
            image = node.xpath('./div/a[1]/img/@src')
            # 评论
            item = {
                "username" : username,
                "content" : content,
                "image" : image
            }
            # with 后面有两个必须执行的操作：__enter__ 和 _exit__
            # 不管里面的操作结果如何，都会执行打开、关闭
            # 打开锁、处理内容、释放锁
            with self.lock:
                # 写入存储的解析后的数据
                self.filename.write(json.dumps(item, ensure_ascii=False))


CRAWL_EXIT = False
PARSE_EXIT = False

def main():

    # 页码的队列，表示10个页面
    pageQueue = Queue(20)
    # 放入1-10的数字，先进先出
    for i in range(2, 22):
        pageQueue.put(i)


    # 采集结果(每页的html源码）的数据队列，参数为空表示不限制
    dataQueue = Queue()

    filename = open("duanzi.json", "a+")

    # 创建锁
    lock = threading.Lock()

    # 采集线程的名称
    crawlList = ["采集线程1号", "采集线程2号", "采集线程3号"]

    # 存储三个采集线程
    threadcrawl = []
    for threadName in crawlList:
        thread = ThreadCrawl(threadName, pageQueue, dataQueue)
        thread.start()
        threadcrawl.append(thread)



    parseList = ["解析线程1号", "解析线程2号", "解析线程3号"]
    threadparse = []
    for threadName in parseList:
        thread = ThreadParse(threadName, dataQueue, filename, lock)
        thread.start()
        threadparse.append(thread)



    while not pageQueue.empty():
        pass

    # 如果采集线程为空，采集线程退出循环
    global CRAWL_EXIT
    CRAWL_EXIT = True

    print("pageQueue为空 ")
    for thread in threadcrawl:
        thread.join() # 非守护进程
        print("1")


    while not dataQueue.empty():
        pass

    # 如果解析线程为空，解析线程退出循环
    global PARSE_EXIT
    PARSE_EXIT = True

    print("pageQueue为空 ")
    for thread in threadparse:
        thread.join() # 非守护进程
        print("2")

    with lock:
        # 关闭文件
        filename.close()
    print("谢谢使用")


if __name__ == '__main__':
    main()