from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('about/', views.about_page, name='about_page'),
    path('appointment/', views.appointment_page, name='appointment_page'),
]
