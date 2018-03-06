# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
class KagglerankPipeline(object):
    def process_item(self, item, spider):
        return item
    def close_spider(self,spider):
        with open('compete_ranking.json','w')as f:
           json.dump(spider.com_rank_users,f)

