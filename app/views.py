from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from app.models import ProductItem, CartItem
from django.shortcuts import get_object_or_404, render
import json
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

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

def get_all_products(request):
    try:
        # Retrieve all products from the database
        products = ProductItem.objects.all()

        # Convert products queryset to JSON format
        product_list = list(products.values())

        return JsonResponse({'success': True, 'products': product_list})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def add_product_item(request):
    new_product = ProductItem(id=1, title='guitar', quantity=1 , price=19)
    new_product.save()
    return HttpResponse("added data")

@csrf_exempt    
def add_products(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("here is data: ", data)
            
            if not isinstance(data, list):
                raise ValueError('JSON data must be a list')

            for item in data:
                title = item.get('title')
                quantity = item.get('quantity')
                price = item.get('price')

                # Create a new Product instance
                product = ProductItem.objects.create(title=title, quantity=quantity, price=price)

            return JsonResponse({'success': True, 'message': 'Products added successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed'}, status=405)
    
@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)  # Default quantity is 1

            # Check if the product exists
            product = ProductItem.objects.get(pk=product_id)

            # Add item to cart
            cart_item, created = CartItem.objects.get_or_create(
                product=product,
                defaults={'quantity': quantity}
            )

            if not created:
                # If the item already exists in the cart, update the quantity
                cart_item.quantity += quantity
                cart_item.save()

            return JsonResponse({'success': True, 'message': 'Item added to cart successfully'})
        except ProductItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed'}, status=405)
    
def get_all_cart_items(request):
    try:
        # Retrieve all cart items from the database
        cart_items = CartItem.objects.all()

        # Convert cart items queryset to JSON format
        cart_items_list = list(cart_items.values())

        return JsonResponse({'success': True, 'cart_items': cart_items_list})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        try:
            # Get the user's cart items
            cart_items = CartItem.objects.all()  # You might want to filter by user if you have user-specific carts

            # Calculate total quantity and total revenue
            total_quantity = sum(item.quantity for item in cart_items)
            total_revenue = sum(item.product.price * item.quantity for item in cart_items)

            # Clear the user's cart after checkout
            cart_items.delete()

            return JsonResponse({'totalQuantity': total_quantity, 'totalRevenue': total_revenue})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed'}, status=405)
    
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    # print(request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'success': True,'token': token.key, 'user': serializer.data, 'isAdmin': user.is_superuser})