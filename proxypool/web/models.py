from proxypool.web.app import sqldb
from _datetime import datetime



class Check_log(sqldb.Model):
    __tablename__ = 'check_logs'
    id = sqldb.Column(sqldb.Integer, primary_key=True)
    datetime = sqldb.Column(sqldb.DateTime, default=datetime.now)
    log_info = sqldb.Column(sqldb.String(64))
    level = sqldb.Column(sqldb.String(64))

class Spider_log(sqldb.Model):
    __tablename__ = 'spider_logs'
    id = sqldb.Column(sqldb.Integer, primary_key=True)
    datetime = sqldb.Column(sqldb.DateTime, default=datetime.now)
    log_info = sqldb.Column(sqldb.String(64))
    level = sqldb.Column(sqldb.String(64))

class Drop_log(sqldb.Model):
    __tablename__ = 'drop_logs'
    id = sqldb.Column(sqldb.Integer, primary_key=True)
    datetime = sqldb.Column(sqldb.DateTime, default=datetime.now)
    log_info = sqldb.Column(sqldb.String(64))
    level = sqldb.Column(sqldb.String(64))
