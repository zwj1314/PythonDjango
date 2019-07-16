from django.urls import path,re_path
from dailyfreshuser import views

app_name = '[dailyfreshuser]'
urlpatterns = [

    # 用户注册
    re_path('^register/$', views.register, name="register"),
    # register.html 进行ajax请求，查看用户名是否已经存在
    re_path('^register_exist', views.register_exist, name="register_exist"),
    # 接收注册提交过来的的信息
    re_path('^register_handle', views.register_handle, name="register_handle"),
    # 注册完成后跳转到登陆页面，注意：这里的login必须完全匹配（$），不然后面的login_handle无法匹配
    re_path('^login$', views.login, name="login"),
    # 处理登陆时提交过来的信息，若验证成功则跳转到用户信息info界面
    re_path('^login_handle', views.login_handle, name="login_handle"),
    # 用户信息界面
    re_path('^info', views.info, name="info"),
    # 订单模块
    re_path('^order/(\d+)', views.order, name="order"),
    # 收货地址
    re_path('^site', views.site, name="site"),
    # 用户登出
    re_path('^logout', views.logout, name="logout"),


]