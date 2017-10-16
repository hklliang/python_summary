# -*- coding:utf-8 -*-
__author__ = 'hklliang'
__date__ = '2017-10-12 10:37'
import socket, struct, json, sys, os, math


class MYTCPClient:
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    allow_reuse_address = False
    max_packet_size = 1024
    coding = 'utf-8'
    request_queue_size = 5
    server_dir = 'files'

    def __init__(self, server_address):

        self.server_address = server_address
        self.client = socket.socket(self.address_family, self.socket_type)
        self.client.connect(server_address)

    def server_close(self):
        """Called to clean-up the server.
        """
        self.client.close()

    def run(self):

        while True:

            cmd = input('>>:').strip()
            if len(cmd) == 0: continue

            self.client.send(cmd.encode(self.coding))
            method, filename = cmd.split()
            if method == 'get':
                self.get(filename)
            elif method=='put':
                self.put(filename)

    def put(self, filename):
        file_size = os.stat(filename).st_size
        self.client.send(str(file_size).encode(self.coding))
        ack_received = int(self.client.recv(1024).decode())
        if file_size==ack_received:#表示文件已存在
            print('put:%s already exists'%filename)
            return
        with open(filename,'rb') as f:
            f.seek(ack_received)
            # if server_ack == b'1':
            self.client.sendall(f.read())
            self.get_progress()
        print('put:%s filesize:%s' % (file_size, filename))

    def get_progress(self):
        r=0
        while r<=100:
            r=int(self.client.recv(1024).decode())
            self.progress(r)

            if r == 100:
                break





    def get(self, filename):

        server_response = self.client.recv(1024)
        print('server_response', server_response)
        self.client.send(b'1')  # 表示准备好接收数据了
        file_total_size = int(server_response.decode(self.coding))
        received_size = 0
        with open(filename, 'wb') as f:
            while received_size < file_total_size:
                #避免接受多余数据
                if file_total_size-received_size<self.max_packet_size:
                    recv_size=file_total_size-received_size
                else:
                    recv_size=self.max_packet_size
                data = self.client.recv(recv_size)
                received_size += len(data)
                f.write(data)
                percent=int(received_size / file_total_size*100)

                self.client.send(str(percent).encode())
                self.progress(percent)
            else:
                print('get:%s filesize:%s' % (file_total_size, filename))





    def progress(self, percent, width=50):
        if percent > 100:
            percent = 100
        show_str = '[%%-%ds]' % (width) % (int(percent * width/100)* '#')
        print('%s%d%%' % (show_str, percent), file=sys.stdout, flush=True)


tcpclient = MYTCPClient(('127.0.0.1', 8080))

tcpclient.run()
