# -*- coding: utf-8 -*-
import scrapy
import json
from zhihuActs.items import actsItem
from scrapy import Request
import csv
import time
'''运行该命令，可暂停爬虫scrapy crawl somespider -s JOBDIR=crawls/somespider-1'''

class ZhihuactSpider(scrapy.Spider):
    '''记录时间'''
    time1=time.ctime()
    ctime1=time.time()

    '''提取目标token'''
    name = 'zhihuAct'
    filename=r'C:\Users\孙轶伟\PycharmProjects\tests\zhihuActs\zhihuActs\token_url.csv'
    lists=[]
    with open(filename,newline='',encoding='utf-8') as file:
        reader=csv.reader(file)
        for row in reader:
            lists.append(row[0])




    unfinished_items={}
    activities = []
    '''这里定义初始url，由之前未完成的url和新创建的url组合而成'''
    start_urls = []

    current_token = None
    process_id = []
    # 用来记录进入处理流程中的id
    finished_id = []
    # 用来记录已经完成的id





    unfinished_token=[]
    unfinished_urls=[]
    try:
        with open("unfinished_url.txt") as f:
            unfinished_items=json.load(f)
            for log_token in unfinished_items:
                if(unfinished_items[log_token]):
                    process_id.append(log_token)
                    unfinished_urls.append(unfinished_items[log_token])
    except:
        pass
    '''选中用户'''
    start_num=10
    end_num=100
    lists=lists[start_num:end_num]


    for url in unfinished_urls:
        start_urls.append(url)

    start_url= 'https://www.zhihu.com/api/v4/members/{user_id}/activities?limit=8&desktop=True'
    for id in lists:
        if id not in unfinished_items:
            process_id.append(id)
            start_urls.append(start_url.format(user_id=id))



    def start_requests(self):
        n=0
        for start_url in self.start_urls:
            #self.current_token=self.lists[n]
            yield Request(url=start_url,callback=self.parse_act,dont_filter=True)
            print("在这里第一页应该爬取结束了")
            print("在这里应该进入下一页了才对")
            yield Request(url=start_url,callback=self.parse_next,dont_filter=True)
            n+=1


    def parse_act(self, response):
        results=response.text
        url=response.url
        token=get_token_from_url(url)
        if token not in self.unfinished_items:
            self.unfinished_items[token]=url
        else:
            self.unfinished_items[token]=url




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
                    item['question_id']=result['target']['question']['id']
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
        print(get_token_from_url(response.url))
        js = json.loads(results)
        if js.get('paging').get('is_end')==False:
            if js.get('paging').get('next'):
                next_url=js['paging']['next']

            time.sleep(6)
            yield Request(url=next_url,callback=self.parse_act,dont_filter=True)
            print("在这里的地方进行了换页")

            yield Request(url=next_url,callback=self.parse_next,dont_filter=True)
            print("在这里换到了下下页")

        else:
            '''在这里识别删除未完成的url记录，并记录'''

            token = get_token_from_url(response.url)
            self.finished_id.append(token)

            self.unfinished_items[token]=None
            return None

def get_token_from_url(url):
    s=url.split("/")
    return s[6]






if __name__=="__main__":
    url='https://www.zhihu.com/api/v4/members/2333/activities?limit=8&desktop=True'
    print(get_token_from_url(url))








