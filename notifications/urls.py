from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications_list, name='notifications_list'),
    path('read/<int:pk>/', views.read_and_redirect, name='read_and_redirect'),
    path('api/unread-count/', views.unread_count_api, name='unread_count_api'),
]