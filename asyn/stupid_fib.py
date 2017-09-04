import time
import random

"""
其中next(sfib)相当于sfib.send(None)，可以使得sfib运行至第一个yield处返回。
后续的sfib.send(random.uniform(0, 0.5))则将一个随机的秒数发送给sfib，
作为当前中断的yield表达式的返回值。这样，我们可以从“主”程序中控制协程计算斐波那契数列时的思考时间，
协程可以返回给“主”程序计算结果，Perfect！
"""
def stupid_fib(n):
	index = 0
	a = 0
	b = 1
	while index < n:
		sleep_cnt = yield b
		print('let me think {0} secs'.format(sleep_cnt))
		time.sleep(sleep_cnt)
		a, b = b, a + b
		index += 1
print('-'*10 + 'test yield send' + '-'*10)
N = 20
sfib = stupid_fib(N)
a=sfib.send(None)#都是为了启动sfib，然后保留现场
# fib_res = next(sfib)
print(a)
while True:
	print(fib_res)
	try:
		fib_res = sfib.send(random.uniform(0, 0.5))
	except StopIteration:
		break