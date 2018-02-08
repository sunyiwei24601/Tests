# -*- coding: utf-8 -*-

# Define your item pipelines here
from scrapy.exporters import JsonItemExporter
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import  DropItem
class DuplicatePipeline(object):
    def __init__(self):
        ids_seen=set()
'''
    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("duplicate item found:%s"%item)
        else:
            self.ids_seen.add(item['id'])
            return item
'''
class JsonSavePipeline(object):
    f = open("items.json", 'wb')
    def __init__(self):
         f=open("items.json",'wb')

    def process_item(self,item,spider):
        line=json.dumps(dict(item))+"\n"
        self.f.write(line.encode('utf-8'))
        return item
