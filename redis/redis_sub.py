# -*- coding:utf-8 -*-  
__author__ = 'hklliang'
__date__ = '2017-08-25 17:11'

# !/usr/bin/env python
# -*- coding:utf-8 -*-

from redishelper import RedisHelper

obj = RedisHelper()
redis_sub = obj.subscribe()

while True:
    msg = redis_sub.parse_response()
    print(msg)
