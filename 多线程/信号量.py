from threading import Thread,Semaphore
import threading
import time
# def func():
#     if sm.acquire():
#         print (threading.currentThread().getName() + ' get semaphore')
#         time.sleep(2)
#         sm.release()
def func():
    sm.acquire()
    print('%s get sm' %threading.current_thread().getName())
    time.sleep(3)
    sm.release()
if __name__ == '__main__':
    sm=Semaphore(5)
    for i in range(23):
        t=Thread(target=func)
        t.start()