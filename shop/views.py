from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from darshan.models import Temples
from shop.models import Product
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

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

# Create your views here.
def allproducts(request):
    global z
    c = []
    if request.POST:
        list = request.POST.getlist('temples', None)
        print(list)
        for i in list:
            c.append(i)

    print(c)
    b = Temples.objects.all()
    query = request.GET.get("q")
    queryset_list=Temples.objects.all()
    if query:
      queryset_list = queryset_list.filter(Q(temple2__icontains=query)|
                                           Q(City__icontains=query)|
                                           Q(Country__icontains=query)|
                                           Q(Deity__icontains=query)|
                                           Q(State__icontains=query)).distinct().order_by('temple2')



    context = {

        'query_list':queryset_list,
        'c':c,
        'b':b,

    }
    return render(request, 'shop/allproduct.html', context)

def detail(request,val):
    a = get_object_or_404(Product,ProductName = val )
    context = {'a':a}
    return render(request, 'shop/details.html' ,context)