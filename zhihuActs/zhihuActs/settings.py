# -*- coding: utf-8 -*-

# Scrapy settings for zhihuActs project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhihuActs'

SPIDER_MODULES = ['zhihuActs.spiders']
NEWSPIDER_MODULE = 'zhihuActs.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhihuActs (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False
authoration=['oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
             'Bearer 2|1:0|10:1513832293|4:z_c0|92:Mi4xUFJOakF3QUFBQUFBa0lLVHVlN2REQ1lBQUFCZ0FsVk5aWTBvV3dBTW4yUk1XX0l2YjNhNlNSUmhmRy1GaDZsWWVR|d45ed089d0c3ca18eff8a3f5bee812db4804d2a13a92b69f124d47b5a82d0292',
             'Bearer 2|1:0|10:1518512590|4:z_c0|92:Mi4xa0pzZ0FBQUFBQUFBd0d6dWU2c2pEU1lBQUFCZ0FsVk56dmR2V3dCdVdlcy1MSHQ1MkFyM1dXSlpLaF9MaXcyalJ3|5c98ec54dd91baa05f5d265ba19e034bcb28f36959ff93b47bb3a598bdbccb18']
# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Host": "www.zhihu.com",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'Accept':' application/json, text/plain, */*',
    'Accept-Language':' zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    #'Accept-Encoding': 'gzip, deflate, br',

    'x-api-version': '3.0.40',
    #'authorization': 'Bearer 2|1:0|10:1518512590|4:z_c0|92:Mi4xa0pzZ0FBQUFBQUFBd0d6dWU2c2pEU1lBQUFCZ0FsVk56dmR2V3dCdVdlcy1MSHQ1MkFyM1dXSlpLaF9MaXcyalJ3|5c98ec54dd91baa05f5d265ba19e034bcb28f36959ff93b47bb3a598bdbccb18',
    'authorization':authoration[0],
    'x-udid': 'AFAs9vEGJQ2PTsPE0PGKRyCNYtPjokHiT9w=',
    'origin': 'https://www.zhihu.com',
    #'Cookie': 'q_c1=e84afa18f842439ca6ea21290194baad|1516079712000|1516079712000; capsion_ticket="2|1:0|10:1518526594|14:capsion_ticket|44:MzZmYTA5ZDhjODNhNDkxMWE2ZjY1ZjE2M2U4ZmVhOTg=|13385ee6293961418dbe0c83ca428134430914125f0507a0ca2dee459f432ad1"; _zap=dd4d01dc-f921-46ec-a2d0-ad9df7450d9b; infinity_uid="2|1:0|10:1518444407|12:infinity_uid|24:OTQ0MjM1MDY5MzQzMzI2MjA4|ad21e515a371893417557951f2486ff6e90425b55a60b4517b6ac15199481526"; r_cap_id="NjE1NTE1NzEyZTc3NDhkM2I4MDM2MjFjZWM5MTZkMWU=|1517975681|a0563d3befb7734c445b550f001580c2cbab4761"; cap_id="ZThlYTQ5ZDZhZWY3NDQ4ODg4YjRhYzhlZThiMmY2MzM=|1517975681|b524868055889c9c2da89cbbd0d5b24ff75f0ae5"; l_cap_id="ODY4NzY4NGU1NTk2NDVmYTk0MmU3ZTU2NmZiNmYwZjU=|1517975681|5adebf91419832e004ee009defc177d5f29bf3d2"; z_c0="2|1:0|10:1518526596|4:z_c0|92:Mi4xa0pzZ0FBQUFBQUFBa092TFdZUWlEU1lBQUFCZ0FsVk5oQzV3V3dEa0gwLUpmNkFrRVhwSUUzNWxqQmpDdC1qd3JB|ddeaa883cf6ea466bc51c157d45bae606bd6edebf583964204fd9e5e0d9e60c3"; aliyungf_tc=AQAAAOuoxlRwlQ0Ac9xTcuV+4Rg902jE; _xsrf=fba40c48-af92-49b9-8b02-6b9f7f204d45; d_c0="AJDry1mEIg2PTsBoseanVvvBtenQbIZZapQ=|1518434695"',
    'Connection':' keep-alive'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zhihuActs.middlewares.ZhihuactsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #'zhihuActs.middlewares.ProxyMiddleware': 543,
    'zhihuActs.middlewares.Proxy_Bought_Middleware': 542,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
 #See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'zhihuActs.pipelines.save_token_pipline': 999,
    #'zhihuActs.pipelines.save_activities_pipline': 300,
     'zhihuActs.pipelines.save_activities_mysql_pipeline':400,
}
LOG_LEVEL='INFO'
DOWNLOAD_TIMEOUT=5
DOWNLOAD_DELAY=0
RANDOM_DOWNLOAD_DELAY= True
CONCURRENT_REQUESTS=32





# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 1.0
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
