# -*- coding: utf-8 -*-
import scrapy
import json
from max.items import MaxItem
from scrapy import Request
class VpgameSpider(scrapy.Spider):
    name = 'vpgame'
    start_urls=[]
    url='http://www.vpgame.com/gateway/v1/match/?page={page}&category=dota&status=closed&lang=zh_CN'
    for i in range(1,470):
        start_urls.append(url.format(page=i))
    schedule_url='http://www.vpgame.com/gateway/v1/match/schedule?tid={tid}&lang=zh_CN&_=1519490981939'


    def parse(self, response):
        j=json.loads(response.text)
        tid=[]
        for i in j['body']:
            tid.append((i['tournament_schedule_id'],i['round']))

        for i,j in tid:
            r=Request(self.schedule_url.format(tid=i),callback=self.detail_parse)
            r.meta['round']=j
            yield  r

    def detail_parse(self,response):
        keys = ['id', 'name', 'mode', 'modename', 'status',
                'left_odd', 'right_odd', 'date', 'competitioncol', 'left_team',
                'left_id', 'right_id',
                'right_team', 'victory', 'whowins', 'leaft_team_score', 'right_team_score']
        t=response.text
        j=json.loads(t)

        for com in j['body']:
            item = MaxItem()
            item['id']=com['id']
            item['name']=com['name']
            item['mode']=com['mode']
            item['modename']=com['mode_name']
            item['status']=com['status']
            item['left_odd']=com['left_odd']
            item['right_odd']=com['right_odd']
            item['date']=com['date']
            item['right_team']=com['right_team']
            item['left_team']=com['left_team']
            item['left_id']=com['odd']['left']['id']
            item['right_id']=com['odd']['right']['id']
            item['victory']=com['victory']
            if com['odd']['left']['victory']=='wins':
                item['whowins']='left'
            if com['odd']['right']['victory']=='wins':
                item['whowins']='right'
            item['left_team_score']=com['left_team_score']
            item['right_team_score']=com['left_team_score']
            item['competitioncol']=response.meta['round']

            yield item









