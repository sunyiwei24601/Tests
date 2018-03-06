# -*- coding: utf-8 -*-
import scrapy
import requests
import json
from scrapy import Request
class KrSpider(scrapy.Spider):
    name = 'kr'
    url = 'https://www.kaggle.com/kernels.json?sortBy=hotness&group=everyone&pageSize=20&after={after}&competitionId={competition}'
    after=569157
    competition=8089
    start_url='https://www.kaggle.com/kernels.json?sortBy=hotness&group=everyone&pageSize=20&competitionId={competition}'
    r = requests.get(url.format(after=after,competition=competition)).text
    j = json.loads(r)

    start_urls=[]

    def parse(self, response):
        r=response.text
        j=json.loads(r)
        for i in j:
            yield self.get_kernels(i)
        if(len(j)==20):
            after=j[-1]['id']
            competition=response.meta['competition']
            r=Request(self.url.format(after=after,competition=competition),callback=self.parse)
            r.meta['competition']=competition
            yield r



    def get_kernels(self,j):
        pass
