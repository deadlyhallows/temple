from django.shortcuts import render, redirect
from cart.models import Carts, CartItem
from .forms import OrderCreateForm
from .models import OrderItem, Order
from shop.models import Product
from django.shortcuts import get_object_or_404
#from .tasks import order_created
from payu_biz.views import make_transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import hashlib
from django.conf import settings
import logging, traceback
import orders.constants as constants
from django.core.urlresolvers import reverse
import hashlib
import requests
from .admin import OrderAdmin
from random import randint
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.views.decorators.csrf import csrf_exempt
from notify.signals import notify

@login_required
def order_create(request):

    total_cost=Decimal(0.0)
    total_items=0
    user = get_user(request)
    print(user)

    #c = Carts.objects.get(user_id=user.id)
    c = get_object_or_404(Carts, user_id=user.id)
    #print(c)
    items = CartItem.objects.filter(cart_id=c.id)
    print("A")
    for item in items:
        #print(item)
        total_items += item.quantity
        a = get_object_or_404(Product, id=item.product_id)
        #print(a)
        total_cost += (item.quantity * a.Price)
    if request.method == 'POST':
        print("b")
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            print("c")
            #cd = form.cleaned_data
            order = form.save(commit=False)
            order.buyer_id = get_user(request).id
            #order.paid=True
            order.save()
            print("d")
            for item in items:
                total_items+=item.quantity
                a = get_object_or_404(Product, id=item.product_id)
                total_cost += (item.quantity * a.Price)
                OrderItem.objects.create(order=order,
                                         product=a,
                                         price=a.Price,
                                         quantity=item.quantity)
                #item.delete()

            #launch asynchronous task
            #order_created.delay(order.id)
            return render(request, 'orders/order/created.html', {'order': order})

    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'total_cost':total_cost,'form': form,'items':items})

@login_required
def payment(request):
    print(request.user)
    user = request.user
    a = get_object_or_404(User, username=user)
    #b = Order.objects.filter(buyer_id=user.id).order_by('created').first()
    #c=get_object_or_404(OrderItem,order_id=b.id)
    #PAID_FEE_AMOUNT = c.price
    data = {}
    txnid = get_transaction_id(request)
    hash_ = generate_hash(request, txnid)
    hash_string = get_hash_string(request, txnid)
    # use constants file to store constant values.
    # use test URL for testing
    data["action"] = settings.PAYMENT_URL_LIVE #LIVE for production
    data["amount"] = float(settings.PAID_FEE_AMOUNT)
    data["productinfo"] = settings.PAID_FEE_PRODUCT_INFO
    data["key"] = settings.KEY
    data["txnid"] = txnid
    data["hash"] = hash_
    data["hash_string"] = hash_string
    data["firstname"] = a.first_name
    data["email"] = a.email
    data["phone"] = a.mobile.Mobile_No
    data["service_provider"] = settings.SERVICE_PROVIDER
    data["furl"] = request.build_absolute_uri(reverse("orders:payment_failure"))
    data["surl"] = request.build_absolute_uri(reverse("orders:payment_success"))
    return render(request, "orders/order/success.html", data)


# generate the hash
@login_required
def generate_hash(request, txnid):
    try:
        # get keys and SALT from dashboard once account is created.
        #hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string = get_hash_string(request, txnid)
        generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        return generated_hash
    except Exception as e:
        # log the error here.
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


# create hash string using all the fields
@login_required
def get_hash_string(request, txnid):
    a = get_object_or_404(User, username=request.user)
    print(request.user)
    hash_string = settings.KEY + "|" + txnid + "|" + str(
        float(settings.PAID_FEE_AMOUNT)) + "|" + settings.PAID_FEE_PRODUCT_INFO + "|"
    hash_string += a.first_name + "|" + a.email + "|"
    hash_string += "||||||||||" + settings.SALT

    return hash_string


# generate a random transaction Id.
@login_required
def get_transaction_id(request):
    hash_object = hashlib.sha256(str(randint(0, 9999)).encode("utf-8"))
    # take approprite length
    txnid = hash_object.hexdigest().lower()[0:32]
    return txnid


# no csrf token require to go to Success page.
# This page displays the success/confirmation message to user indicating the completion of transaction.
@login_required
@csrf_exempt
def payment_success(request):
    user = request.user
    p = get_object_or_404(Order, buyer_id=user.id)
    p.paid=True
    p.save()
    c1 = get_object_or_404(Carts, user_id=user.id)
    items1 = CartItem.objects.filter(cart_id=c1.id)
    for item in items1:
        item.delete()
    #important:when paid is seen in database table mark is_accepted as True for for the product to notify
    #order_delivered(OrderAdmin,request, obj, form, change )
    data = {}
    return render(request, "orders/order/paysuccess.html", data)


# no csrf token require to go to Failure page. This page displays the message and reason of failure.
@login_required
@csrf_exempt
def payment_failure(request):
    print(request.user)
    data = {}
    return render(request, "orders/order/payfail.html", data)

def order_delivered(self, request, obj, form, change):
    if Order().is_dirty():
        user = User.objects.filter(id=obj.buyer_id)
        notify.send(sender=self, target=obj, recipient_list=list(user), verb="accepted")
    obj.save()