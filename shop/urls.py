from django.urls import path
from . import views_shop

urlpatterns = [
    path('', views_shop.shop_home, name='shop_home'),
    path('about/', views_shop.about, name='shop_about'),
    path('contact/', views_shop.contact, name='shop_contact'),
    path('products/', views_shop.product, name='shop_products'),
    path('search/', views_shop.search, name='shop_search'),
    path('track_order/', views_shop.track_order, name='shop_track_order'),
    path('cart/', views_shop.cart, name='shop_cart'),
    path('checkout/', views_shop.checkout, name='shop_checkout'),
    path('add-multiple-to-cart/', views_shop.add_multiple_to_cart, name='shop_add_multiple_to_cart'),
]
