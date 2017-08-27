# -*- coding:utf-8 -*-  
__author__ = 'hklliang'
__date__ = '2017-08-22 17:05'

import socket

HOST='localhost'
PORT=8001

s=socket.socket()
s.connect((HOST,PORT))

while True:
    msg=input(">>:").encode('utf-8')

    s.sendall(msg)
    data=s.recv(1024)

    print('Received',repr(data))

s.close()