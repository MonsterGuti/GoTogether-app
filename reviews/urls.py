from django.urls import path
from . import views

urlpatterns = [
    path('ride/<int:ride_pk>/add/', views.add_review, name='add_review'),
]