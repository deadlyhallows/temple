from django.shortcuts import render
from cart.cart import Cart
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
from random import randint
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

def order_create(request):
    cart = Cart(request)
    print("A")
    if request.method == 'POST':
        print("b")
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            #cd = form.cleaned_data
            order = form.save()

            for item in cart:
                a = get_object_or_404(Product, ProductName=item['product'])
                print(type(item['product']))
                OrderItem.objects.create(order=order,
                                         product=a,
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            #launch asynchronous task
            #order_created.delay(order.id)
            return render(request, 'orders/order/created.html', {'order': order})

    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


def payment(request):
    print(request.user)
    user = request.user
    a = get_object_or_404(User, username=request.user)
    #b = Order.objects.filter(buyer_id=user.id).order_by('created').first()
    #c=get_object_or_404(OrderItem,order_id=b.id)
    #PAID_FEE_AMOUNT = c.price
    data = {}
    txnid = get_transaction_id()
    hash_ = generate_hash(request, txnid)
    hash_string = get_hash_string(request, txnid)
    # use constants file to store constant values.
    # use test URL for testing
    data["action"] = settings.PAYMENT_URL_LIVE
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
def get_hash_string(request, txnid):
    a = get_object_or_404(User, username=request.user)
    print(request.user)
    hash_string = settings.KEY + "|" + txnid + "|" + str(
        float(settings.PAID_FEE_AMOUNT)) + "|" + settings.PAID_FEE_PRODUCT_INFO + "|"
    hash_string += a.first_name + "|" + a.email + "|"
    hash_string += "||||||||||" + settings.SALT

    return hash_string


# generate a random transaction Id.
def get_transaction_id():
    hash_object = hashlib.sha256(str(randint(0, 9999)).encode("utf-8"))
    # take approprite length
    txnid = hash_object.hexdigest().lower()[0:32]
    return txnid


# no csrf token require to go to Success page.
# This page displays the success/confirmation message to user indicating the completion of transaction.
@csrf_exempt
def payment_success(request):
    data = {}
    return render(request, "orders/order/paysuccess.html", data)


# no csrf token require to go to Failure page. This page displays the message and reason of failure.
@csrf_exempt
def payment_failure(request):
    data = {}
    return render(request, "orders/order/payfail.html", data)