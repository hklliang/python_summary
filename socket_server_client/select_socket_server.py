# -*- coding:utf-8 -*-  
__author__ = 'hklliang'
__date__ = '2017-08-22 17:29'
#_*_coding:utf-8_*_


#_*_coding:utf-8_*_


import select
import socket
import sys
import queue


server=socket.socket()
server.setblocking(0)

server.bind(('localhost',8001))
server.listen(5)
inputs=[server,]
outputs=[]
message_queues={}
"""
来一个连接就会readble就多一个，
"""
while True:
    print('waiting for next event')
    print(inputs)
    readable,writeable,exeptional=select.select(inputs,outputs,inputs)#如果没有任何fd就绪,那程序就会一直阻塞在这里
    print('readable',readable)
    for r in readable:
        if r is server:
            conn,addr=r.accept()
            print('new connection from ',conn)
            r.setblocking(0)
            inputs.append(conn)
            #为了不阻塞整个程序, 我们不会立刻在这里开始接收客户端发来的数据, 把它放到inputs里, 下一次loop时, 这个新连接
            # 就会被交给select去监听,如果这个连接的客户端发来了数据 ,那这个连接的fd在server端就会变成就续的,select就会把这个连接返回,返回到
            # readable 列表里,然后你就可以loop readable列表,取出这个连接,开始接收数据了, 下面就是这么干 的
            message_queues[conn]=queue.Queue()
        else:#s不是server的话,那就只能是一个 与客户端建立的连接的fd了
            data=r.recv(1024)
            if data:
                print('receive from [%s]'%r.getpeername()[0],data)
                message_queues[r].put(data)
                if r not in outputs:
                    outputs.append(r)
            else:
                print('client is closed')

                if r in outputs:
                    outputs.remove(r)

                inputs.remove(r)

                del message_queues[r]

    for w in writeable:
        try:
            next_msg=message_queues[w].get_nowait()
        except queue.Empty:
            print("client [%s]" % w.getpeername()[0], "queue is empty..")
            outputs.remove(w)

        else:
            print("sending msg to [%s]" % w.getpeername()[0], next_msg)
            w.send(next_msg.upper())

    for s in exeptional:
        print("handling exception for ", s.getpeername())
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        del message_queues[s]
