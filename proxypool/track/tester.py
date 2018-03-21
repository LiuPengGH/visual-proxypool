import asyncio
import aiohttp
import time
import sys
try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from proxypool.common.db import RedisClient
from proxypool.common.setting import *
from proxypool.log.save_log import add_check_log




class Tester(object):
    def __init__(self):
        self.redis = RedisClient()
 
    async def test_single_proxy(self, proxy):
        # 测试单个代理
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                add_check_log( '正在测试%s'%proxy,LOG_INFO)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15, allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        add_check_log('代理可用%s'%proxy,LOG_INFO)
                    else:
                        self.redis.decrease(proxy)
                        add_check_log('请求状态码不合法%d IP:%s'%( response.status,proxy),LOG_ERROR)
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                add_check_log('代理请求失败%s'%proxy,LOG_ERROR)
    
    def run(self):
        # 测试主函数
        add_check_log('测试器开始运行',LOG_INFO)

        try:
            count = self.redis.count()
            add_check_log('当前剩余%d个代理'%count,LOG_INFO)

            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                add_check_log('正在测试第%d-%d个代理'%(start + 1,stop),LOG_INFO)
                test_proxies = self.redis.batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            add_check_log('测试器发生错误%s'%e.args,LOG_ERROR)


