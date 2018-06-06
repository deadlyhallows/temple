from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from darshan.forms import SignUpForm, MobileForm
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    print("a")
    if form.is_valid():
        print("b")
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id =product_id)
    cart.remove(product)

    return redirect('cart:cart_detail')

def cart_detail(request):
    print(request)
    cart = Cart(request)
    print("c")
    for item in cart:
        print(type(item))
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity':str(item['quantity']),
                                                                   'update':True})
        item['update_quantity_form'] = str(item['update_quantity_form'])

    context = {'loop_times': range(2, 21),
               'cart': cart,
               'form': AuthenticationForm,
               'Mobile_form': MobileForm,
               'user_form': SignUpForm,

    }

    return render(request, 'cart/detail.html', context)






# Create your views here.
