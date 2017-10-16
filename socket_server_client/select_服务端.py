from socket import *
import select,time

s=socket(AF_INET,SOCK_STREAM)
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(('127.0.0.1',8081))
s.listen(5)
s.setblocking(False) #设置socket的接口为非阻塞
read_l=[s,]
while True:
    r_l,w_l,x_l=select.select(read_l,[],[])#没有client时会block
    #当客户端发了个信息过来，r_l=conn，且只有conn，没有s
    print('r_l', r_l)
    print('w_l', w_l)
    print('x_l', x_l)
    print('1read_l', read_l)
    for ready_obj in r_l:
        if ready_obj == s:
            conn,addr=ready_obj.accept() #此时的ready_obj等于s
            read_l.append(conn)#将conn放入real_l，此时有s和conn
            print('2read_l',read_l)
        else:
            try:
                print('ready_obj',ready_obj)
                data=ready_obj.recv(1024) #此时的ready_obj等于conn
                if not data:
                    ready_obj.close()
                    read_l.remove(ready_obj)
                    continue
                time.sleep(30)
                ready_obj.send(data.upper())

            except ConnectionResetError:
                ready_obj.close()
                read_l.remove(ready_obj)

"""
收到连接时  r_l [s,],read_l[s,] append后 read_l[s,c1]
收到信息时 r_l [c1,] read_l[s,c1]
在收到连接2 r_l [s,],read_l[s,c1] append后 read_l[s,c1,c2] 
断开后  r_1 [c1] read_l [s,c1,c2]
r_l相当于有反应的对象
real_l相当于包括server的连接池

需要处理完c1的消息，才能响应c2的连接
"""