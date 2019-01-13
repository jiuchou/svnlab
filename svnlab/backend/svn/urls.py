'''
user.urls
~~~~~~~~~

This module implements the Requests Urls.
Requests is an HTTP library, written in Python, for user beings. Basic GET and POST.

:copyright: (c) 2019 by JiuChou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.01.13
'''

from django.urls import path

import svnOperation
import views

urlpatterns = [
    path(r'getSVNPathList', svnOperation.getSVNPathList),
    path(r'getSVNPathDetail', svnOperation.getSVNPathDetail),

    path(r'changeRoleByUser', views.changeRoleByUser),
]
