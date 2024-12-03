from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_tweet, name='show_tweet'),
    path('create', views.tweet_create, name='tweet_create'),
    path('edit/<int:tweet_id>/', views.tweet_edit, name='tweet_edit'),
    path('delete/<int:tweet_id>/', views.tweet_delete, name='tweet_delete'),

    path('auth/register', views.register_User, name='register_User'),
    path('search/', views.search, name='search'),
]