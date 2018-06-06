from django.shortcuts import render
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem
from shop.models import Product
from django.shortcuts import get_object_or_404
#from .tasks import order_created
from payu_biz.views import make_transaction

def payment(request):
    """ DO your stuffs here and create a dictionary (key,value pair), Payment gate calling with provided data dict """
    cleaned_data = {
    'txnid': "aaaaassss", 'amount': 450000, 'productinfo': "sample_produ",
    'firstname':"renjith", 'email': "renjithsraj@live.com", 'udf1': '',
    'udf2': '', 'udf3': '', 'udf4': '', 'udf5': '', 'udf6': '', 'udf7': '',
    'udf8': '', 'udf9': '', 'udf10': '','phone':"9746272610"
    }

    return make_transaction(cleaned_data)

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