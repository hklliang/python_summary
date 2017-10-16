import time

"""
有yield的函数，调用后不会马上执行
可以通过next或者send(None)来执行到yield，会阻塞
再通过send来再重新唤醒yield,yield的左边会接收到send的值，
send会接收到yield右边的值
"""
def consumer():#5
    '''任务1:接收数据,处理数据'''
    k=0
    while True:#6
        print('begin')#7
        x=yield k#8

        k+=1
        print('end')#11
        print('x=',x)#12

def producer():#2
    '''任务2:生产数据'''
    g=consumer()#3
    next(g)#4
    for i in range(10):#9
        t=g.send(i)#10

        print('t=',t)#13


start=time.time()
#基于yield保存状态,实现两个任务直接来回切换,即并发的效果
#PS:如果每个任务中都加上打印,那么明显地看到两个任务的打印是你一次我一次,即并发执行的.
producer()#1

stop=time.time()
print(stop-start) #2.0272178649902344