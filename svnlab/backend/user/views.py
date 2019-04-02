"""
user.views
~~~~~~~~~~

This module implements the Requests Views.
View is an logical management library, written in Python, for user beings.

:copyright: (c) 2019 by JiuChou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.01.13
"""
import json
import os

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from rest_framework.views import APIView

from svnlab.common.custom_ldap import CustomLdap
from svnlab.common.decorator import get_token, get_username

from svnlab.common.user_utils import userLogon

from .CustomLdap import MyLdap
from .models import UserRole, ModuleRole

class UserLoginView(APIView):
    """View of user login operation.
    """
    # ldap的地址和端口号
    AUTH_LDAP_SERVER_URI = 'ldap://10.1.2.180:389'

    def post(self, request):
        """User Login by LDAP server
        """
        response = {}
        req = json.loads(request.body.decode())
        username = req['username']
        password = req['password']
        try:
            custom_ldap = CustomLdap(self.AUTH_LDAP_SERVER_URI,
                                     username,
                                     password)
            user_info = custom_ldap.get_user_info(username)
            token = get_token(username)
            response['token'] = token
            response['user_info'] = user_info
            response['message'] = "SUCCESS: Login successful!"
            response['status_code'] = 200
            return JsonResponse(response)
        except Exception as e:
            response['message'] = "ERROR: Login failed! {0}".format(e)
            response['status_code'] = 401
            return JsonResponse(response)

def getUserPermissionList(request):
    """Get developer roles info
    """
    response = {}
    token = request.META.get('HTTP_AUTHORIZATION')
    print(token)

    try:
        username = get_username(token)
        req = request.GET
        username = req['username']
        page = req['page']
        limit = req['limit']

        roles = UserRole.objects.filter(username=username)\
                                .exclude(role=0)\
                                .values("username",
                                        "role",
                                        "module",
                                        "path",
                                        "url",
                                        "manager").order_by("url")
        response['total'] = len(roles)

        role_list = []
        paginator = Paginator(roles, limit)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of resluts.
            contacts = paginator.page(paginator.num_pages)

        for role in contacts:
            role_list.append(role)

        response['role_list'] = role_list
        response['message'] = "SUCCESS: Get user permission lists successful!"
        response['status_code'] = 200
    except Exception as e:
        response['message'] = "ERROR: Verify authentication failed! {0}".format(e)
        response['status_code'] = 401
        return JsonResponse(response)
    return JsonResponse(response)

def getModuleSvnList(request):
    """PermissionManagement-Module
    Get Permission list by manager when user is module manager.
    """
    response = {}
    # 获取请求参数
    req = request.GET
    # Token = req['Token']
    username = req['username']
    manager = req['username']

    # 从数据库读取数据
    moduleRoleList = ModuleRole.objects.filter(manager=manager).values('path', 'url', 'module', 'manager', 'readOnlyUserNum', 'readAndWriteUserNum').order_by('url')

    response['data'] = {
        'total': len(moduleRoleList),
        'moduleRoleList': list(moduleRoleList)
    }
    response['message'] = 'Success: get module permission lists success!'
    response['status'] = 200

    return JsonResponse(response)

def getModuleSvnDetail(request):
    """PermissionManagement-Module
    Get Permission list by manager when user is module manager.
    """
    response = {}
    # 获取请求参数
    req = request.GET
    print(req)
    # Token = req['Token']
    # username = req['username']

    return JsonResponse(response)

def refreshModulePermissionList(request):
    """PermissionManagement-Module
    Refresh Permission list by manager when user is module manager.
    """
    response = {}
    # 获取请求参数
    req = request.GET
    # Token = req['Token']
    manager = req['username']
    
    # 根据模块名获取当前所有模块的地址和权限情况
    # 将获取到到数据写入到数据库
    # ParaseModuleRoleToDB
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    result = os.system("chmod +x {0}/common/roleUtils/*.sh; {0}/common/roleUtils/getModuleRole.sh {1};".format(BASE_DIR, manager))
    if result == 0:
        print("Success: Parase {0}'s manage module role to database success!".format(username))
    else:
        print("Error: Parase {0}'s manage module role to database failed!".format(username))

    response['message'] = 'Success: refresh module permission lists success!'
    response['status'] = 200

    return JsonResponse(response)
