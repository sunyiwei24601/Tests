# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import json
import re
from scrapy import  Request
import time
from Kaggle.items import competitionItem
class KaggleSpider(scrapy.Spider):
    name = 'kaggle'

    start_urls = ['titericz']

    competition_url='https://www.kaggle.com/{id}/competitions.json?' \
                    'sortBy=grouped&group=entered' \
                    '&pageSize=20&page=1'
    refer=r'https://www.kaggle.com'
    kernel_url='https://www.kaggle.com/kernels.json?' \
               'sortBy=votes&group=everyone&pageSize=30' \
               '&userId={id}&page={page}'
    discussion_url='https://www.kaggle.com/{username}' \
                   '/discussion_messages.json?sortBy=mostVotes&group=commentsAndTopics' \
                   '&pageSize=50&page={page}'


    def start_requests(self):
        for id in self.start_urls:
            request =scrapy.Request(url=self.competition_url.format(id=id),
                                 callback=self.parse,
                                 dont_filter=True)
            request.meta['username']=id
            yield  request

    def parse(self, response):
        t=response.text
        print(response.url)
        j=json.loads(t)
        username=response.meta['username']
        for item in self.get_compete_item(j,response.meta['username']):
            yield item


        #比赛内容的递归翻页
        if(not self.check_competition_end(j)):
            compete_url=re.findall('.*page=',response.url)[0]
            request=Request(compete_url+'2',callback=self.parse_compete)
            request.meta['username']=response.meta['username']
            yield request

        #discussion 内容
        r1=Request(self.discussion_url.format(username=username,page=1),callback=self.parse_discuss)
        r1.meta['username']=username
        yield r1


        #获取id内容
        id_url=j['pagedCompetitionGroup']['competitions'][0]['userTeamUsers'][0]['thumbnailUrl']
        id=re.findall(r'.*\/([0-9]{4,6})-',id_url)
        r2=Request(self.kernel_url.format(id=id,page=1),callback=self.parse_kernel)
        r2.meta['id']=id
        yield r2
        #获取kernel内容

    def check_competition_end(self,js):
        if  js['fullCompetitionGroups'] or len (js['pagedCompetitionGroup']['competitions'])>0:
            return False
        else:
            return True

    def get_compete_item(self,js,username):
        full=js['fullCompetitionGroups']
        print('老哥这里抓取到了东西吧')
        paged=js['pagedCompetitionGroup'].get('competitions','')
        if full:
            for compete in full[0]['competitions']:
                item = competitionItem()
                item['ID']=compete['competitionId']
                item['username']=username
                item['home_page_url']='www.kaggle.com/'+username

                item['competition_name'] =compete['competitionTitle']
                item['competition_url'] = self.refer+compete['competitionUrl']
                item['enabled_time'] = compete['enabledDate']
                item['dealine']=compete['deadline']
                item['rank']=str(compete['userRank'])+'/'+str(compete['totalTeams'])
                item['medal_type']=compete['medal']
                item['remark']=compete['competitionDescription']
                item['scrapy_time']=time.ctime()
                print(item)
                yield item


        if paged:
            for compete in paged:
                item = competitionItem()
                item['ID']=compete['competitionId']
                item['username']=username
                item['home_page_url']='www.kaggle.com/'+username

                item['competition_name'] =compete['competitionTitle']
                item['competition_url'] = self.refer+compete['competitionUrl']
                item['enabled_time'] = compete['enabledDate']
                item['dealine']=compete['deadline']
                item['rank']=str(compete['userRank'])+'/'+str(compete['totalTeams'])
                item['medal_type']=compete['medal']
                item['remark']=compete['competitionDescription']
                item['scrapy_time']=time.ctime()
                print(item)
                yield item

    def parse_compete(self,response):
        t=response.text
        js=json.loads(t)
        pagenum=int(response.url.split('page=')[1])
        compete_url = re.findall('.*page=', response.url)[0]

        print(response.url)
        if not self.check_competition_end(js):
            for item in self.get_compete_item(js,response.meta['username']):
                yield item
        request=Request(compete_url+str(pagenum+1),callback=self.parse_compete)
        request.meta['username']=response.meta['username']
        yield request

    def parse_discuss(self,response):
        t=response.text
        j=json.loads(t)
        pagenum=int(response.url.split('page=')[1])

        username=response.meta['username']
        if j['discussions']:
            for item in self.get_discuss_item(j):
                yield item



        #进入下一页
        r=Request(self.discussion_url.format(username=username,page=pagenum+1),callback=self.parse_discuss)
        r.meta['username']=username
        yield r

    def get_discuss_item(self,js):
        pass

    def parse_kernel(self,response):
        t=response.text
        id=response.meta['id']
        j=json.loads(t)
        pagenum=int(response.url.split('page=')[1])

        if len(j)>0:
            for kernel in j:
                yield self.get_kernel_item(kernel)

        r=Request(self.kernel_url.format(id=id,page=pagenum+1))
        r.meta['id']=id
        return r

    def get_kernel_item(self,js):
        pass



