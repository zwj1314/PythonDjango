
from django.urls import path,re_path
from booktest import views

# 解决Django2中遇到在根目录下urls.py中的include方法的第二个参数namespace添加之后就出错的问题。请在[app_name]目录下的urls.py中的urlpatterns前面加上app_name='[app_name]'
app_name = '[booktest]'
urlpatterns = [

    # 正则表达中添加括号，则表示将括号中的信息传递给request
    #re_path('^getTest1/', views.getTest1),
    re_path('^postTest1/', views.postTest1),

    # 调用views中的postTest2函数，返回相应的参数和页面
    re_path('^postTest2/', views.postTest2),

    # 调用cookie
    re_path('^cookieTest/', views.cookieTest),

    # 重定向
    re_path('^redirectTest1/', views.redirectTest1),
    re_path('^redirectTest2/', views.redirectTest2),

    # session
    re_path('^session1/', views.session1),
    re_path('^session2/', views.session2),
    re_path('^session2_handle/', views.session2_handle),
    re_path('^session3/', views.session3),

    # 反向解析
    re_path('^(\d+)/(\d+)/', views.show1, name="show1"),


]