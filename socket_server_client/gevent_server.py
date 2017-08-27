# -*- coding:utf-8 -*-  
__author__ = 'hklliang'
__date__ = '2017-08-22 16:56'

import sys
import socket
import time
import gevent

from gevent import socket,monkey
monkey.patch_all()

"""
通过gevent实现单线程下的多socket并发
"""
def server(port):
    s=socket.socket()
    s.bind(('0.0.0.0',port))

    s.listen(500)
    while True:
        conn,add=s.accept()
        gevent.spawn(handle_request,conn)#


def handle_request(conn):
    try:
        while True:
            data=conn.recv(1024)
            print('recv',data)
            conn.send(data)
            if not data:
                conn.shutdown(socket.SHUT_WR)

    except ConnectionResetError as e:
        print(e)

    finally:
        conn.close()

if __name__ == '__main__':
    server(8001)
