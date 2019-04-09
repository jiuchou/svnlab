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

from . import views, module_permission

urlpatterns = [
    path(r'login', views.UserLoginView.as_view()),
    path('refesh-module-permission-list', module_permission.get_module_permission_list),
    path('get-module-permission-list', module_permission.get_module_permission_list),
    path('get-module-permission-detail', module_permission.get_module_permission_detail),
    path('refresh-module-permission-list', module_permission.refresh_module_permission_detail),

    # PermissionManagement-User
    path(r'fetch-user-permission-list', views.getUserPermissionList),
    path(r'getUserPermissionList', views.getUserPermissionList),
    # PermissionManagement-Module
    path(r'getModuleSvnList', views.getModuleSvnList),
    path(r'getModuleSvnDetail', views.getModuleSvnDetail),
    path(r'refreshModulePermissionList', views.refreshModulePermissionList),
]
