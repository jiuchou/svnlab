"""
common.decorator
~~~~~~~~~~~~~~~~

This module implements the decorator function.
Usage is verify user token whether valid or invalid.

:copyright: (c) 2019 by JiuChou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.03.25
"""
import jwt
import datetime

# iss: JWT签发者
# sub: JWT所面向的用户
# aud: 接收JWT的一方
# exp: JWT的过期时间
# nbf: 定义在什么时间之前，该JWT都是不可用的
# iat: JWT的签发时间
# jti: JWT的唯一身份标识，主要用来作为一次性的token，从而回避重放攻击
def get_token(username):
    """Get user token by username
    For example:
        >>> token = jwt.encode(
            {
                'iss': "svnlab",
                'sub': "svnlab-frontend",
                'usernmae': "jiuchou",
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10),
                'iat': datetime.datetime.utcnow()
            },
            "secret_key,
            algorithm="HS256"
        )
        >>> print(token)
    """
    playload = {
        'iss': "svnlab",
        'sub': "svnlab-frontend",
        'usernmae': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10),
        'iat': datetime.datetime.utcnow()
    }
    key = "secret_key"
    token = str(jwt.encode(playload, key, algorithm="HS256"), encoding="utf-8")
    return token

def get_username(token):
    """Verity token: should be True if token is valid value.
    For example:
        >>> jwt.decode(token, "secret_key", algorithm="HS256")
    """
    try:
        decode_token = jwt.decode(token, "secret_key", algorithm="HS256")
        username = decode_token.get("username")
        return username
    except Exception as e:
        return None
