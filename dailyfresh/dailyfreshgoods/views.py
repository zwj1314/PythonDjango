from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from dailyfreshcart.models import *

def index(request):
    # 查询各个分类的最新4条，最热4条数据
    typelist = TypeInfo.objects.all()
    #  _set 连表操作
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]  # 按照上传顺序
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]  # 按照点击量
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]

    cart_num = 0
    # 判断是否存在登录状态
    # if request.session.has_key('user_id'):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    context = {
        'title': '首页',
        'cart_num': cart_num,
        'guest_cart': 1,
        'type0': type0, 'type01': type01,
        'type1': type1, 'type11': type11,
        'type2': type2, 'type21': type21,
        'type3': type3, 'type31': type31,
        'type4': type4, 'type41': type41,
        'type5': type5, 'type51': type51,
    }

    return render(request, 'dailyfreshgoods/index.html', context)


def list(request, tid, pindex, sort):
    """

    :param request:
    :param tid:
    :param pindex:
    :param sort:
    :return:
    """
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort == 1: # 默认
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort == 2: # 价格
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == 3: #人气，点击量
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
    paginator = Paginator(goods_list, 4)
    page = paginator.page(int(pindex))
    context = {
        'title':typeinfo.ttitle,
        'guest_cart':1,
        'page':page,
        'typeinfo':typeinfo,
        'sort':sort,
        # 新品推荐
        'news':news
    }
    return render(request, 'dailyfreshgoods/list.html', context)


def detail(request, id):
    goods = GoodsInfo.objects.get(pk=int(id))
    goods.gclick = goods.gclick + 1
    goods.save()
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {
        'title':goods.gtype.ttitle,
        'guest_cart':1,
        'g':goods,
        'news':news,
        'id':id
    }
    return render(request, 'dailyfreshgoods/detail.html', context)


