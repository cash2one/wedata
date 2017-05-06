from functools import wraps
from flask import request, g
from math import ceil
MAX_PAGESIZE = 100
MIN_PAGE = 1
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 25


class Paginator(object):
    def __init__(self, page, page_size):
        self.page = max(int(page), MIN_PAGE)
        self.page_size = min(int(page_size), MAX_PAGESIZE)
        self.count = 0

    def __repr__(self):
        return '<Paginator page:{self.page!r} page_size:{self.page_size!r} offset:{self.offset!r} \
limit:{self.limit!r}>'.format(self=self)

    @property
    def offset(self):
        return self.page_size * (self.page - 1)

    @property
    def limit(self):
        return self.page_size

    @property
    def total_pages(self):
        return ceil(self.count / self.page_size)


def pagination(f):
    """
    to add g.paginator
    if g.paginator does not exist, return all.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        page = request.args.get("page", 1)
        page_size = request.args.get("page_size", 25)
        if page_size == '-1':
            pass
        else:
            g.paginator = Paginator(page, page_size)
        return f(*args, **kwargs)
    return wrapper

def paginate_data(data):
    if not hasattr(g, 'paginator'):
        return {"results": data}
    return {
        "page": g.paginator.page,
        "page_size": g.paginator.page_size,
        "total_pages": g.paginator.total_pages,
        "total_count": g.paginator.count,
        "results": data
    }
