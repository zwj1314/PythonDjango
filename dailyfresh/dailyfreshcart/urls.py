from django.contrib import admin
from django.urls import path,re_path,include
from . import views


app_name = '[dailyfreshcart]'
urlpatterns = [

    re_path('^$', views.user_cart, name="cart"),
    #re_path('^add(?P<gid>\d+)_(?P<count>\d+)/', views.add, name="add"),
    re_path('^add(\d+)_(\d+)/', views.add, name="add"),
    re_path('^edit(\d+)_(\d+)/', views.edit, name="edit"),
    re_path('^delete(\d+)/', views.delete, name="delete"),

]