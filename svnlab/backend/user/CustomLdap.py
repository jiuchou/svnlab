'''
user.CustomLdap
~~~~~~~~~

This module implements the custom operation of LDAP server.

:copyright: (c) 2019 by JiuChou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.01.13
'''

# third-party library
from rest_framework.exceptions import APIException
import ldap

class MyLdap:
    '''
    docstring
    '''
    # Authentication: LDAP two
    # root DN
    AUTH_LDAP_BIND_DN = 'OU=大华技术,DC=dahuatech,DC=com'
    AUTH_LDAP_BIND_PASSWORD = ''
    AUTH_DOMAIN = 'dahuatech'
    # cn, uid, sAMAccountName
    AUTH_LDAP_USER_SEARCH_FILTER_NAME = 'sAMAccountName'
    # Retrieve attributes from ldap
    AUTH_LDAP_USER_ATTR_MAP = None
    # AUTH_LDAP_USER_ATTR_MAP = {
    #     'username': 'sAMAccountName',
    #     'email': 'mail',
    #     'telephone': 'telephone',
    #     'truename': 'givenName'
    # }

    def __init__(self, server_uri, username='', password=''):
        '''
        docstring
        '''
        self.server_uri = server_uri
        self.ldap_obj = None
        self.ldap_connect(username, password)

    def ldap_connect(self, username='', password=''):
        '''
        docstring
        '''
        url = self.server_uri
        conn = ldap.initialize(url)
        conn.protocol_version = ldap.VERSION3
        if username and not password:
            raise APIException("Please input password!")
        try:
            username = '{0}\\{1}'.format(self.AUTH_DOMAIN, username)
            rest = conn.simple_bind_s(username, password)
        except ldap.SERVER_DOWN:
            raise APIException("Can't connect to LDAP!")
        except ldap.INVALID_CREDENTIALS:
            raise APIException("LADP user failed!")
        except Exception as e:
            raise APIException(type(e))
        # 97 表示success
        if rest[0] != 97:
            raise APIException(rest[1])
        self.ldap_obj = conn

    def ldap_search(self, username=''):
        """
        AUTH_LDAP_BIND_DN: 域
        AUTH_LDAP_USER_SEARCH_FILTER_NAME: 搜索策略
        AUTH_LDAP_USER_ATTR_MAP: 同步账户信息到django的auth_user表中
        username: 搜索的用户
        """
        AUTH_LDAP_USER_SEARCH_FILTER = '({0}={1})'.format(self.AUTH_LDAP_USER_SEARCH_FILTER_NAME, username)
        try:
            search_id = self.ldap_obj.search(self.AUTH_LDAP_BIND_DN, ldap.SCOPE_SUBTREE, AUTH_LDAP_USER_SEARCH_FILTER, self.AUTH_LDAP_USER_ATTR_MAP)
            _, user_data = self.ldap_obj.result(search_id)
            if not user_data:
                return False, []
        except ldap.LDAPError as e:
            raise APIException(e)
        return True, user_data
