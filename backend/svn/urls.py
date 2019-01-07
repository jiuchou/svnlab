from django.urls import path

from backend.svn import views

urlpatterns = [
    path('getSVNPathList', views.getSVNPathList),
    path('getSVNPathDetail', views.getSVNPathDetail),
]
