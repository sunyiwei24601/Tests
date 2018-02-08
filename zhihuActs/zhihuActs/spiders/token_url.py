# -*- coding: utf-8 -*-
import scrapy
import csv
import json

class TokenUrlSpider(scrapy.Spider):
    name = 'token_url'
    start_url = 'https://www.zhihu.com/api/v4/members/{id}'
    filename = r'C:\Users\孙轶伟\PycharmProjects\tests\zhihuActs\zhihuActs\user_id.csv'
    lists = []
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            lists.append(row[0])
    start_urls=[]
    for id in lists[1:]:
        start_urls.append(start_url.format(id=id))
    tokens=[]


    def parse(self, response):

        js=json.loads(response.text)
        if(js.get('url_token')):
            token_url=js['url_token']
            self.tokens.append(token_url)



