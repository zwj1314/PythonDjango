
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

    #验证码
    re_path('^verifyCode', views.verifyCode),
    re_path('^verifyTest2', views.verifyTest2),
    re_path('^verifyTest1/', views.verifyTest1),

    #上传图片
    re_path('^uploadPic', views.uploadPic),
    re_path('^uploadHandle', views.uploadHandle),

    #省市选择
    re_path('^area$', views.area),
    re_path('^pro', views.pro),
    re_path('^city(\d+)', views.city),
    re_path('^dis(\d+)',views.dis),

    #富文本
    re_path('^htmlEditor$', views.htmlEditor),
    re_path('^htmlEditorHandle/', views.htmlEditorHandle),

    #缓存
    re_path('^cache1', views.cache1),

    #全文搜索
    re_path('^mysearch', views.mysearch),

    #
    re_path('^celeryTest', views.celeryTest),




]