from django.urls import path

from app import views

app_name = 'dashboard'

urlpatterns = [
    path('hello/', views.hello_world, name='hello_world'),
    path('product/<int:id>', views.get_product_item, name='get_product_item'),
]
