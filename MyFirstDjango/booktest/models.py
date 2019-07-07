from django.db import models
from tinymce.models import HTMLField

class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateTimeField()
    # 若添加下面代码，则数据库中的表名则会更改为制定的表名
    # class Meta():
    #     db_table = 'bookinfo'
    def __str__(self):
        return self.btitle


class HeroInfo(models.Model):
    hname = models.CharField(max_length=10)
    hgender = models.BooleanField()
    hcontent = models.CharField(max_length=1000)
    '''
    在django2.0后，定义外键和一对一关系的时候需要加on_delete选项，此参数为了避免两个表里的数据不一致问题
    on_delete有CASCADE、PROTECT、SET_NULL、SET_DEFAULT、SET()五个可选择的值
    CASCADE：此值设置，是级联删除。
    PROTECT：此值设置，是会报完整性错误。
    SET_NULL：此值设置，会把外键设置为null，前提是允许为null。
    SET_DEFAULT：此值设置，会把设置为外键的默认值。
    SET()：此值设置，会调用外面的值，可以是一个函数。
    '''
    hbook = models.ForeignKey(BookInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.hname

class AreaInfo(models.Model):
    title = models.CharField(max_length=20)
    parea = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

class Test1(models.Model):
    content = HTMLField()
