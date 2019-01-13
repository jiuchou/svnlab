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
from django.http import JsonResponse
from rest_framework.views import APIView

# user-defined
# 安装时存在svnlab.common库
from svnlab.common.user import userLogon
from .CustomLdap import MyLdap

class UserLoginView(APIView):
    '''
    View of user login operation.
    '''
    # ldap的地址和端口号
    AUTH_LDAP_SERVER_URI = 'ldap://10.1.2.180:389'

    def get(self, request):
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
            customUserInfo = userLogon(username, ldapUserInfo)
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
