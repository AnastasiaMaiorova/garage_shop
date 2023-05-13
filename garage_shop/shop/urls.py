from django.urls import path
from . import views

from .views import ProductDetailView

urlpatterns = [
    path('', views.index, name='shop'),
    path('product/<str:ct_model>/<str:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    # главная страница
    path('mainpage', views.info_shop, name='info_shop'),

]