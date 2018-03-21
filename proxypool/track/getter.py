import sys
from proxypool.common.db import RedisClient
from proxypool.spider.crawler import Crawler
from proxypool.common.setting import *
from proxypool.log.save_log import add_spider_log

class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()
    
    def is_over_threshold(self):
        # 判断是否达到了代理池限制
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
    
    def run(self):
        add_spider_log('获取器开始执行',LOG_INFO)
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                sys.stdout.flush()
                for proxy in proxies:
                    self.redis.add(proxy)
