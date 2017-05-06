# -*- coding: utf-8 -*-
import re
import json
import time
from datetime import datetime

from wedata.utils import unescape_url


def strip_html(self, html):
    pattern = re.compile(r"var msgList \= \'(.*?)\'\;")
    data = pattern.search(html, re.S).groups()[0]
    return data

def handle_list_page_json_data(account_id, data):
    '''
     处理列表页的json
    '''
    data = json.loads(data)
    article_infos = []  # 文章信息
    frommsgids = set()  # 公众号的图文消息ID

    general_msg_list = data['general_msg_list']
    if not general_msg_list:
        return 0
    general_msg_list = json.loads(general_msg_list)

    for i in general_msg_list['list']:
        frommsgid = i['comm_msg_info']['id']
        frommsgids.add(frommsgid)
        # print(json.dumps(i, sort_keys=True, indent=4, ensure_ascii=False))
        if 'app_msg_ext_info' in i:
            common_msg_info = i['comm_msg_info']
            publication_time = common_msg_info['datetime']
            publication_time = time.localtime(publication_time)
            publication_time = time.strftime('%Y-%m-%d %H:%M:%S', publication_time)

            app_msg_ext_info = i['app_msg_ext_info']
            multi_app_msg_item_list = app_msg_ext_info['multi_app_msg_item_list']

            article_info = {
                'account_id': account_id,
                'file_id': app_msg_ext_info['fileid'],
                'article_title': app_msg_ext_info['title'],
                'author': app_msg_ext_info['author'],
                'copyright_stat': app_msg_ext_info['copyright_stat'] if 'copyright_stat' in app_msg_ext_info else '',
                'digest': app_msg_ext_info['digest'],
                'cover': app_msg_ext_info['cover'],
                'source_url': unescape_url(app_msg_ext_info['source_url']),
                'content_url': unescape_url(app_msg_ext_info['content_url']),
                'publication_time': publication_time,
                'obtain_time': datetime.now(),
                'is_headline': 1
            }
            article_infos.append(article_info)

            for j in multi_app_msg_item_list:
                article_info = {
                    'account_id': account_id,
                    'file_id': j['fileid'],
                    'article_title': j['title'],
                    'author': j['author'],
                    'digest': j['digest'],
                    'copyright_stat': j['copyright_stat'],
                    'cover': j['cover'],
                    'source_url': unescape_url(j['source_url']),
                    'content_url': unescape_url(j['content_url']),
                    'publication_time': publication_time,
                    'obtain_time': datetime.now(),
                    'is_headline': 0
                }
                article_infos.append(article_info)
    for x in article_infos:
        print(x)
    return article_infos, frommsgids


def handle_rlr_json_data(json_data):
    '''
    处理阅读和点赞的json
    '''
    data = json.loads(json_data)

    like_num = data['appmsgstat']['like_num']
    read_num = data['appmsgstat']['read_num']
    # comment_enabled = data['comment_enabled'] if 'comment_enabled' in data else 0

    return like_num, read_num


def handle_comment_json_data(json_data, comment_id, url):
    '''
    处理评论的json
    '''
    data = json.loads(json_data)
    comments = []

    for i in data['elected_comment']:
        comment = {}
        comment['page_url'] = url
        comment['comment_id'] = comment_id
        comment['id2'] = i['id']
        comment['content_id'] = i['content_id']
        comment['content'] = i['content']
        comment['is_from_friend'] = i['is_from_friend']
        comment['is_from_me'] = i['is_from_me']
        comment['is_top'] = i['is_top']
        comment['like_id'] = i['like_id']
        comment['like_num'] = i['like_num']
        comment['like_status'] = i['like_status']
        comment['nick_name'] = i['nick_name']
        comment['logo_url'] = i['logo_url']
        comment['my_id'] = i['my_id']

        create_time = i['create_time']
        create_time = time.localtime(create_time)
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', create_time)

        comment['create_time'] = create_time

        comments.append(comment)

    return comments
