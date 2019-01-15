'''
user.views
~~~~~~~~~

This module implements the Requests Views.
View is an logical management library, written in Python, for user beings.

:copyright: (c) 2019 by JiuChou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.01.13
'''

# built-in library
import json

# third-party library
from django.core import serializers
#分页功能
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from rest_framework.views import APIView

# user-defined
# 安装时存在svnlab.common库
from svnlab.common import userUtils
from .CustomLdap import MyLdap
from .models import UserRole, ModuleRole

class UserLoginView(APIView):
    '''View of user login operation.
    '''
    # ldap的地址和端口号
    AUTH_LDAP_SERVER_URI = 'ldap://10.1.2.180:389'

    def post(self, request):
        '''
        User Login by LDAP server.
        '''
        response = {}
        req = json.loads(request.body.decode())
        username = req['username']
        password = req['password']
        myLdap = MyLdap(self.AUTH_LDAP_SERVER_URI, username, password)
        result, ldapUserInfo = myLdap.ldap_search(username)
        if result:
            customUserInfo = userUtils.userLogon(username, ldapUserInfo)
            # 生成随机字符串
            if request.session.get('username'):
                del request.session["username"]
            request.session['username'] = username
            request.session.set_expiry(60)
            response['data'] = {
                'token': request.session.session_key,
                'userInfo': customUserInfo
            }
            response['message'] = 'Login Success'
            response['status'] = 200

        return JsonResponse(response)

def getUserPermissionList(request):
    '''View of user role operation.
    '''
    response = {}
    req = request.GET
    username = req['username']
    page = req['page']

    userRoleList = UserRole.objects.filter(username=username).values('username', 'role', 'module', 'path', 'url', 'manager').order_by('url')
    print(userRoleList)
    total = len(userRoleList)

    userRoleListByPaginator = []
    # show 10 contacts per page
    paginator = Paginator(userRoleList, 20)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of resluts.
        contacts = paginator.page(paginator.num_pages)
    for role in contacts:
        userRoleListByPaginator.append(role)

    response['data'] = {
        'total': total,
        'roleList': userRoleListByPaginator
    }
    response['message'] = 'Success: get user permission lists success!'
    response['status'] = 200

    return JsonResponse(response)
