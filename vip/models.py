from django.db import models

# Create your models here.
'''
VIP - User 一对多
VIP - Permission 多对多
'''
class Vip(models.Model):
    #Vip与用户是一对多的关系，在多的地方增家vip_id
    name = models.CharField(max_length=32, unique=True)
    level = models.IntegerField()
    price = models.FloatField()

    def perms(self):
        '''当前VIP具有的权限'''
        #根据你的Vip的ID找到该VIP对应的权限的关系(一个VIP跟多个权限有关系)；
        #根据这个关系线找到提取对应的权限ID
        #根据权限ID找到权限名
        relations = VipPermRelation.objects.filter(vip_id=self.id)
        perm_id_list = [r.perm_id for r in relations]
        return Permission.objects.filter(id__in=perm_id_list)

    def has_perm(self,perm_name):
        '''检查是否具有某种权限'''
        #根据name创建perm对象，根据对象ID与VIP的ID找他们之间的关系
        perm = Permission.objects.get(name=perm_name)
        return VipPermRelation.objects.filter(vip_id=self.id, perm_id=perm.id).exists()

#一个子段只能对应一章表，所以权限和VIP应该分开写
class Permission(models.Model):
    '''
    权限表：
        vipflag         会员标识
        superlike       超级喜欢
        rewind          反悔功能
        anylocation     任意更改定位
        unlimit_like    无限喜欢次数
    '''
    name = models.CharField(max_length=32, unique=True)

'''
关系表里面的每一条记录都记录者一个唯一的关系
vip_id        perm_id
会员1         会员标识-----多对多关系
会员1         超级喜欢
会员2         会员标识
会员2         反悔功能
会员2         无限喜欢次数
会员3         会员标识
会员3         超级喜欢
会员3         反悔功能
会员3         任意更改定位
会员3         无限喜欢次数

'''

class VipPermRelation(models.Model):
    '''
    会员权限  关系表
    会员套餐一：
        会员标识-----多对多关系
        超级喜欢
    会员套餐二：
        会员标识
        反悔功能
        无限喜欢次数
    会员套餐三：
        会员标识
        超级喜欢
        反悔功能
        任意更改定位
        无限喜欢次数

    '''
    vip_id = models.IntegerField()
    perm_id = models.IntegerField()