from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='glavnaya_str'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
]