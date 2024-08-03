from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_post_list, name='blog_post_list'),
    path('post/<int:pk>/', views.blog_post_detail, name='blog_post_detail'),
    path('create/', views.create_blog_post, name='create_blog_post'),
    path('edit/<int:pk>/', views.edit_blog_post, name='edit_blog_post'),
    path('post/<int:pk>/delete/confirm/', views.delete_blog_post_confirm, name='delete_blog_post_confirm'),
    path('post/<int:pk>/delete/', views.delete_blog_post, name='delete_blog_post'),  # E
]