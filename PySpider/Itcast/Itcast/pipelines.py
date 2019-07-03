# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class ItcastPipeline(object):
    # __init__方法是可选的，作为类的初始化方法
    def __init__(self):
        self.filename = open("itcastv3.json", "w")

    # process_item方法是必须写的，用来处理item数据
    def process_item(self, item, spider):
        jsontext = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.filename.write(jsontext)
        return item

    # close_spider方法是可选的，类的结束时调用的方法
    def close_spider(self, spider):
        self.filename.close()
