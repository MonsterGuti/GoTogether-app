from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('create/', views.create_ride, name='create_ride'),
    path('ride/<int:pk>/', views.ride_detail, name='ride_detail'),
    path('ride/<int:pk>/book/', views.book_ride, name='book_ride'),
    path('ride/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('ride/<int:pk>/send-message/', views.send_message_ajax, name='send_message_ajax'),
    path('ride/<int:pk>/messages/fetch/', views.get_messages_ajax, name='get_messages_ajax'),

    path('booking/<int:booking_id>/approve/', views.approve_booking, name='approve_booking'),
    path('booking/<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),
    path('booking/<int:booking_id>/remove/', views.remove_passenger, name='remove_passenger'),

    path('my-rides/', views.my_rides, name='my_rides'),
    path('ride/<int:pk>/delete/', views.delete_ride, name='delete_ride'),
    path('ride/<int:pk>/edit/', views.edit_ride, name='edit_ride'),
    path('api/geocode/', views.proxy_geocode, name='proxy_geocode'),
]
