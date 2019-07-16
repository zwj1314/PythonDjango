from django.contrib import admin
from .models import UserInfo, GoodsBrowser

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ["uname", "uemail", "ureceiveaddr", "uaddress", "upostcode", "uphone"]
    list_per_page = 5
    list_filter = ["uname", "upostcode"]
    search_fields = ["uname", "upostcode"]
    readonly_fields = ["uname"]


class GoodsBrowserAdmin(admin.ModelAdmin):
    list_display = ["user", "goods"]
    list_per_page = 50
    list_filter = ["user__uname", "goods__gtitle"]
    search_fields = ["user__uname", "goods__gtitle"]
    readonly_fields = ["user", "goods"]
    refresh_times = [3, 5]


admin.site.site_header = '天天生鲜后台管理系统'
admin.site.site_title = '天天生鲜后台管理系统'

admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(GoodsBrowser, GoodsBrowserAdmin)
