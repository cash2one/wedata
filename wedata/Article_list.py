# -*- coding: utf-8 -*-
import re
import json
import time
from datetime import datetime

import requests

from config import DB_Session
from wedata.models import Official_account, Article
from wedata.utils import store
from wedata.parser import handle_list_page_json_data, handle_comment_json_data, handle_rlr_json_data

class Article_Info(object):

    def __init__(self):
        self.session = DB_Session()
        # self.baseUrl = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjM5MTI5MzIzMw==&f=json&frommsgid=1000000223&count=10&scene=124&is_ok=1&uin=MTc2OTM3NTU3Nw%3D%3D&key=440320bd14295a240d6bd1b97bad0d390cc4d4e483c5a01c1f5a9699d3ee6df7dd0c12c7cb2fa2e6e2f2d70af6534cd351933c85eaf7a88eed1b8459384b8ebe470da3792d3f27aca9fe4de525bee520&pass_ticket=M%2FDZak4Lo%2BbZQVYhgwyQsGImzfk5GTlAV5xaYb0qPlnac0oF99t96qm54xrGBoxk&wxtoken=&x5=1&f=json'
        self.baseUrl = 'https://mp.weixin.qq.com/mp/profile_ext'
        self.headers = {
            'Accept': 'image/png,*/*;q=0.5',
            'Accept-Language': 'zh-cn,zh;q=0.5',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Charset': 'gb2312,utf-8;q=0.7,*;q=0.7',
            'Keep-Alive': '300',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25)',
            'Host': 'mp.weixin.qq.com'
        }
        self.cookies = {
            'wxtokenkey': '7f71ef1f7318c2aa5f9e689f3b614d5bff30cd4c15e1937e246a69565c104d80',
            'wxticket': '2530867729',
            'wxticketkey': '29a7c65133d1c11469793fe453cadd10ff30cd4c15e1937e246a69565c104d80',
            'wap_sid': 'CNmO2ssGEkBJV015c2dGSG50NHBPa1ZqRURTZ2VHcWFFam9SWGdfRFcxRlZUdDUyOUlwQXdyekczdVNlOUkyWkdWQVFpU1hyGAQgpBQosfqg9Agwwd+JxwU=',
            'wap_sid2': 'CNmO2ssGEnB0RUxVS1RXTUt0OEJxZXNtWWdZVGktNEZTdmpRLTZROXA5QkJDV0Y1bHB0Mzl3cnVSVncyTC1FcDhlbDVpSXNnODVHVTFXUnY3WmlnWENocW5VZk5RWHY5QkhHcENJODJwTFNlYWd4V1Q0dUNBd0FBMLmqjMcF'
        }

    def _get_key(self):
        return 'c529fc820a281546e271590d0080c695b94787467867e7e25a4c3eef13bb9a104e58097af764150b6f821c5717c4dbae39a04b6108301e5e2652ff720ec72f2f73231120817f389fb78157457ed05699'

    def get_cookies(self, biz):
        baseurl = 'https://mp.weixin.qq.com/mp/profile_ext'
        payload = {
            'action': 'home',
            '__biz': biz,
            'uin': 'MTc3NzE1MDE1',
            'key': self._get_key(),
            'wxtoken': '',
            'x5': 1,
            'wx_header': 1

        }
        r = requests.get(
            url=baseurl,
            headers=self.headers,
            params=payload,
            verify=True
        )
        return r.cookies


    def get_list_msg_info(self, biz, frommsgid):
        '''
        获取列表页信息
        '''
        cookies = self.get_cookies(biz)
        payload = {
            'action': 'getmsg',
            '__biz': biz,
            'f': 'json',
            'frommsgid': frommsgid,
            'count': 10,
            'scene': 124,
            'is_ok': 1,
            'uin': 'MTc2OTM3NTU3Nw==',
            'key': self._get_key(),
            'wxtoken': '',
            'x5': 1,
        }
        if frommsgid == 0:
            payload.pop('frommsgid')

        r = requests.get(
            url=self.baseUrl,
            headers=self.headers,
            params=payload,
            cookies=cookies,
            verify=True
        )
        json_data = r.text
        print(r.url)
        print(json_data)
        return json_data


    def get_all_hsitory(self, account_id):
        '''
        获取一个公众号所有的文章信息
        '''
        account = self.session.query(Official_account).filter(Official_account.account_id==account_id).first()
        frommsgids_str = account.frommsgids
        if not frommsgids_str:
            frommsgids = []
        else:
            frommsgids = frommsgids_str.split(' ')

        print(account.biz)

        min_frommsgid = 0
        while 1:
            json_data = self.get_list_msg_info(account.biz, min_frommsgid)
            article_infos, frommsgids_tmp = handle_list_page_json_data(account.account_id ,json_data)
            store(Article, article_infos)
            frommsgids.extend(frommsgids_tmp)
            print(frommsgids)
            min_frommsgid = min(frommsgids)
            print(min_frommsgid)
            if len(article_infos) == 0:
                break

            time.sleep(1)

        frommsgids = list(set(frommsgids))  # 去重
        frommsgids_str = ' '.join(str(gid) for gid in frommsgids)
        account.frommsgids = frommsgids_str
        self.session.commit()


if __name__ == '__main__':

    account = Article_Info()
    # account.get_wap_sid2()
    account.get_all_hsitory('axzq98')

    # account.get_list_msg_info('Mjc0NzU0MzU0MA==', 0)
