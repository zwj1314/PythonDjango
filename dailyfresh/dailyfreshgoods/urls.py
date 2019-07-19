from django.urls import path,re_path
from dailyfreshgoods import views

app_name = '[dailyfreshgoods]'
urlpatterns = [

    re_path('^(\d+)$', views.detail, name='detail'),
    re_path('^list(\d+)_(\d+)_(\d+)$', views.list, name='list'),
    re_path('^$', views.index, name='index'),
    re_path('^search', views.ordinary_search, name='ordinary_search'),


]