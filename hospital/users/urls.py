from django.contrib import admin
from django.urls import path,include
from .import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.user_signup,name='signup'),
    path('login/', views.user_login,name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.user_home,name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
