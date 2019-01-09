from django.urls import path, include

from backend.report import views

urlpatterns = [
    path(r'changeRoleByUser', views.changeRoleByUser),
]
