

def fib(n):
	index = 0
	a = 0
	b = 1
	while index < n:
		yield b
		a, b = b, a + b
		index += 1

def copy_fib(n):
	print('I am copy from fib')
	yield from fib(n)#可以认为将生成器的功能转移到另一个函数
	print('Copy end')
print('-'*10 + 'test yield from' + '-'*10)
# a=next(copy_fib(20))
# print(a)
# b=next(copy_fib(20))
# print(b)
# c=next(copy_fib(20))
# print(c)
a=copy_fib(20)
b=a.send(None)
print(b)
c=next(a)
next(a)
next(a)
next(a)
next(a)
next(a)
next(a)
next(a)
next(a)
b=next(a)
print(b)

# for fib_res in copy_fib(20):
# 	print(fib_res)