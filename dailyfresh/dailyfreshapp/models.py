from django.db import models

# Create your models here.
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
