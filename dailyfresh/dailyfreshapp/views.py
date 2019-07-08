from django.shortcuts import render,redirect
from dailyfreshapp.models import *
from hashlib import sha1
from django.http import HttpResponse,JsonResponse

# 首页
def index(request):
    return render(request, 'dailyfreshapp/index.html')

# 用户注册
def register(request):
    return render(request, 'dailyfreshapp/register.html')

# 接收用户注册的信息
def register_handle(request):
    # 接收用户输入的信息
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    # 判断两次输入的密码
    if upwd != upwd2:
        return redirect('/user/register')
    # 对密码进行加密
    s1 = sha1()
    s1.update(upwd.encode('utf8')) # 指定编码格式，不然会报错
    upwd3 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    # 对象保存到数据库中
    user.save()
    # 注册成功，跳转到登陆的页面
    return redirect('/user/login/')

# 判断用户名是否已经存在
def register_exist(request):
    # 前端js传入参数调用此方法，此时表单都没有提交，是GET方法
    user_name = request.GET['uname']
    count = UserInfo.objects.filter(uname=user_name).count()
    return JsonResponse({'count':count})

# 登陆界面
def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title':'用户登录', 'error_name':0, 'error_pwd':0, 'uname':uname}
    return render(request, 'dailyfreshapp/login.html', context)

# 接收登陆的信息
def login_handle(request):
    # 接收请求信息
    uname = request.POST['username']
    upwd = request.POST['pwd']
    jizhu = request.POST['jizhu']
