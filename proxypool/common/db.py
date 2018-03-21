import re
import redis
from proxypool.common.error import PoolEmptyError
from proxypool.common.setting import *
from random import choice
from proxypool.log.save_log import *


class RedisClient(object):

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
    
    def add(self, proxy, score=INITIAL_SCORE):
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            add_drop_log('代理不符合规范-%s-丢弃'%proxy,LOG_INFO)
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)
    
    def random(self):
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError
    
    def decrease(self, proxy):
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            add_check_log('代理-%s-当前分数:%d-减1'%(proxy,score),LOG_INFO)
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            add_drop_log('代理-%s-当前分数:%d-移除' % ( proxy,score),LOG_INFO)
            return self.db.zrem(REDIS_KEY, proxy)
    
    def exists(self, proxy):
        return not self.db.zscore(REDIS_KEY, proxy) == None
    
    def max(self, proxy):
        add_check_log('代理%s可用，分数设置为:%d' %(proxy,MAX_SCORE),LOG_INFO)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)
    
    def count(self):
        return self.db.zcard(REDIS_KEY)
    
    def all(self):
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
    
    def batch(self, start, stop):
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)

if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(680, 688)
    print(result)
