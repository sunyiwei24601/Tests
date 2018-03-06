# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class KagglePipeline(object):
    def open_spider(self,spider):

        self.db = pymysql.connect('localhost', 'root', '192837', 'kaggle', charset="utf8")
        self.cursor = self.db.cursor()


    def process_item(self, item, spider):
        if('competition_url'in item.keys()):
            sql="insert into competitions VALUES("
            keys=[]
            for i in item:
                keys.append(i)
            for i in keys[:-1]:
                sql+="'"+str(item.get(i,"NUll")).replace("'",r"\'")+"',"
            sql = sql + str(item[keys[-1]]).replace("'",r"\'") + ')'

            self.cursor.execute(sql)
        else:
            sql = "insert into discussions VALUES("
            keys = []
            for i in item:
                keys.append(i)
            for i in keys[:-1]:
                sql += "'" + str(item.get(i, "NUll")).replace("'", r"\'") + "',"
            sql = sql + str(item[keys[-1]]).replace("'", r"\'") + ')'
            print(sql)
            self.cursor.execute(sql)


            self.db.commit()
        return item

    def close_spider(self,spider):
        self.db.close()