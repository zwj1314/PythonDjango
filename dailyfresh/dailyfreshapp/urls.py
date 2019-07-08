from django.urls import path,re_path
from dailyfreshapp import views


urlpatterns = [

    re_path('^register/$', views.register),
    re_path('^register_handle', views.register_handle),
    re_path('^login', views.login),
    re_path('^register_exist', views.register_exist),

]