"""
common.custom_ldap
~~~~~~~~~~~~~~~~~~

This module implements the custom operation of LDAP server.

:copyright: (c) 2019 by JiuChou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.03.25
"""
import json
import ldap
import os

from rest_framework.exceptions import APIException

class CustomLdap(object):
    """
    docstring
    """
    # Authentication: LDAP two
    # root DN
    AUTH_LDAP_BIND_DN = "OU=大华技术,DC=dahuatech,DC=com"
    AUTH_LDAP_BIND_PASSWORD = ""
    AUTH_DOMAIN = "dahuatech"
    # cn, uid, sAMAccountName
    AUTH_LDAP_USER_SEARCH_FILTER_NAME = "sAMAccountName"
    # Retrieve attributes from ldap
    AUTH_LDAP_USER_ATTR_MAP = None
    # AUTH_LDAP_USER_ATTR_MAP = {
    #     'username': 'sAMAccountName',
    #     'email': 'mail',
    #     'telephone': 'telephone',
    #     'truename': 'givenName'
    # }

    def __init__(self, server_uri, username="", password=""):
        """docstring
        """
        self.server_uri = server_uri
        self.ldap_obj = None
        self.ldap_connect(username, password)

    def ldap_connect(self, username="", password=""):
        """docstring
        """
        url = self.server_uri
        conn = ldap.initialize(url)
        conn.protocol_version = ldap.VERSION3
        if username and not password:
            raise APIException("ERROR: Please input password!")
        try:
            username = '{0}\\{1}'.format(self.AUTH_DOMAIN, username)
            rest = conn.simple_bind_s(username, password)
        except ldap.SERVER_DOWN:
            raise APIException("ERROR: Can't connect to LDAP!")
        except ldap.INVALID_CREDENTIALS:
            raise APIException("ERROR: LADP user failed!")
        except Exception as e:
            raise APIException(type(e))
        # 97 表示success
        if rest[0] != 97:
            raise APIException(rest[1])
        self.ldap_obj = conn

    def ldap_search(self, username=""):
        """
        AUTH_LDAP_BIND_DN: 域
        AUTH_LDAP_USER_SEARCH_FILTER_NAME: 搜索策略
        AUTH_LDAP_USER_ATTR_MAP: 同步账户信息到django的auth_user表中
        username: 搜索的用户
        """
        AUTH_LDAP_USER_SEARCH_FILTER = "({0}={1})".format(
            self.AUTH_LDAP_USER_SEARCH_FILTER_NAME,
            username)
        try:
            search_id = self.ldap_obj.search(self.AUTH_LDAP_BIND_DN,
                                             ldap.SCOPE_SUBTREE,
                                             AUTH_LDAP_USER_SEARCH_FILTER,
                                             self.AUTH_LDAP_USER_ATTR_MAP)
            _, user_data = self.ldap_obj.result(search_id)
            if not user_data:
                return False, []
        except ldap.LDAPError as e:
            raise APIException(e)
        return True, user_data

    def _store_role_to_db(self, username):
        # Parse role to database
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cmd = "bash {0}/common/roleUtils/getUserRole.sh {1}".format(BASE_DIR,
                                                                    username)
        result = os.system(cmd)
        if result == 0:
            message = "SUCCESS: Parse {0}'s role to database!".format(username)
            print(message)
        else:
            message = "ERROR: Parse {0}'s role to database!".format(username)
            print(message)

    def get_user_info(self, username):
        """
        1.获取用户基础信息
        2.解析用户权限，存放至数据库
        """
        response = {}
        result, user_info = self.ldap_search(username)
        user_info = json.dumps(str(user_info[0][0]), ensure_ascii=False)
        print(user_info)
        truename = user_info.split(",")[0].split("=")[1]
        response = {
            'username': username,
            'roles': "guster",
            'truename': truename,
            'sex': "",
            'email': "",
            'telephone': "",
            'introduction': "",
            'profile_photos': "",
            'join_time': "",
            'login_time': ""
        }
        self._store_role_to_db(username)

        return response
