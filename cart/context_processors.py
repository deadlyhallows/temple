from .models import Carts,CartItem
from .cart import Cart
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404




def cart(request):
    user = request.user
    if user.is_authenticated:
        try:
            cart = Carts.objects.get(user_id = request.user.id)
        except Carts.DoesNotExist:
            cart  = None  
        cart_items = CartItem.objects.filter(cart=cart)
        total_items = 0
        order_total = Decimal(0.0)
        for item in cart_items:
            order_total += (item.product.Price * item.quantity)
            total_items += item.quantity

        return {
        'set':user,
        'order_total':order_total,
        'total_items':total_items,
        }

    elif not user.is_authenticated and not user.is_superuser:
            return {'set':user,
                'cart': Cart(request)}
