from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from darshan.forms import SignUpForm, MobileForm
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm, CartAddProductForms
from django.contrib.auth import get_user
from decimal import Decimal
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from .models import Carts, CartItem
from shop.models import Product
from django.contrib.auth.decorators import login_required


#----------------For Logged In User---------------

@login_required
def get_user_cart(request):
    """Retrieves the shopping cart for the current user."""
    # If the user is logged in, then grab the user's cart info.
    cart_id = None
    cart = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        try:
            cart = Carts.objects.get(user=request.user)
        except Carts.DoesNotExist:
            cart = Carts(user=request.user)
            cart.save()
    else:
        cart_id = request.session.get('cart_id')
        if not cart_id:
            cart = Carts()
            cart.save()
            request.session['cart_id'] = cart.id
        else:
            cart = Carts.objects.get(id=cart_id)
    return cart

@login_required
def get_cart_count(request):
    print(request.user)
    cart = get_user_cart(request)
    print(cart)
    total_count = 0
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        total_count += item.quantity
    return total_count

@login_required
def update_cart_info(request):
    request.session['cart_count'] = get_cart_count(request)


@login_required
def view_cart(request):
    quantity=0
    cart_total_price = None
    user = request.user
    print(user)
    cart_form = CartAddProductForm()#to update the quantity
    cart = get_object_or_404(Carts, user_id=user.id)
    print(cart)
    cart_items = CartItem.objects.filter(cart_id=cart.id)
    order_total = Decimal(0.0)
    print("S")
    for item in cart_items:# getting the total price of the cart
        order_total += (item.product.Price * item.quantity)
        quantity+=item.quantity
        item_cart = Product.objects.filter(id=item.product_id)
        for x in item_cart:
            cart_total_price = item.quantity * x.Price

    context = {    'loop_times': range(1, 21),
                   'quantity':quantity,
                   'user':user,
                   'cart': cart_items,
                   'cart_form':cart_form,
                   'total':cart_total_price,
                   'form': AuthenticationForm,
                   'Mobile_form': MobileForm,
                   'user_form': SignUpForm,
                   }
    return render(request, 'cart/detail.html', context)


@login_required
def add_to_cart(request, product_id):


    form = CartAddProductForm(request.POST)
    print("a")
    if form.is_valid():
        print("b")
        cd = form.cleaned_data
        cart = get_user_cart(request)
        product = Product.objects.get(id=product_id)
        quantity = str(cd['quantity'], )
        # update_quantity = cd['update']
        cart_item = CartItem(product=product, cart=cart, quantity=quantity)

        cart_item.save()



    print(get_cart_count(request))
    return redirect('cart:view_cart')

@login_required
def update_quantity(request,product_id):
    if request.method == 'POST' and 'quantity' in request.POST:
        get_updated_quantity = request.POST.get('quantity', None)
        updated_item = get_object_or_404(CartItem, product_id=product_id)
        updated_item.quantity = get_updated_quantity
        updated_item.save()

    return redirect('cart:view_cart')

@login_required
def remove_from_cart(request, product_id):
    print(product_id)

    cart_item = get_object_or_404(CartItem, id=product_id)
    quantity = cart_item.quantity
    cart_item.delete()
    if request.session.get('cart_count'):
        request.session['cart_count'] -= quantity
    else:
        request.session['cart_count'] = 0
    update_cart_info(request)
    return redirect('cart:view_cart')

#---------For Anonymous User's cart------------------

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    print("a")
    form = CartAddProductForms(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')
    
    

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id =product_id)
    cart.remove(product)

    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    
    context = {'loop_times': range(2, 21),
               'cart': cart,

               'form': AuthenticationForm,
               'Mobile_form': MobileForm,
               'user_form': SignUpForm,

    }

    return render(request, 'cart/ses_cart_detail.html', context)






