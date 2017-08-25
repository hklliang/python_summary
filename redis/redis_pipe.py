# -*- coding:utf-8 -*-  
__author__ = 'hklliang'
__date__ = '2017-08-25 17:05'

import redis
import time
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)

r = redis.Redis(connection_pool=pool)

# pipe = r.pipeline(transaction=False)
pipe = r.pipeline(transaction=True)

pipe.set('name', 'alex')
time.sleep(5)
pipe.set('role', 'sb')

pipe.execute()#一起提交