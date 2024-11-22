from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('subscribe/', views.subscribe, name='subscribe'), 
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
]