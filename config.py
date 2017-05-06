# -*- coding:utf-8 -*-
import os, sys
DIR = os.path.normpath(os.path.join(os.path.abspath(__file__), '..'))
sys.path.insert(0, DIR)
import logging

import redis
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# from common.data.models import Official_account


HEADERS = {
    'Host': 'mp.weixin.qq.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; M5 Note Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043202 Safari/537.36 MicroMessenger/6.5.4.1000 NetType/WIFI Language/en',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN, en-US;q=0.8',
}

HOST = '192.168.1.100'

CAPS = {
    'platformName': 'Android',
    'platformVersion': '6.0',
    'deviceName': '192.168.1.116:5555'
}

# redis config
rd = redis.StrictRedis(host='localhost', port=6379, db=1)

# database
MYSQL_CONFIG = {
    'root': '123456',
    'host': '192.168.1.101',
    'db': 'wechat3',
    'charset': 'utf8',
    'echo': 'False',
    'pool_size': 100,
    'pool_recycle': 3600
}
DB_CONNECT_STRING = 'mysql+pymysql://root:qwe```@127.0.0.1/wedata2?charset=utf8mb4'
engine = create_engine(DB_CONNECT_STRING, echo=False, pool_size=100, pool_recycle=3600)

# engine = create_engine(**MYSQL_CONFIG)
metadata = MetaData(engine)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

# log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
    datefmt='%d %b %Y %H:%M:%S',
    filename='/var/log/wechat.log',
    filemode='a+')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)-4s: %(levelname)-4s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# device
wechat_id = 'gcdyweixin'
udid = '192.168.1.102:5555'

INTERVAL_TIME = 30
