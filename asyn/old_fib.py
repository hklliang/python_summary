def old_fib(n):
	res = [0] * n
	index = 0
	a = 0
	b = 1
	while index < n:
		res[index] = b
		a, b = b, a + b
		index += 1
	return res
a=old_fib(20)
print(a)
print('-'*10 + 'test old fib' + '-'*10)
for fib_res in old_fib(20):
	print(fib_res)
