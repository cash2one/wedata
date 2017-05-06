# -*- coding: utf-8 -*-
import os
import sys
DIR = os.path.normpath(os.path.join(os.path.abspath(__file__), '../..'))
sys.path.insert(0, DIR)

from mitmproxy import controller, options, master
from mitmproxy.proxy import ProxyServer, ProxyConfig

from config import rd

class Mitm(master.Master):

    @controller.handler
    def response(self, f):
        if 'mp.weixin.qq.com/s' in f.request.url or 'mp.weixin.qq.com/mp/appmsg/show' in f.request.url:  # 正文页
            content_url = rd.rpop('content_url').decode('ascii')
            print('#', f.request.url)
            print('-', content_url)
            js_code = "<script>setTimeout(function(){window.location.href='%s';},2000);</script>" % content_url
            f.response.text = js_code + f.response.text

        if 'mp.weixin.qq.com/mp/getappmsgext' in f.request.url:  # 阅读数、点赞数
            rd.lpush('read&like', [f.request.url, f.response.text])

        if 'mp.weixin.qq.com/mp/appmsg_comment' in f.request.url:  # 评论
            rd.lpush('comment', [f.request.url, f.response.text])

    def run(self):
        try:
            master.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()

if __name__ == '__main__':
    opts = options.Options(cadir="~/.mitmproxy/")
    config = ProxyConfig(opts)
    server = ProxyServer(config)
    m = Mitm(opts, server)
    m.run()
