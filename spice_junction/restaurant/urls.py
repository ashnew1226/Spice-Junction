from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_page, name='menu'),
    path('ajax/foods/<int:category_id>/', views.foods_by_category, name='foods_by_category'),
    path('ajax/add-to-cart/', views.ajax_add_to_cart, name='add_to_cart'),
    path('add-review/', views.add_review, name='add_review'),
    path('logout/', views.custom_logout, name='logout'),
    path('cart-detail/', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('ajax/remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('ajax/update-cart/', views.update_cart_quantity, name='update_cart'),
    path('my-orders/', views.my_orders, name='my_orders'),

]
