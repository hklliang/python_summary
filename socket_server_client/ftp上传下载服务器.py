# -*- coding:utf-8 -*-
__author__ = 'hklliang'
__date__ = '2017-10-12 10:37'
import socket, struct, json, sys, os, math,hashlib
import threading

class MYTCPServer:
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    allow_reuse_address = False
    max_packet_size = 1024
    coding = 'utf-8'
    request_queue_size = 5
    server_dir = 'files'

    def __init__(self, server_address, bind_and_activate=True):

        self.server_address = server_address
        self.socket = socket.socket(self.address_family, self.socket_type)

        if bind_and_activate:
            try:
                self.server_bind()
                self.server_activate()
            except:
                self.server_close()
                raise

    def server_bind(self):

        if self.allow_reuse_address:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()

    def server_activate(self):
        """Called by constructor to activate the server.
        """
        self.socket.listen(self.request_queue_size)

    def server_close(self):
        """Called to clean-up the server.
        """
        self.socket.close()

    def get_request(self):
        """Get the request and client address from the socket.
        """
        return self.socket.accept()

    def close_request(self, request):
        """Called to clean up an individual request."""
        request.close()

    def run(self):
        while True:
            self.conn, self.client_addr = self.get_request()

            print('from client', self.client_addr)
            while True:
                try :
                    data = self.conn.recv(1024)
                except ConnectionResetError:
                    break
                if not data: break

                args = data.decode(self.coding).split()

                if args[0]=='get':
                    self.get(args[1])

                if args[0]=='put':
                    self.put(args[1])


    def get_file_path(self,filename):
        file_path = os.path.normpath(os.path.join(self.server_dir, filename))
        return file_path



    def get(self,filename):
        file_path=self.get_file_path(filename)
        with open(file_path,'rb') as f:
            # m=hashlib.md5()#可以用来判断文件是否有更新
            file_size=os.stat(file_path).st_size
            self.conn.send(str(file_size).encode(self.coding))
            client_ack=self.conn.recv(1024)
            if client_ack==b'1':
                t =threading.Thread(target=self.get_progress, )
                t.start()

                self.conn.sendall(f.read())
                # self.get_progress()
                # for line in f:
                #     # m.update(line)#可以用来判断文件是否有更新
                #     self.conn.send(line)
                # # print('file md5',m.hexdigest())
        print('get:%s filesize:%s' % (file_size, filename))

    def get_progress(self):
        r = 0
        while r <= 100:
            r = int(self.conn.recv(1024).decode())

            self.progress(r)

            if r==100:
                break



    def put(self, filename):

        filename=os.path.basename(filename)
        file_path=self.get_file_path(filename)

        client_response=self.conn.recv(1024)
        file_total_size = int(client_response.decode(self.coding))

        #1如果文件名存在且大小相同则返回
        #2服务器文件大于上传文件，则重新上传
        #3服务器文件小于上传文件，则断点续传
        if os.path.exists(file_path) and os.path.getsize(file_path)<=file_total_size:
            serve_file_size = os.path.getsize(file_path)

            if serve_file_size==file_total_size:
                self.conn.send(('%s'%serve_file_size).encode())
                print('put:%s already exists'%file_path)
                return

            received_size = serve_file_size
            mode='ab'

        else:
            received_size=0
            mode='wb'
        print('----->', file_path)

        self.conn.send(('%s' % received_size).encode())
        with open(file_path, mode=mode) as f:

            # f.seek(received_size)
            while received_size < file_total_size:
                if file_total_size - received_size < self.max_packet_size:
                    recv_size = file_total_size - received_size
                else:
                    recv_size = self.max_packet_size
                recv_data = self.conn.recv(recv_size)
                f.write(recv_data)

                received_size += len(recv_data)
                percent=int(received_size / file_total_size*100)
                self.progress(percent)
                self.conn.send(str(percent).encode())
            else:
                print('put:%s filesize:%s' % (file_total_size, file_path))

    def progress(self, percent, width=50):
        if percent > 100:
            percent = 100
        show_str = '[%%-%ds]' % (width) % (int(percent*width/100)* '#')
        print('%s%d%%' % (show_str, percent), file=sys.stdout, flush=True)


tcpserver1 = MYTCPServer(('127.0.0.1', 8080))

tcpserver1.run()
