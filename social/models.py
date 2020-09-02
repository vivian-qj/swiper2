from django.db import models

# Create your models here.
#滑动模块
class Swiper(models.Model):
    STATUS = (
        ('superlike', '超级喜欢'),
        ('like','喜欢'),
        ('dislike', '不喜欢'),
    )

    uid = models.IntegerField(verbose_name= '滑动者的UID')#滑动者的UID
    sid = models.IntegerField(verbose_name= '被滑动者的UID')#被滑动者的UID

    status = models.CharField(max_length=8, choices=STATUS)
    time = models.DateTimeField(auto_now_add=True)#auto_now_add：创建的时间；auto_now：每次保存的时间

'''好友模块'''
class Friend(models.Model):
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()