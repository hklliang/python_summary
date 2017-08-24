# -*- coding:utf-8 -*-  
__author__ = 'hklliang'
__date__ = '2017-08-24 18:11'

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
#print(sys.argv) python 后面的脚本名 以空格分割的参数
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='direct_logs',
                      routing_key=severity, #以前是queue的名字
                      body=message)
print(" [x] Sent %r:%r" % (severity, message))

#E:\python\python_code\python_summary\rabbitMQ python direct_consumer.py warning from