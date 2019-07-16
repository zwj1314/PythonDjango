from django.contrib import admin
from django.urls import path,re_path,include
from . import views

app_name = '[dailyfreshorder]'
urlpatterns = [

    re_path(r'^$', views.order, name="order"),
    re_path(r'^push/$', views.order_handle, name="push"),
]