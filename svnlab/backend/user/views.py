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
import os

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
        'userRoleList': userRoleListByPaginator
    }
    response['message'] = 'Success: get user permission lists success!'
    response['status'] = 200

    return JsonResponse(response)

def getModuleSvnList(request):
    '''PermissionManagement-Module
    Get Permission list by manager when user is module manager.
    '''
    response = {}
    # 获取请求参数
    req = request.GET
    # Token = req['Token']
    username = req['username']
    manager = req['manager']

    # 根据模块名获取当前所有模块的地址和权限情况
    # 将获取到到数据写入到数据库
    # ParaseModuleRoleToDB
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    result = os.system("chmod +x {0}/common/roleUtils/*.sh; {0}/common/roleUtils/getModuleRole.sh {1};".format(BASE_DIR, manager))
    if result == 0:
        print("Success: Parase {0}'s role to database success!".format(username))
    else:
        print("Error: Parase {0}'s role to database failed!".format(username))

    # 从数据库读取数据
    moduleRoleList = ModuleRole.objects.filter(manager=manager).all().order_by('url')
    moduleRoleList = serializers.serialize("json", moduleRoleList)
    total = len(moduleRoleList)
    response['data'] = {
        'total': total,
        'moduleRoleList': moduleRoleList
    }
    response['message'] = 'Success: get module permission lists success!'
    response['status'] = 200

    return JsonResponse(response)

def getModuleSvnDetail(request):
    '''PermissionManagement-Module
    Get Permission list by manager when user is module manager.
    '''
    response = {}
    # 获取请求参数
    req = request.GET
    print(req)
    # Token = req['Token']
    # username = req['username']

    return JsonResponse(response)
