from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from app.models import ProductItem
from django.shortcuts import get_object_or_404, render

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello, World!")

def get_product_item(request, id):
    product = get_object_or_404(ProductItem, id=id)
    data = {
        'title': product.title,
        'quantity': product.quantity,
        'price': str(product.price),  # Convert DecimalField to string
    }
    return JsonResponse(data)

def add_product_item(request):
    new_product = ProductItem(title='guitar', quantity=1 , price=19)
    new_product.save()
    return HttpResponse("added data")
    