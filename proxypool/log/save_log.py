from proxypool.web.app import sqldb
from proxypool.web.models import Check_log,Spider_log,Drop_log

#check_log存储
def add_check_log(log_info,level):
    log = Check_log(log_info=log_info,level=level)
    sqldb.session.add(log)
    sqldb.session.commit()

#spider_log存储
def add_spider_log(log_info,level):
    log = Spider_log(log_info=log_info,level=level)
    sqldb.session.add(log)
    sqldb.session.commit()

#drop_log存储
def add_drop_log(log_info,level):
    log =Drop_log(log_info=log_info,level=level)
    sqldb.session.add(log)
    sqldb.session.commit()