from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
def index(request):
    # return HttpResponse('<h1>hello world</h1>')

    return render(request, 'hello.html')


def login(request):
    # return HttpResponse('<h1>hello world</h1>')
    error_msg=''
    if request.method=="POST":
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        if username == 'root' and pwd == '123':
            return redirect('http://www.baidu.com')
        else:
            error_msg='用户名或密码错误'
    return render(request, 'login.html', {'error_msg': error_msg})