from django.db import models
from django.db.models import Q
from user.models import User
# Create your models here.
#滑动模块
class Swiped(models.Model):
    STATUS = (
        ('superlike', '超级喜欢'),
        ('like','喜欢'),
        ('dislike', '不喜欢'),
    )

    uid = models.IntegerField(verbose_name= '滑动者的UID')#滑动者的UID
    sid = models.IntegerField(verbose_name= '被滑动者的UID')#被滑动者的UID

    status = models.CharField(max_length=8, choices=STATUS)
    time = models.DateTimeField(auto_now_add=True)#auto_now_add：创建的时间；auto_now：每次保存的时间

    @classmethod
    def mark(cls, uid, sid, status):
        '''标记一次滑动'''
        if status in ['superlike', 'like', 'dislike']:
            #因为可能会推送两次一样的人
            defaults = {'status': status}
            cls.objects.update_or_create(uid=uid, sid=sid , defaults=defaults)

    @classmethod
    def is_like(cls, uid, sid):
        '''检查你喜欢的是否喜欢你'''
        cls.objects.filter(uid=uid,sid=sid, #uid = sid调用的时候反着写，不然别扭
                           status__in=['like','superlike']).exists()#看它村不存在


'''好友模块'''
class Friend(models.Model):
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()
    @classmethod
    def be_friends(cls, uid1, uid2):
        '''成为好友'''
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        cls.objects.get_or_create(uid1=uid1)

    @classmethod
    def is_friend(cls, uid1, uid2):
        '''检查是否为好友'''
        condition = Q(uid1=uid1, uid2=uid2) | Q(uid1=uid2, uid2=uid1)
        cls.objects.filter(condition).exists()
    @classmethod
    def break_off(cls, uid1, uid2):
        '''断绝好友关系'''
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        try:
            cls.objects.get(uid1=uid1, uid2=uid2).delete()

        except cls.DoesNotExist:
            pass

    @classmethod
    def friends(cls, uid):
        condition = Q(uid1=uid) | Q(uid2=uid)#uid可能在uid1/uid2里，把他们都挑选出来
        relations = cls.objects.filter(condition)#过滤出我的好友关系，其中既包含我的ID也包含好友的ID
        friend_id_list = []
        #找出好友的ID
        for r in relations:
            friend_id = r.uid2 if r.uid1==uid else r.uid1
            friend_id_list.append(friend_id)

        return User.objects.filter(id__in=friend_id_list)#返回好友对象
