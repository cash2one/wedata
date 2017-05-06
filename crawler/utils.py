# -*- coding: utf-8 -*-
from html import unescape
from urllib.parse import urlparse, parse_qs

from config import session

def store(Model, data):
    if not len(data):
        return
    for item in data:
        session.execute(Model.__table__.insert().prefix_with('IGNORE'), item)
        # i = Model(**item)
        # session.add(i)
    session.commit()

def unescape_url(url):
    url = unescape(url)
    url = unescape(url)
    return url

def urlparam2dict(url):
    query = urlparse(url).query
    return dict([(k, v[0]) for k, v in parse_qs(query).items()])
