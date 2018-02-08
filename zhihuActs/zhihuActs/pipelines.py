# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from zhihuActs.items import actsItem
class ZhihuactsPipeline(object):
    def process_item(self, item, spider):
        return item

class save_token_pipline(object):
    def close_spider(self,spider):
        fieldnames = ['first_name', 'last_name']

        with open('token_url.csv', 'w', newline='', encoding='utf-8') as file:
            w = csv.writer(file)
            print(spider.tokens)
            for token in spider.tokens:
                w.writerow([str(token)])


class save_activities_pipline(object):
    def process_item(self,item,spider):
        act =dict(item)
        spider.activities.append(act)
        return item

    def close_spider(self,spider):
        fieldnames = actsItem.fields.keys()
        with open('activities.csv', 'w', newline='', encoding='utf-8') as file:
            w = csv.DictWriter(file, fieldnames=fieldnames)
            w.writeheader()
            for act in spider.activities:
                w.writerow(act)
