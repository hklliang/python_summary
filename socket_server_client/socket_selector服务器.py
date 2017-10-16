from socket import *
import selectors,time

sel=selectors.DefaultSelector()
def accept(server_fileobj,mask):
    print('server_fileobj',server_fileobj)
    print('mask',mask)
    conn,addr=server_fileobj.accept()
    print('accept')
    sel.register(conn,selectors.EVENT_READ,read)

def read(conn,mask):
    print('conn',conn)
    print('mask',mask)
    time.sleep(30)
    try:
        data=conn.recv(1024)
        if not data:
            print('closing',conn)
            sel.unregister(conn)
            conn.close()
            return
        conn.send(data.upper()+b'_SB')
    except Exception:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()



server_fileobj=socket(AF_INET,SOCK_STREAM)
server_fileobj.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
server_fileobj.bind(('127.0.0.1',8088))
server_fileobj.listen(5)
server_fileobj.setblocking(False) #设置socket的接口为非阻塞
sel.register(server_fileobj,selectors.EVENT_READ,accept) #相当于网select的读列表里append了一个文件句柄server_fileobj,并且绑定了一个回调函数accept

while True:
    events=sel.select() #检测所有的fileobj，是否有完成wait data的
    print('events',events)
    for sel_obj,mask in events:
        callback=sel_obj.data #callback=accpet
        callback(sel_obj.fileobj,mask) #accpet(server_fileobj,1)

"""
events 来连接的  s,执行accept  收到数据时c1，执行read

"""