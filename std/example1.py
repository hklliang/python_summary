import sys
while True:
    line=sys.stdin.readline()
    # 会一直阻塞，直到屏幕有输入后再回车才会进行往下进行
    #空格回车tab也会读到
    # line = sys.stdin
    if 'q\n'==line:
        exit()
    if not line:
        break
    print(str([line]))
# sys.stdout.write('abc')#程序执行完才会输出，且后面不会带回车
# a=sys.stdin.read(1)#只会接收屏幕上输入，读取第一个字符
# print(a)

# print(sys.stdin)
# a=sys.stdin.read(1)
# print(sys.stdin)
# sys.stdout.write(str([a]))#['\n']