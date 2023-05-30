from django.urls import path, re_path
from . import views

from .views import ProductDetailView, CategoryDetailView, ShopDetailView, AddToCartView, AccountView
from .views import AboutCompony, Delivery, AddressCompony

urlpatterns = [
    # index
    path('', views.info_shop, name='shop'),
    path('product/<str:ct_model>/<str:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    # path('logout-then-login/', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),
    # главная страница
    path('mainpage/', views.info_shop, name='info_shop'),
    path('account/', AccountView.as_view(), name='account'),
    # path('account/', views.account, name='account'),
    path('logout/', views.custom_logout, name='logout'),
    path('product/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    # path('product/oil/', views.oils, name='oils'),
    path('product/', ShopDetailView.as_view(), name='product'),
    path('cart/', views.cart_detail, name='cart_detail'),
    re_path(r'^cart/add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    re_path(r'^cart/remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
    re_path(r'^create/$', views.order_create, name='order_create'),
    # path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('about-compony/', AboutCompony.as_view(), name='about_compony'),
    path('delivery/', Delivery.as_view(), name='delivery'),
    path('address/', AddressCompony.as_view(), name='address_compony')
    # path('success/', views.success, name='success'),
]