# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import json

class DdbookPipeline(object):
    def process_item(self, item, spider):
        print(item)
        # item为虚假的字典格式，需要将其转化为字典再存储
        content = []
        for i in item:
            dict = {}
            dict[i] = item[i]
            content.append(dict)
        self.collection.insert_many(content)

    def open_spider(self, spider):
        self.client = MongoClient()
        self.collection = self.client['DD']['book']

    def close_spider(self,spider):
        # 关闭mongodb数据库
        self.client.close()