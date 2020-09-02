from django.shortcuts import render
from lib.http import render_json

from social.logic import get_rcmd_users
# Create your views here.

def get_users(request):
    '''获取推荐列表'''
    #逻辑写入logic里
    #分页处理（5个一组）
    group_num = int(request.GET.get('group_num',0))#第几页
    start = group_num*5
    end = start + 5
    users = get_rcmd_users(request.user)[start:end]#5个一页

    result = [user.to_dict() for user in users]

    return render_json(result)

def like(request):
    '''喜欢'''
    return render_json(None)

def superlike(request):
    '''超级喜欢'''
    return render_json(None)

def dislike(request):
    '''不喜欢'''
    return render_json(None)

def rewind(request):
    '''反悔'''
    return render_json(None)



