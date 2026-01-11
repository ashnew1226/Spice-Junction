from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_page, name='menu'),
    path('ajax/foods/<int:category_id>/', views.foods_by_category, name='foods_by_category'),
    path('ajax/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('add-review/', views.add_review, name='add_review'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register_user, name='register'),

]
