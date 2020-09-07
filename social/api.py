from django.shortcuts import render
from lib.http import render_json

from social import logic
from social.models import Friend
from vip.logic import perm_require
# Create your views here.

def get_users(request):
    '''获取推荐列表'''
    #逻辑写入logic里
    #分页处理（5个一组）
    group_num = int(request.GET.get('group_num',0))#第几页
    start = group_num*5
    end = start + 5
    users = logic.get_rcmd_users(request.user)[start:end]#5个一页

    result = [user.to_dict() for user in users]

    return render_json(result)

def like(request):
    '''喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logic.like(request.user, sid)#是否完成了匹配
    return render_json({'is_matched': is_matched})

@perm_require('superlike')#完全可以不用修改原函数，直接在上面加上装饰器实现权限功能；若是不用权限直接注释
def superlike(request):
    '''超级喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logic.superlike(request.user, sid)  # 是否完成了匹配
    return render_json({'is_matched': is_matched})


def dislike(request):
    '''不喜欢'''
    sid = int(request.POST.get('sid'))
    logic.dislike(request.user, sid)  # 是否完成了匹配
    return render_json(None)

@perm_require('rewind')
def rewind(request):
    '''反悔'''
    sid = int(request.POST.get('sid'))
    logic.rewind(request.user, sid)  # 是否完成了匹配
    return render_json(None)

def friends(request):
    '''好友列表'''
    my_friends = Friend.friends(request.user.id)
    friends_info = [frd.to_dict() for frd in my_friends]
    return render_json({'friends':friends_info})



