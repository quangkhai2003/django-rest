from django.urls import path

from app import views

app_name = 'dashboard'

urlpatterns = [
    path('hello/', views.hello_world, name='hello_world'),
    path('product/<int:id>', views.get_product_item, name='get_product_item'),
    path('products/', views.get_all_products, name='get_all_products'),
    path('add/', views.add_product_item, name='add_product_item'),
    path('add_products/', views.add_products, name='add_products'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart_items/', views.get_all_cart_items, name='get_all_cart_items'),
    path('checkout/', views.checkout, name='checkout'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
]
