from django.shortcuts import render,redirect
from booktest.models import *
from django.http import HttpResponse,HttpResponseRedirect
#from django.template import RequestContext,loader

def index(request):
    # temp = loader.get_template('booktest/index.html') # get_tenplate是去获取templates路径下（同级路径）的文件
    # return HttpResponse(temp.render()) #render方法是去解析html
    bookList = BookInfo.objects.all()
    context = {'list':bookList}
    return render(request, 'booktest/index.html', context)


def show(request, book_id):
    book = BookInfo.objects.get(pk=book_id)
    herolist = book.heroinfo_set.all()
    context = {'list':herolist}
    return render(request, 'booktest/show.html', context)

def postTest1(request):
    return render(request, 'booktest/postTest1.html')

#构造函数，由urls中的路由配置调用函数
def postTest2(request):
    # 获取postTest1页面提交过来的表单数据
    uname = request.POST['uname']
    upwd = request.POST['upwd']
    ugender = request.POST.get('ugender')
    uhobby = request.POST.getlist('uhobby')
    # 构造上下文
    context = {'uname':uname, 'upwd':upwd, 'ugender':ugender, 'uhobby':uhobby}
    return render(request, 'booktest/postTest2.html', context)


# Cookie练习
def cookieTest(request):
    response = HttpResponse()
    cookie = request.COOKIES
    if 't1' in cookie:
        response.write(cookie['t1'])
    #response.set_cookie('t1','abc')
    return response

# 重定向练习
def redirectTest1(request):
     #return HttpResponseRedirect('/booktest/redirectTest2')
    return redirect('/booktest/redirectTest2')

def redirectTest2(request):
    return HttpResponse('这是重定向来的页面')

# 通过用户登陆练习Session
def session1(request):
    uname = request.session.get('myname', '未登陆')
    context = {'uname':uname}
    return render(request, 'booktest/session1.html', context)

def session2(request):
    return render(request, 'booktest/session2.html')

def session2_handle(request):
    # 获取前端页面传入的用户名
    uname = request.POST['uname']
    # session（字典）中设置存储用户名
    request.session['myname'] = uname
    # 设置session的有效时间 0表示关闭浏览器的时候过期
    #request.session.set_expiry(0)
    # 登陆成功后，重定向到登陆的页面
    return redirect('/booktest/session1/')

def session3(request):
    # 删除session
    del request.session['myname']
    return redirect('/booktest/session1/')


def show1(request, id, id2):
    context = {"id":id}
    return render(request, 'booktest/show.html', context)