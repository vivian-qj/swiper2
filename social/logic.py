import datetime
from user.models import User
from social.models import Swiped,Friend

def get_rcmd_users(user):#user = User.objects.get(id=1)
    '''获取推荐用户'''
    sex = user.profile.dating_sex
    location = user.profile.location
    min_age = user.profile.min_dating_age
    max_age = user.profile.max_dating_age

    current_year = datetime.date.today().year
    max_year = current_year - min_age
    min_year = current_year -max_age

    users = User.objects.filter(sex=sex, location=location,
                        birth_year__gte=min_year, birth_year__lte=max_year)
    return users

def like(user, sid):
    '''喜欢一个用户右滑'''
    Swiped.mark(user.id, sid ,'like')
    #检查被滑动着是否喜欢过自己
    if Swiped.is_like(sid,user.id):
        Friend.be_friends(user.id, sid)#添加好友记录
        return True
    else:
        return False

def superlike(user, sid):
    '''超级喜欢一个用户'''
    Swiped.mark(user.id, sid ,'superlike')
    #检查被滑动着是否喜欢过自己
    if Swiped.is_like(sid,user.id):
        Friend.be_friends(user.id, sid)#添加好友记录
        return True
    else:
        return False


def superlike(user, sid):
    '''不喜欢一个用户'''
    Swiped.mark(user.id, sid, 'dislike')

def rewind(user, sid):
    '''反悔'''
    try:
        #取消滑动记录
        Swiped.objects.get(uid=user.id, sid=sid).delete()#表示原来滑到过的记录
    except Swiped.DoesNotExist:
        pass
    #撤销好友关系
    Friend.break_off(user.id, sid)