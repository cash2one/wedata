# -*- coding: utf-8 -*-
import re
import time
import json
from datetime import datetime

import requests
from config import HEADERS, session

from wedata.models import Article, Comment
from wedata.parser import handle_comment_json_data
from wedata.utils import urlparam2dict, store


def _get_key():
    return '27682868500c559dc3179bb696ba6240769e07689ec23274e307bb7bcce1dc34f7c092a6df135317ad4dd71e07a7b52cae214f6d6b7b0b5742359fe131645bd07b57d676f71908ecad5a2eb1b20e841c'

def get_cookies(url):

    url = url.split('#')[0]
    tmp = '&uin=MTc2OTM3NTU3Nw==&key={}'.format(_get_key())
    url = url + tmp

    r = requests.get(url)
    return r.cookies


def get_comment(url, comment_id):
    cookies = get_cookies(url)
    params = urlparam2dict(url)
    # cookies = {}
    # cookies['wap_sid2'] = 'CNmO2ssGEogBMF9lNWhickNDS3d1eTB0dDhQUUVWOEVNdG9uU3hFTnh1ejFOb3lhV1ZaRGVGUU9UNnJmUWhSQTdjeklIQmVWWkN3WTB3OUxIUFIxMC1kODhWdDVnc29jblphbktVY3FRRkdoSHdkTEtpSlhCRzN3WWtyQjdhUzl1QkFhVnFWcTdnd01BQUF+fjCFmZTHBQ=='
    # baseUrl = 'http://mp.weixin.qq.com/mp/getappmsgext?__biz=MzI0NTM4OTYwNQ==&appmsg_type=9&mid=2247483715&sn=4a412427def307615cdcfdfb90d0c63b&idx=1&scene=42&title=2017%E5%B9%B4%E9%A6%99%E6%B8%AF%E6%98%A5%E5%AD%A3%E4%BC%98%E6%83%A0%E5%BC%80%E8%B7%91&ct=1487295406&abtest_cookie=AQABAAgAAQCFhh4AAAA=&devicetype=android-23&version=/mmbizwap/en_US/htmledition/js/appmsg/index34ce60.js&f=json&r=0.7705947444040753&is_need_ad=1&comment_id=0&is_need_reward=0&both_ad=1&reward_uin_count=0&msg_daily_idx=1&uin=777&key=777&pass_ticket=h6Gq1l4%25252Bvd%25252B0tdOCxRAJlfUVRrBP%25252Fs9TTyExU%25252BrPH9WN%25252B%25252FTs2dceX0b3AnDVSPLx&wxtoken=2656406050&devicetype=android-23&clientversion=26050434&x5=1&f=json'
    baseUrl = 'http://mp.weixin.qq.com/mp/appmsg_comment'
    payload = {
        'action': 'getcomment',
        '__biz': params['__biz'],
        'appmsgid': 2652681240,
        'idx': params['idx'],
        'scene': 42,
        'comment_id': comment_id,
        'offset': 0,
        'limit': 100,
        'uin': 777,
        'key': 777,
        'wxtoken': 1727017869,
        'clientversion': 26050434,
        'devicetype': 'android-23',
        'x5': 1,
        'f': 'json'
    }

    r = requests.get(
        url=baseUrl,
        headers=HEADERS,
        params=payload,
        cookies=cookies,
        verify=True
    )
    print(r.text)
    return r.text




pattern = r'var comment_id = \"(.*?)\"'
while 1:
    article = session.query(Article).filter(Article.source_content!=None).filter(Article.comment_id==10).first()
    print(article.id ,article.account_id ,article.article_title)

    try:
        comment_id = re.search(pattern, article.source_content, re.DOTALL).groups()[0]
    except:
        article.comment_id = 9
        session.add(article)
        session.commit()
        continue

    if comment_id == '0':
        print('--')
        article.comment_id = 0
        session.add(article)
        session.commit()
        continue

    print(comment_id)
    json_data = get_comment(article.content_url, comment_id)
    print(json_data)
    try:
        comments = handle_comment_json_data(json_data, comment_id, article.content_url)
    except:
        article.comment_id = 9
        session.add(article)
        session.commit()
        continue

    store(Comment, comments)

    article.comment_id = comment_id
    session.add(article)
    session.commit()

    time.sleep(2)

