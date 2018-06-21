from django.contrib.auth.decorators import login_required
from temple.decorators import user_is_shopkeeper
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from darshan.models import Temples
from shop.models import Product, ProductSelected
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from shop.forms import CustomSearchForm
from cart.forms import CartAddProductForm
from darshan.tokens import account_activation_token
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import AuthenticationForm
import smtplib
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.core import serializers
from django.views.generic import View
from django.template.loader import get_template
from django.template import Context
from operator import attrgetter
from haystack.query import SearchQuerySet
import copy
from shop.forms import ProductAddForm
from shop.models import Shopkeeper, Product
from cart.models import CartItem
from haystack.generic_views import SearchView
from notify.signals import notify
from darshan.views import send_verification_mail


class ProductSearch(SearchView):
    template = 'search/search.html'
    form_name = CustomSearchForm


def allproducts(request):
    print(request.user)
    lists = None

    k = []

    if request.method == 'POST' and 'temples' in request.POST:
        lists = request.POST.getlist('temples', None)
        print(list)

    temple = Temples.objects.all()
    query = request.GET.get("q")
    queryset_list=Temples.objects.all()
    if query:
      queryset_list = queryset_list.filter(Q(temple2__icontains=query)|
                                           Q(City__icontains=query)|
                                           Q(Country__icontains=query)|
                                           Q(Deity__icontains=query)|
                                           Q(State__icontains=query)).distinct().order_by('temple2')
    context = {

        'k': k,
        'query_list': queryset_list,
        'list':lists,
        'b':temple,
    }
    return render(request, 'shop/allproduct.html', context)

def details1(request,val):
    print(val)
    user = request.user
    product = Product.objects.filter(Product_Name=val)
    cart_product_form = CartAddProductForm()
    context = {'product': product,
               'cart_product_form': cart_product_form,
               'user':user}
    return render(request, 'shop/details.html', context)


#---------For Shopkeeper -----------------    

@login_required
@user_is_shopkeeper
def seller_profile(request):
  shopkeeper = get_object_or_404(Shopkeeper,user=request.user)
  items = Product.objects.filter(seller=shopkeeper)
  context = {
    'items': items
  }
  return render(request,"shop/seller_profile.html", context)       


@login_required
@user_is_shopkeeper
def product_add(request):
    shopkeeper= get_object_or_404(Shopkeeper,user=request.user)
    item_add_form = ProductAddForm(request.POST or None, request.FILES or None)
    if item_add_form.is_valid():
        instance = item_add_form.save(commit=False)
        instance.seller=shopkeeper
        instance.save()
        
        return redirect('shop:seller_profile')
    else:
        item_add_form = ProductAddForm()

    context = {'item_add_form':item_add_form, }            

    return render(request,'shop/item_add.html', context ) 

@login_required
@user_is_shopkeeper
def product_update(request,p=None):
    seller = get_object_or_404(Shopkeeper,user=request.user)
    instance = get_object_or_404(Product,id=p)
    item_add_form = ProductAddForm(request.POST or None,request.FILES or None, instance=instance)
    
    if item_add_form.is_valid() == True:
        instances = item_add_form.save(commit=False)
        instances.save()
        us = []
        tm = Product().is_dirty()
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
        if tm:
            dirty_fields = Product().get_dirty_fields()
            print(dirty_fields)
            for field in dirty_fields:
                if field=='OutofStock' and instance.OutofStock==True:
                   notify.send(sender=seller, target=instance, recipient_list=list(recipient), verb="Out of stock")
                   for person in recipient:
                      subject = 'Notification'
                      verb="Out of Stock"
                      message = render_to_string('darshan/notification_email.html', {
                      'target':instance,'verb':verb })
                      person.email_user(subject, message)
                      send_verification_mail(person.email, message, subject)
                if field=='OutofStock' and instance.OutofStock==False:
                   notify.send(sender=seller, target=instance, recipient_list=list(recipient), verb="Available")
                   for person in recipient:
                      subject = 'Notification'
                      verb="Available"
                      message = render_to_string('darshan/notification_email.html', {
                      'target':instance,'verb':verb })
                      person.email_user(subject, message)
                      send_verification_mail(person.email, message, subject)

        print("o")
        return redirect('shop:seller_profile')
            
          
    context = {
                'item_add_form':item_add_form,
    }

    return render(request,'shop/item_add.html', context)

@login_required
@user_is_shopkeeper
def product_remove(request,p):

    instance = get_object_or_404(Product,id=p)
    instance.delete()

    return redirect('shop:seller_profile')     
