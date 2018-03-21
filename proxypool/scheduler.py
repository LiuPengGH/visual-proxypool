import time
from multiprocessing import Process
from proxypool.api import app
from proxypool.track.getter import Getter
from proxypool.track.tester import Tester
from proxypool.common.setting import *
from proxypool.log.save_log import *

class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        # 定时测试代理
        tester = Tester()
        while True:
            add_check_log('测试器开始运行',LOG_INFO)
            tester.run()
            time.sleep(cycle)
    
    def schedule_getter(self, cycle=GETTER_CYCLE):
        # 定时获取代理
        getter = Getter()
        while True:
            add_spider_log('开始抓取代理',LOG_INFO)
            getter.run()
            time.sleep(cycle)
    
    def schedule_api(self):
        # 开启API
        app.run(API_HOST, API_PORT)
    
    def run(self):
        # print('代理池开始运行')

        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
