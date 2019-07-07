from django.shortcuts import render,redirect
from booktest.models import *
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
#from django.template import RequestContext,loader
from django.conf import settings
import os
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from booktest.task import sayhello

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


# 验证码练习
def verifyCode(request):
    #引入绘图模块
    from PIL import Image,ImageDraw,ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色（RGB）、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    #创建画面
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    #构造字体对象
    font = ImageFont.truetype('Arial Bold.ttf', 23)
    #调用画笔的line()函数绘制干扰线
    for i in range(0, 50):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        # 绘制线
        draw.line([begin, end], fill=fill)
    #调用画笔的point()函数绘制干扰点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        # 绘制点
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选择4个值作为验证码
    rand_str = ''
    for i in range(4):
        temp_str = str1[random.randrange(0, len(str1))]
        rand_str += temp_str
        # 总宽度为100，每个字符从0，25...开始绘制
        draw.text((i*25,0),
                  temp_str,
                  (255, 255, 255),
                  font)
    #释放画笔
    del draw
    #session中记录验证码，与用户输入的进行对比
    request.session['code'] = rand_str
    #将图片保存到内存流中
    import io
    buf = io.BytesIO()
    im.save(buf, 'png')
    #将内存流中的内容输出到客户端
    return HttpResponse(buf.getvalue(), 'image/png')

def verifyTest1(request):
    return render(request, 'booktest/verifyTest1.html')

def verifyTest2(request):
    code1 = request.POST['code1']
    code2 = request.session['code']
    return HttpResponse('OK' if str(code1).lower() == str(code2).lower() else 'False')

#上传图片
def uploadPic(request):
    return render(request, 'booktest/uploadPic.html')

def uploadHandle(request):
    if request.method == "POST":
        f1 = request.FILES['pic1']
        #fname = '%sbooktest/%s' %(settings.MEDIA_ROOT, f1.name)
        fname = os.path.join(settings.MEDIA_ROOT, f1.name)
        with open(fname, 'wb') as pic:
            for c in f1.chunks():
                pic.write(c)
        return HttpResponse("上传成功，文件已经存储在" + '<img src="/static/media/%s"/>' %f1.name)
    else:
        return HttpResponse("Error")


#省市区选择
def area(request):
    return render(request, 'booktest/area.html')

def pro(request):
    proList = AreaInfo.objects.filter(parea__isnull=True) #.values()
    # # [{},{},{}]=====>{data:[]}
    # data1 = {'data':data}
    list = []
    # [[1,'北京'],[2,'天津'],...]
    for item in proList:
        list.append([item.id, item.title])#[1,'北京']
    # list--->[[],[],[]]
    return JsonResponse({'data':list})

def city(request, id):
    #parea_id=id 输入的省的id和数据库中某些数据的parea_id相等，不需要关联
    # parea__id=id 根据输入的id查找到parea，再找到parea_id和输入的id相同。
    cityList = AreaInfo.objects.filter(parea_id=id)
    list = []
    #[{id:1,title:北京},{id:2,title:天津},...]
    for item in cityList:
        list.append({'id':item.id,'title':item.title})
    return JsonResponse({'data':list})

def dis(request, id):
    #parea_id=id 输入的省的id和数据库中某些数据的parea_id相等，不需要关联
    # parea__id=id 根据输入的id查找到parea，再找到parea_id和输入的id相同，将parea_id与id关联
    disList = AreaInfo.objects.filter(parea_id=id)
    list = []
    #[{id:1,title:北京},{id:2,title:天津},...]
    for item in disList:
        list.append({'id':item.id,'title':item.title})
    return JsonResponse({'data':list})

#自定义编辑器
def htmlEditor(request):
    return render(request, 'booktest/htmlEditor.html')

def htmlEditorHandle(request):
    html = request.POST['hcontent']
    #改写更新这个模型类，先查询之前存储的信息
    test1 = Test1.objects.get(pk=1)
    test1.content = html
    test1.save()
    context = {'content':html}
    return render(request, 'booktest/htmlShow.html', context)

#添加视图缓存
@cache_page((60 * 15))
def cache1(request):
    #return HttpResponse('hello1')
    #return HttpResponse('hello2')
    cache.set('key1', 'value1', 600)
    return render(request, 'booktest/cache1.html')


#全文搜索+结巴分词
def mysearch(request):
    return render(request, 'booktest/mysearch.html')

#
def celeryTest(request):
    # print('hello ...')
    # import time
    # time.sleep(10)
    # print('world ...')
    #sayhello()
    sayhello.delay()

    return HttpResponse("hello world")






















