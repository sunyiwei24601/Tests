# -*- coding: utf-8 -*-

# Scrapy settings for kagglerank project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'kagglerank'
LOG_LEVEL='INFO'
SPIDER_MODULES = ['kagglerank.spiders']
NEWSPIDER_MODULE = 'kagglerank.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'kagglerank (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY =False

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

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Cookie':'intercom-id-koj6gxx6=5296acaa-8a07-4d4d-a08a-2dd76f447e6f; __stripe_mid=99a2f1bf-f79d-4045-812e-044b3d287779; __RequestVerificationToken=iiumo2s5zpCSIZwVfvZaE0lKoyAUyJFr4YCEk9qfsnaoLKE58Cp6R1GdSUH6KIXw1bjgyZmtzc98nGQXPQ5mDZlNB4s1; ARRAffinity=b1bb1165b64053f3b2487920451d9f426ed0f0ef7cf8b948912fb5400e1daca9; ai_user=UqPj7|2018-03-06T16:05:11.861Z; _ga=GA1.2.499892106.1520352316; _gid=GA1.2.1508100693.1520352316; ai_session=YbslF|1520352335190.52|1520352335190.52; TempData=_VMTwedzhVUrGrbdAGQ3IhCuOTS8ITf1KqqqRNO5DnHKDM59w15TM4N47HLtfwdAbXYDQswhZMEh9DBnwtmRlrAoSvtoK17OeWY7l/bVht79feebgufYerpNV1C715Nv9sgbNeqVyP7hVhXwhOrS014SRES8mDICLgodyYL+z2lu3yaSsqulpNqp2ee9bAUbmhksvmKE+r7c8Dmb4PkJNZKnnMso='





}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'kagglerank.middlewares.KagglerankSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'kagglerank.middlewares.KagglerankSpiderMiddleware': 543,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
  # 'kagglerank.pipelines.KagglerankPipeline': 300,
    'kagglerank.pipelines.kernels_mysql_save':400
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
