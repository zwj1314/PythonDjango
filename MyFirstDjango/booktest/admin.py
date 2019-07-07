from django.contrib import admin
from booktest.models import *

class HeroInfoInline(admin.TabularInline): #StackedInline
    # 级连，添加书籍的同时添加英雄信息
    model = HeroInfo
    # 添加的英雄信息的个数
    extra = 2

#方式二、装饰器方式注册
#@admin.register(BookInfo)
class BookInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'btitle', 'bpub_date']
    list_filter = ['btitle']
    search_fields = ['btitle']
    list_per_page = 10
    fieldsets = [
        ('base', {'fields':['btitle']}),
        ('super',{'fields':['bpub_date']})
    ]
    inlines = [HeroInfoInline]

# 方式一、Register your models here.
admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo)
admin.site.register(Test1)



