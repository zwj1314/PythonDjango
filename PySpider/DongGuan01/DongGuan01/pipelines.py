# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from scrapy.conf import settings
import pymongo
import pymysql
import time

class Dongguan01Pipeline(object):
    def __init__(self):
        # 创建一个文件
        self.filename = codecs.open("donggguan.json", "w", encoding = "utf-8")

    def process_item(self, item, spider):
        # 中文默认使用ascii码来存储，禁用后默认为Unicode字符串
        content = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.filename.write(content)
        return item

    def close_spider(self, spider):
        self.filename.close()


class Dongguan02Pipeline(object):

    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        sheetname = settings["MONGODB_SHEETNAME"]

        client = pymongo.MongoClient(host= host, port= port)
        mydb = client[dbname]
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item


class Jb51MysqlPipeline(object):
    def __init__(self):
        host = settings["MYSQL_HOST"]
        port = settings["MYSQL_PORT"]
        user = settings["MYSQL_USER"]
        passwd = settings["MYSQL_PASSWD"]
        db = settings["MYSQL_DB"]
        # 数据库链接
        self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset="utf8mb4")
        # 通过CURSOR执行增删改查
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(
            "insert into jb51(title, url, content, tags, time) values (%s, %s, %s, %s, %s)",
            (
                item['title'],
                item['url'],
                item['content'],
                item['tags'],
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
        )
        # 提交sql语句
        self.conn.commit()
        return item




class Jb51MongodbPipeline(object):

    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        sheetname = settings["MONGODB_SHEETNAME"]

        client = pymongo.MongoClient(host= host, port= port)
        mydb = client[dbname]
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
