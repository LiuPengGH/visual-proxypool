import requests
from requests.exceptions import ConnectionError
from proxypool.log.save_log import add_spider_log
from proxypool.common.setting import *

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def get_page(url, options={}):
    headers = dict(base_headers, **options)
    add_spider_log('正在抓取%s'%str(url),LOG_INFO)
    try:
        response = requests.get(url, headers=headers)
        add_spider_log('抓取%s成功,状态码：%d'%(url, response.status_code),LOG_INFO)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        add_spider_log('抓取失败%s'%url,LOG_ERROR)
        return None
