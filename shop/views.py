from django.contrib.auth.decorators import login_required
from temple.decorators import user_is_shopkeeper
from django.shortcuts import render, redirect
from django.db.models import Q
from darshan.models import Temples
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from cart.forms import CartAddProductForm, CartAddProductForms
from django.contrib.auth.models import User
from django.contrib import messages
from shop.forms import ProductAddForm
from shop.models import Product
from cart.models import CartItem
from notify.signals import notify
from cart.models import Carts


# class ProductSearch(SearchView):
#     template = 'search/search.html'
#     form_name = CustomSearchForm


def allproducts(request):
    # print(request.user)
    lists = None
    k = []

    if request.method == 'POST' and 'temples' in request.POST:
        lists = request.POST.getlist('temples', None)
        # print(list)

    temple = Temples.objects.all()
    query = request.GET.get("q")
    queryset_list = Temples.objects.all()
    if query:
        queryset_list = queryset_list.filter(Q(temple2__icontains=query) |
                                             Q(City__icontains=query) |
                                             Q(Country__icontains=query) |
                                             Q(Deity__icontains=query) |
                                             Q(State__icontains=query)).distinct().order_by('temple2')
    context = {

        'k': k,
        'query_list': queryset_list,
        'list': lists,
        'b': temple,
    }
    return render(request, 'shop/allproduct.html', context)


def details1(request, pk):
    # print(val)
    user = request.user
    product = Product.objects.filter(id=pk).first()
    related_products= Product.objects.filter(Q(Temple_Name_id=product.Temple_Name_id)|Q(Product_Name=product.Product_Name)).distinct()
    cart_product_form = CartAddProductForm()
    cart_product_forms = CartAddProductForms()
    context = {'product': product,
               'loop_times': range(2, 21),
               'cart_product_form': cart_product_form,
               'cart_product_forms': cart_product_forms,
               'user': user,
               'related_products':related_products}
    return render(request, 'shop/details.html', context)


# ---------For Shopkeeper -----------------

@login_required
@user_is_shopkeeper
def seller_profile(request):
    shopkeeper = get_object_or_404(User, id=request.user.id)
    items = Product.objects.filter(seller=shopkeeper)
    context = {
        'items': items
    }
    return render(request, "shop/seller_profile.html", context)


@login_required
@user_is_shopkeeper
def product_add(request):
    user = request.user
    shopkeeper = get_object_or_404(User, id=user.id)
    item_add_form = ProductAddForm(request.POST or None, request.FILES or None)
    if item_add_form.is_valid():
        instance = item_add_form.save(commit=False)
        instance.seller = shopkeeper
        instance.save()

        return redirect('shop:seller_profile')
    else:
        messages.error(request, item_add_form.errors)
        item_add_form = ProductAddForm(request.POST)

    context = {'item_add_form': item_add_form, }

    return render(request, 'shop/item_add.html', context)


@login_required
@user_is_shopkeeper
def product_update(request, p=None):
    user = request.user
    seller = get_object_or_404(User, id=user.id)
    instance = get_object_or_404(Product, id=p)
    item_add_form = ProductAddForm(request.POST or None, request.FILES or None, instance=instance)

    if item_add_form.is_valid() == True:
        instances = item_add_form.save(commit=False)

        if instance.is_dirty():
            dirty_fields = instance.get_dirty_fields()
            # print(dirty_fields)
            for field in dirty_fields:
                if field == 'Out_of_Stock' and instance.Out_of_Stock == True:
                    us = []
                    user1 = User.objects.filter(is_superuser=False)
                    user = CartItem.objects.filter(product_id=instance.id)
                    for x in user:
                        users = get_object_or_404(Carts, id=x.cart_id)
                        c = get_object_or_404(User, id=users.user_id)
                        us.append(c)

                    if not us:
                        recipient = user1
                    else:
                        recipient = us
                    notify.send(sender=seller, target=instance, recipient_list=list(recipient), verb="Out of stock")
                    for person in recipient:
                        subject = 'Notification from Divya Kripa:Your Order'
                        verb = "Out of Stock"
                        message = render_to_string('darshan/notification_email.html', {
                            'target': instance, 'verb': verb})
                        person.email_user(subject, message)
                        # send_verification_mail(person.email, message, subject)
                if field == 'Out_of_Stock' and instance.Out_of_Stock == False:
                    us = []
                    user1 = User.objects.filter(is_superuser=False)
                    user = CartItem.objects.filter(product_id=instance.id)
                    for x in user:
                        users = get_object_or_404(Carts, id=x.cart_id)
                        c = get_object_or_404(User, id=users.user_id)
                        us.append(c)

                    if not us:
                        recipient = user1
                    else:
                        recipient = us
                    notify.send(sender=seller, target=instance, recipient_list=list(recipient), verb="Available")
                    for person in recipient:
                        subject = 'Notification from Divya Kripa:Your Order'
                        verb = "Available"
                        message = render_to_string('darshan/notification_email.html', {
                            'target': instance, 'verb': verb})
                        person.email_user(subject, message)
                        #send_verification_mail(person.email, message, subject)

        instances.save()

        # print("o")
        return redirect('shop:seller_profile')

    context = {
        'item_add_form': item_add_form,
    }

    return render(request, 'shop/item_add.html', context)


@login_required
@user_is_shopkeeper
def product_remove(request, p):
    # print("fbvbf")
    instance = get_object_or_404(Product, id=p)
    # print(instance)
    instance.delete()

    return redirect('shop:seller_profile')


def error400(request):
    return render(request, 'shop/error/HTTP400.html')


def error403(request):
    return render(request, 'shop/error/HTTP403.html')


def error404(request):
    return render(request, 'shop/error/HTTP404.html')


def error500(request):
    return render(request, 'shop/error/HTTP500.html')


def error200(request):
    return render(request, 'shop/error/HTTP500.html')
