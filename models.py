# -*- coding:utf-8 -*-
import os
import sys
DIR = os.path.normpath(os.path.join(os.path.abspath(__file__), '../../../'))
sys.path.insert(0, DIR)

from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, DateTime, SmallInteger, Text, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from config import engine

BaseModel = declarative_base()

class Official_account(BaseModel):
    __tablename__ = 'official_account'

    id = Column(Integer, primary_key=True)
    account_id = Column(String(30), unique=True)
    account_name = Column(String(30))
    qrcode = Column(String(200))
    profile = Column(Text)
    tag = Column(String(30))
    wechat_id = Column(String(30))
    followed_time = Column(DateTime)
    biz = Column(String(20))
    all_history = Column(Boolean)
    recently_updated = Column(DateTime)
    frommsgids = Column(Text)
    has_comment = Column(Boolean)

class Article(BaseModel):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    file_id = Column(String(30))
    account_id = Column(String(30))
    article_title = Column(String(200))
    author = Column(String(30))
    digest = Column(Text)
    source_url = Column(String(300))
    content_url = Column(String(300), unique=True)
    source_content = Column(Text)
    article_content = Column(Text)
    publication_time = Column(DateTime)
    obtain_time = Column(DateTime)
    article_read_num = Column(String(10))
    article_like_num = Column(String(10))
    article_reward_num = Column(String(10))
    rlr_update_time = Column(DateTime)
    is_headline = Column(Boolean)
    is_authorship = Column(Boolean)
    upload2en = Column(Boolean)
    copyright_stat = Column(String(10))
    cover = Column(String(300))
    comment_id = Column(String(15))

class Comment(BaseModel):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    id2 = Column(Integer)
    is_from_friend = Column(Boolean)
    is_from_me = Column(Boolean)
    is_top = Column(Boolean)
    page_url = Column(String(200))
    content_id = Column(String(30), unique=True)
    nick_name = Column(String(30))
    logo_url = Column(String(200))
    my_id = Column(Integer)
    content = Column(Text)
    create_time = Column(DateTime)
    like_id = Column(String(10))
    like_num = Column(String(5))
    like_status = Column(Boolean)

def init_db():
    BaseModel.metadata.create_all(engine)
def drop_db():
    BaseModel.metadata.drop_all(engine)
init_db()
