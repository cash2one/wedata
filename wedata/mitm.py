# -*- coding: utf-8 -*-
import os
import sys
DIR = os.path.normpath(os.path.join(os.path.abspath(__file__), '../..'))
sys.path.insert(0, DIR)
import time

from mitmproxy import controller, options, master
from mitmproxy.proxy import ProxyServer, ProxyConfig

from config import rd

class Mitm(master.Master):
    @controller.handler
    def response(self, f):
        if 'mp.weixin.qq.com/mp/profile_ext' in f.request.url:
            time.sleep(1)
            biz = rd.rpop('biz').decode('ascii')
            print(biz)
            rd.lpush('list_page', biz, f.response.text)
            js_code = "<script>setTimeout(function(){window.location.href='http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=%s#wechat_webview_type=1&wechat_redirect';},2000);</script>" % biz
            f.response.text = js_code + f.response.text

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
