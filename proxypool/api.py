from flask import g, render_template
from proxypool.common.db import RedisClient
from proxypool.web.models import Check_log,Spider_log,Drop_log

from proxypool.web.app import app, sqldb




#获取redis内所有的proxy
def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis

# web界面首页路由
@app.route('/')
def index():
    return render_template('main.html')

#展示所有Proxy
@app.route('/all/')
def get_all():
    conn = get_conn()
    proxy_list = conn.all()
    proxy_count = str(conn.count())
    with open('proxy.txt','w',encoding = 'utf-8') as fp:
        for proxy in proxy_list:
            fp.write('"%s",'%proxy)

    return render_template('proxy_show.html',proxy_list=proxy_list,proxy_count=proxy_count)

#随机抽取一个Proxy
@app.route('/random/')
def get_proxy():
    conn = get_conn()
    return conn.random()

# 获取Proxypool总量
@app.route('/count/')
def get_counts():
    conn = get_conn()
    return str(conn.count())


@app.route('/create_table/')
def create_table():
    sqldb.drop_all()
    sqldb.create_all()
    return "table created"



#查询所有Check_log
@app.route('/select_all_check_log/')
def select_all_check_log():
    logs = Check_log.query.all()
    title = 'Check_log'
    return render_template('show_log.html',logs=logs,title=title)

#查询所有Spider_log
@app.route('/select_all_spider_log/')
def select_all_spider_log():
    logs = Spider_log.query.all()
    title = 'Spider_log'
    return render_template('show_log.html',logs=logs,title=title)

#查询所有Drop_log
@app.route('/select_all_drop_log/')
def select_all_drop_log():
    logs = Drop_log.query.all()
    title = 'Drop_log'
    return render_template('show_log.html',logs=logs,title=title)

if __name__ == '__main__':
    app.run()
