from django.db import models
from datetime import datetime
from dailyfreshgoods.models import GoodsInfo

class UserInfo(models.Model):
    """
    default,blank是python层面的约束，不影响数据库表的结构，若更改不需要重新迁移
    null=True是数据库表结构的更改，若修改则需要重新迁移
    """
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    ureceiveaddr = models.CharField(max_length=200 ,default='')
    uaddress = models.CharField(max_length=200 ,default='')
    upostcode = models.CharField(max_length=6 ,default='')
    uphone = models.CharField(max_length=11 ,default='')

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.uname

# 用户的浏览记录
class GoodsBrowser(models.Model):
    """
    用户的浏览记录，关联用户表和商品表
    """
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="用户ID")
    goods = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="商品ID")
    browser_time = models.DateTimeField(default=datetime.now, verbose_name="浏览时间")

    class Meta:
        verbose_name = "用户浏览记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}浏览记录{1}".format(self.user.uname, self.goods.gtitle)