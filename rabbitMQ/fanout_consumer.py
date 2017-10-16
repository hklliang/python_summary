# -*- coding:utf-8 -*-  
__author__ = 'hklliang'
__date__ = '2017-08-24 13:59'
"""
广播模式
"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         type='fanout')
"""

channel.basic_qos(prefetch_count=1)#只能处理一条消息，没有处理完，不会给他发消息
channel.basic_consume(callback,
                      queue='hello',)
"""


result = channel.queue_declare(exclusive=True)  # 不指定queue名字,rabbit会随机分配一个名字,exclusive=True会在使用此queue的消费者断开后,自动将queue删除
queue_name = result.method.queue#消费者只能通过队列获得消息

channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()