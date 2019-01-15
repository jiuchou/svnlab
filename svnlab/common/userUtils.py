"""
common.user
~~~~~~~~~

This module implements the user info.
user is an simple library, written in Python, for user beings.

:copyright: (c) 2019 by JiuChou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.01.14
"""

# built-in library
import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def userLogon(username, ldapUserInfo):
    """
    docstring
    1. 获取用户基础信息
    2. 解析用户权限, 存放至数据库
    """
    response = {}
    # ldapUserInfo = json.dumps(str(ldapUserInfo[0][1]["objectClass"]))
    ldapUserInfo = json.dumps(str(ldapUserInfo[0][0]), ensure_ascii=False)
    truename = ldapUserInfo.split(",")[0].split("=")[1]
    response = {
        "username": username,
        "roles": "guster",
        "truename": truename,
        "sex": "",
        "email": "",
        "telephone": "",
        "introduction": "",
        "profile_photos": "",
        "join_time": "",
        "login_time": ""
    }

    # ParaseRoleToDB
    result = os.system("chmod +x {0}/common/roleUtils/*.sh; {0}/common/roleUtils/getUserRole.sh {1};".format(ROOT_DIR, username))
    if result == 0:
        print("Success: Parase {0}'s role to database success!".format(username))
    else:
        print("Error: Parase {0}'s role to database failed!".format(username))

    return response
