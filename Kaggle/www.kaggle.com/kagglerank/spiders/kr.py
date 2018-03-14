# -*- coding: utf-8 -*-
import scrapy
import requests
import json
from scrapy import Request
import time
from kagglerank.items import kernelItem
import csv
class KrSpider(scrapy.Spider):
    name = 'kr'
    url = 'https://www.kaggle.com/kernels.json?sortBy=hotness&group=everyone&pageSize=20&after={after}&competitionId={competition}'

    start_url='https://www.kaggle.com/kernels.json?sortBy=hotness&group=everyone&pageSize=20&competitionId={competition}'

    home_page_url='https://www.kaggle.com'
    start_urls=[]
    valid_num=0
    invalid_num=0
    def __init__(self):
        start=1
        end=1935
        competion_ids=self.get_competition_id(start,end)
        #competion_ids=['4458','4651']
        for cid in competion_ids:
            print (cid)
            self.start_urls.append(self.start_url.format(competition=cid))

    def parse(self,response):
        r=response.text
        j=json.loads(r)
        if(len(j)!=0):
            self.valid_num+=1
        else:
            self.invalid_num+=1



    def parse_next(self, response):
        time.sleep(0.2)
        r=response.text
        print (response.url)
        j=json.loads(r)
        competition = response.url[-4:]
        for i in j:
            yield self.get_kernels(i,competition)
        if(len(j)==20):
            after=j[-1]['id']

            r=Request(self.url.format(after=after,competition=competition),callback=self.parse)
            r.meta['competition']=competition
            yield r



    def get_kernels(self,j,competition_id):
        item=kernelItem()
        item["ID"]=j['id']
        item['username']=j['author']['userName']
        item['home_page_url']=self.home_page_url+j['author']['profileUrl']
        item['competition_id']=competition_id
        item['title']=j['title']
        item['kernels_url']=self.home_page_url+j['scriptUrl']
        item['enabled_time']=j['scriptVersionDateCreated']
        item['totalVotes']=j['totalVotes']
        item['medal']=j['medal']
        item['scrapy_time']=time.ctime()
        item['languageName']=j['languageName']
        item['lastRunTime']=j['lastRunTime']
        item['scriptVersionId']=j['scriptVersionId']
        return item


    def get_competition_id(self,start,end):
        competition_ids=[]
        with open("kaggle_competition_id.csv", newline='', encoding='utf-8') as f:
            c = csv.reader(f, delimiter=' ', quotechar='|')
            n = 0
            for row in c:
                if (n >= start and n <= end):
                    competition_ids.append(row[0])

                elif(n>end):
                    break
                n += 1
        return competition_ids