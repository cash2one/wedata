# -*- coding: utf-8 -*-
import requests

from config import HEADERS

class Official_account_API:
    def __init__(self):
        pass

    def _get_key(self):
        return '8ac5c0aba99f72d6aaab488202bc649ef7463f688bfa5ae06c2ff8a9491e09c090a6e8e4b158ef2365459c9aade95f1a6b1f32686a5e50c3116bd7952c8002adc93c1441c0f7ef52286d9a755f8af58d'

    def _get_cookies(self):
        url = 'http://mp.weixin.qq.com/s?__biz=MjM5MTI5MzIzMw==&mid=2654428984&idx=3&sn=fc9a9cd5ddb784c75b7fd1e25ee51fb8&chksm=bd7435668a03bc707fdbd1bfe156f33ad53b95372f09cb50527db3bb63ad3b11c62519eb800f&scene=27#wechat_redirect'
        url = url.split('#')[0]
        tmp = '&uin=MTc2OTM3NTU3Nw==&key={}'.format(self._get_key())
        url = url + tmp
        r = requests.get(url)
        print(r.cookies['wap_sid2'])
        return r.cookies

    def get_profile(self, biz):
        '''
        获取公众号简介
        '''
        baseUrl = 'https://mp.weixin.qq.com/mp/profile_ext'
        payload = {
            'action': 'home',
            '__biz': biz,
            'scene': 124,
        }

        HEADERS['x-wechat-uin'] = 'MTc2OTM3NTU3Nw=='
        HEADERS['x-wechat-key'] = self._get_key()
        cookies = self._get_cookies()
        r = requests.get(url=baseUrl, headers=HEADERS, params=payload, cookies=cookies, verify=True)
        print(HEADERS)

    def get_qrcode(self, account_id):
        '''
        获取公众号二维码
        '''
        qrcode = 'http://open.weixin.qq.com/qr/code/?username={}'.format(account_id)

    def get_rlr(self, url):
        '''
        获取文章阅读数、点赞数、赞赏数
        '''
        baseUrl = 'http://mp.weixin.qq.com/mp/getappmsgext'
        payload = {
            '__biz': params['__biz'],
            'is_only_read': 1,
            'is_temp_url': 0,
            'appmsg_type': 9,
            'mid': params['mid'] if 'mid' in params else params['appmsgid'],
            'idx': params['idx'] if 'idx' in params else params['itemidx'],
            'scene': params['scene'],
            'sn': params['sn'] if 'sn' in params else params['sign'],
            'devicetype': 'android-23',
            'is_need_ad': 1,
            'is_need_reward': 0,
            'x5': 1,
            'f': 'json'
        }
        r = requests.post(
            url=baseUrl,
            headers=HEADERS,
            data=payload,
            cookies=cookies,
            verify=True
        )

    def get_comment(delf, url, comment_id):
        '''
        获取文章评论
        '''
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

class Account_API:
    def __init__(self):
        pass

    @classmethod
    def update(self):
        '''
        获取公众号最近更新的10个图文消息
        '''
        pass

    @classmethod
    def get_all_history(self):
        pass



if __name__ == '__main__':
    oa = Official_account_API()
    oa.get_profile('MzAwNTMxNTc3NQ==')
