from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('posts/', views.PostListCreate.as_view()),
    path('posts/<int:pk>/', views.PostRUD.as_view()),
    path('posts/<int:post_id>/comments/', views.CommentListCreate.as_view()),
    path('posts/<int:post_id>/comments/<int:pk>/', views.CommentRUD.as_view()),
    path('posts/<int:post_id>/grade/', views.GradePost.as_view()),
]
