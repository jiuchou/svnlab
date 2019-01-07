from django.urls import path, include

from backend.role import views

urlpatterns = [
    path(r'getPermissionList', views.getPermissionList),
]
