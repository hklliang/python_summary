# _*_coding:utf-8_*_
__author__ = 'Alex Li'
import pika
import time
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

# You may ask why we declare the queue again ‒ we have already declared it in our previous code.
# We could avoid that if we were sure that the queue already exists. For example if send.py program
# was run before. But we're not yet sure which program to run first. In such cases it's a good
# practice to repeat declaring the queue in both programs.
channel.queue_declare(queue='hello')
#队列，如果生产者没有队列，消费者可以生成队列
# channel.queue_declare(queue='hello',durable=True)#队列持久化，durable=True需要在生产者和消费者都加上

def callback(ch, method, properties, body):
    print("--->",ch,method,properties)
    time.sleep(10)
    print(" [x] Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)#需要确认消息已经收到，否则一起动又会自动收消息

channel.basic_qos(prefetch_count=1)#只能处理一条消息，没有处理完，不会给他发消息
channel.basic_consume(callback,
                      queue='hello',)
                      # no_ack=True)#确认消息，一般为False，需要确认消息

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()