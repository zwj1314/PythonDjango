"""MyFirstDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from booktest import views

urlpatterns = [

    #简单字符匹配，若为空则调用
    path('', views.index),
    # 正则表达中添加括号，则表示将括号中的信息传递给request
    re_path('^(\d+)$', views.show),
    path('admin/', admin.site.urls),
    re_path('^booktest/', include('booktest.urls', namespace="booktest")),
    re_path('^tinymce/', include('tinymce.urls')),
    re_path(r'^search/', include('haystack.urls')),
]
