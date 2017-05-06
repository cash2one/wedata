# -*- coding:utf-8 -*-
from plan import Plan

from config import DIR

cron = Plan()
scripts = [
    {
        'name': 'liaoning.py',
        'every': '1.day'
    },
    {
        'name': 'hebei_shengchan.py',
        'every': '1.day'
    },
    {
        'name': 'hebei_jingying.py',
        'every': '1.day'
    }
]
for script in scripts:
    cron.script(script['name'], every=script['every'], path='{}/scripts'.format(DIR))

if __name__ == '__main__':
    cron.run('write')
