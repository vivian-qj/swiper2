from django.db import models
import datetime
from lib.orm import ModelMixin
# Create your models here.

class User(models.Model):
    '''用户数据模型'''

    SEX = (
        ('男','男'),#第一项是记录在数据库里的
        ('女','女')
    )
    nickname = models.CharField(max_length=30, unique=True)
    sex = models.CharField(max_length=8, choices=SEX)
    phonenum = models.CharField(max_length=16, unique=True)

    avatar =models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    birth_year = models.IntegerField(default=2002)
    birth_month = models.IntegerField(default=1)
    birth_day = models.IntegerField(default=1)

    @property
    def age(self):
        today = datetime.date.today()
        birth_date = datetime.date(self.birth_year, self.birth_month, self.birth_day)
        return (today - birth_date).days//365


    @property
    def profile(self):

        if not hasattr(self, '_profile'): #等价于self._profile not in self.__dict__
            self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    def to_dict(self):
        return {
            'id' : self.id,
            'nickname': self.nickname,
            'sex': self.sex,
            'phonenum': self.phonenum,

            'avatar': self.avatar,
            'location': self.location,
            'age': self.age
        }


class Profile(models.Model, ModelMixin):
    SEX = (
        ('男', '男'),  # 第一项是记录在数据库里的
        ('女', '女')
    )

    dating_sex = models.CharField(default='女', max_length=8, choices=SEX, verbose_name='匹配的性别')
    location = models.CharField(max_length=80, verbose_name='目标城市')

    min_distance = models.IntegerField(default=1, max_length=30, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10, max_length=30, verbose_name='最大查找范围')

    min_dating_age = models.IntegerField(default=18, max_length=30, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=45, max_length=30, verbose_name='最大交友年龄')

    vibration = models.BooleanField(default=True, verbose_name='是否开启震动')
    only_matche = models.BooleanField(default=True, verbose_name='是否让匹配的人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='是否自动播放视频')
