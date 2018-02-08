# -*- coding: utf-8 -*-
import scrapy
import json
from zhihuActs.items import actsItem
from scrapy import Request
import csv
import time

class ZhihuactSpider(scrapy.Spider):
    name = 'zhihuAct'
    filename=r'C:\Users\孙轶伟\PycharmProjects\tests\zhihuActs\zhihuActs\token_url.csv'
    lists=[]
    with open(filename,newline='',encoding='utf-8') as file:
        reader=csv.reader(file)
        for row in reader:
            lists.append(row[0])
    lists=lists[3:5]
    activities=[]
    start_urls=[]
    start_url= 'https://www.zhihu.com/api/v4/members/{user_id}/activities?limit=8&desktop=True'
    for id in lists:
        start_urls.append(start_url.format(user_id=id))
    #for user_id in lists:
    #    start_urls.append(start_url.format(user_id=user_id))

    def start_requests(self):
        for start_url in self.start_urls:
            yield Request(url=start_url,callback=self.parse_act,dont_filter=True)
            print("在这里第一页应该爬取结束了")
            print("在这里应该进入下一页了才对")
            yield Request(url=start_url,callback=self.parse_next,dont_filter=True)


    def parse_act(self, response):
        results=response.text
        js=json.loads(results)
        results=js['data']
        print('在这里应该爬取到了东西')
        n=0

        for result in results:
            print(n)
            n+=1
            #print(result['verb'])
            #print(result)
            if result.get('verb') in ('LIVE_PUBLISH',
                                      'MEMBER_CREATE_ARTICLE',
                                      'ANSWER_CREATE',
                                      'LIVE_JOIN',
                                      'MEMBER_COLLECT_ARTICLE',
                                      'MEMBER_VOTEUP_ARTICLE',
                                      'ANSWER_VOTE_UP',
                                      'MEMBER_COLLECT_ANSWER',
                                      'QUESTION_FOLLOW',
                                      'MEMBER_CREATE_PIN',
                                      'MEMBER_FOLLOW_ROUNDTABLE',
                                      'MEMBER_FOLLOW_COLUMN',
                                      'TOPIC_FOLLOW'
                                      ):
                item=actsItem()
            else:
                continue

            if result.get('actor').get('id'):
                item['user_id']=result['actor']['id']
            if result.get('created_time'):
                t=int(result['created_time'])
                item['time']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
            if result.get('actor').get('url_token'):
                item['url_token']=result['actor']['url_token']

            if result.get('verb'):
                type=result.get('verb')
                if(type in ('LIVE_PUBLISH','LIVE_JOIN')):
                    item['type']=type
                    item['title']=result['target']['subject']

                elif (type in  ('MEMBER_CREATE_ARTICLE',
                              'MEMBER_COLLECT_ARTICLE',
                              'MEMBER_VOTEUP_ARTICLE')):
                    item['type']=type
                    item['article_id']=result['target']['id']
                    item['title']=result['target']['title']
                    item['voteup_count']=result['target']['voteup_count']
                    #item['comments_author']=''

                elif (type in ('ANSWER_CREATE',
                             'ANSWER_VOTE_UP',
                             'MEMBER_COLLECT_ANSWER')):
                    item['type']=type
                    item['question_id']=result['target']['id']
                    item['title']=result['target']['question']['title']
                    item['voteup_count']=result['target']['voteup_count']
                    item['topics']=result['target']['question']['bound_topic_ids']
                    item['thanks_count']=result['target']['thanks_count']

                elif(type=='QUESTION_FOLLOW'):
                    item['type']=type
                    item['question_id']=result['target']['id']
                    item['title']=result['target']['title']
                    item['topics']=result['target']['bound_topic_ids']



                elif (type =='TOPIC_FOLLOW'):
                    item['type']=type
                    item['topics']=result['target']['id']
                    item['title']=result['target']['name']

                elif (type =='MEMBER_FOLLOW_ROUNDTABLE'):
                    item['type']=type
                    item['roundtable_id']=result['target']['id']
                    item['title']=result['target']['name']

                elif(type=='MEMBER_FOLLOW_COLUMN'):
                    item['type']=type
                    item['title']=result['target']['title']
                    item['column_id']=result['id']

                elif(type=='MEMBER_CREATE_PIN'):
                    item['type']=type
                    item['title']=result['target']['excerpt_title']
                    item['pin_id']=result['target']['id']
            yield item

    def parse_next(self,response):

        results = response.text
        js = json.loads(results)
        if js.get('paging').get('is_end')==False:
            if js.get('paging').get('next'):
                next_url=js['paging']['next']
        else:
            pass

        yield Request(url=next_url,callback=self.parse_act,dont_filter=True)
        print("在这里的地方进行了换页")
        time.sleep(2)
        yield Request(url=next_url,callback=self.parse_next,dont_filter=True)
        print("在这里换到了下下页")




