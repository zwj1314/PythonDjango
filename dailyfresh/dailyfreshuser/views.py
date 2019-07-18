from django.shortcuts import render, redirect, reverse
from dailyfreshuser.models import *
from hashlib import sha1
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from . import user_decorator
from dailyfreshorder.models import *
from django.core.paginator import Paginator

# 首页
def index(request):
    return render(request, 'dailyfreshuser/index.html')

# 用户注册
def register(request):
    return render(request, 'dailyfreshuser/register.html')

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
    return redirect('/user/login')

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
    return render(request, 'dailyfreshuser/login.html', context)

# 接收登陆的信息
def login_handle(request):
    # 接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    # 若记住密码没有被选中，则不会被提交，值为0
    jizhu = post.get('jizhu', 0)
    # 根据用户名来查询对象
    user = UserInfo.objects.filter(uname=uname) # filter若无结果，则为[],get则会报异常
    print(uname)
    #
    if len(user) == 1:
        s1 = sha1()
        s1.update(upwd.encode('utf8'))
        # 查出返回的是一个列表，返回一个或者多个
        if s1.hexdigest() == user[0].upwd:
            redict = HttpResponseRedirect('/user/info')
            # 记住用户名
            if jizhu != 0:
                redict.set_cookie('uname', uname)
            else:
                redict.set_cookie('uname', '', max_age=-1)
            # 记录session，跳转到用户界面时，可以直接拿到用户的信息
            request.session['user_id'] = user[0].id
            request.session['user_name'] = uname
            return redict
        else:
            context = {'title': '用户登陆', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'dailyfreshuser/login.html', context)
    else:
        context = {'title': '用户登陆', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'dailyfreshuser/login.html', context)

# 用户详情页，显示用户的邮箱以及姓名
@user_decorator.login
def info(request):
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()
    browser_goods = GoodsBrowser.objects.filter(user=user).order_by("-browser_time")
    goods_list = []
    if browser_goods:
        goods_list = [browser_good.good for browser_good in browser_goods]  # 从浏览商品记录中取出浏览商品
        explain = '最近浏览'
    else:
        explain = '无最近浏览'

    context = {
        'title': '用户中心',
        'page_name': 1,
        'user_phone': user.uphone,
        'user_address': user.uaddress,
        'user_name': username,
        'goods_list': goods_list,
        'explain': explain,
        'user_email':user.uemail,
    }
    return render(request, 'dailyfreshuser/user_center_info.html', context)

# 订单模块，显示用户的订单
@user_decorator.login
def order(request, index):
    user_id = request.session['user_id']
    orders_list = OrderInfo.objects.filter(user_id=int(user_id)).order_by('-odate')
    paginator = Paginator(orders_list, 2)
    page = paginator.page(int(index))
    context = {
        'paginator': paginator,
        'page': page,
        # 'orders_list':orders_list,
        'title': "用户中心",
        'page_name': 1,
    }
    return render(request, 'dailyfreshuser/user_center_order.html', context)


# 收货地址,根据记录的session查询
@user_decorator.login
def site(request):
    # 如果是用户登陆过来的，则直接查询用户的信息返回
    user = UserInfo.objects.get(id=request.session['user_id'])
    # 如果是用户修改收货地址POST过来的请求，则将更新后的收货地址返回
    if request.method == 'POST':
        user.ureceiveaddr = request.POST['ushou']
        user.uaddress = request.POST['uaddress']
        user.upostcode = request.POST['uyoubian']
        user.uphone = request.POST['uphone']
        user.save()
    context = {'title':'用户中心', 'user':user}
    return render(request, 'dailyfreshuser/user_center_site.html', context)

def logout(request):
    # 用户退出，清空所有的session
    request.session.flush()
    return redirect(reverse("dailyfreshuser:login")) # 注意：这里是双引号 302重定向到登陆界面
    #return redirect(reverse("dailyfreshgoods:index"))
