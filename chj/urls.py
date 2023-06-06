from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('chatt/', views.chatt, name='chatt'),
    # path('delte/<int:id>', views.delte, name='delte'),
    path('user_signin/', views.user_signin, name='user_signin'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
]