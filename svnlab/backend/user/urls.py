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

from . import views

urlpatterns = [
    path(r'login', views.UserLoginView.as_view()),
    # PermissionManagement-User
    path(r'fetch-user-permission-list', views.getUserPermissionList),
    path(r'getUserPermissionList', views.getUserPermissionList),
    # PermissionManagement-Module
    path(r'getModuleSvnList', views.getModuleSvnList),
    path(r'getModuleSvnDetail', views.getModuleSvnDetail),
    path(r'refreshModulePermissionList', views.refreshModulePermissionList),
]
