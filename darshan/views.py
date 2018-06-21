from django.contrib.auth.decorators import login_required
from temple.decorators import user_is_temple_manager
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from darshan.models import Picture, Profile, Temples, Mobile, Darshans, OnlineDonation, TempleManager
from shop.models import Shopkeeper
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from darshan.forms import SignUpForm, TempleForm, MobileForm, DonationForm, TempleManagerForm, TempleAddForm, PictureAddForm, DarshanAddForm
from darshan.tokens import account_activation_token
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import AuthenticationForm
import smtplib
from django.contrib import messages
from django.conf import settings
from django.shortcuts import get_object_or_404
from cart.cart import Cart
from shop.models import Product
from cart.models import CartItem, Carts
from django.utils.timezone import now, localtime
import datetime
import time
from django.db.models import F
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from django.template import RequestContext
from notify.signals import notify


def home(request):

    temples=Temples.objects.all()
    paginator = Paginator(temples, 4)
    page_change_var = 'page'  # change=request
    page = request.GET.get(page_change_var)
    print(type(page))
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {'temples': temples,
               'form': AuthenticationForm,
               'Mobile_form': MobileForm,
               'user_form': SignUpForm,
               'manager_form':TempleManagerForm,
               'object_list': queryset,
               'page_change_var': page_change_var
             }
    return render(request, 'darshan/home.html', context)

def allDarshan(request):
    temples = Temples.objects.all()
    paginator = Paginator(temples, 4)
    page_change_var = 'page'  # change=request
    page = request.GET.get(page_change_var)
    print(type(page))
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {'temples': temples,
               'object_list': queryset,
               'page_change_var': page_change_var
               }
    return render(request, 'darshan/alldarshan.html', context)


#------------For Users -------------
def signup(request):
    print("D")

    if request.method == 'POST' and 'usertype' in request.POST:
        print("p")
        user_form = SignUpForm(request.POST)
        mobile_form = MobileForm(request.POST)
        print("o")
        typeuser = request.POST.get('usertype',None)
        print(typeuser)
        if user_form.is_valid() and mobile_form.is_valid():
            print("asd")
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()

            user.mobile.Mobile_No = mobile_form.cleaned_data.get('Mobile_No')
            user.mobile.save()
            if typeuser=='seller':
                username = user_form.cleaned_data.get('username')
                users = get_object_or_404(User,username=username)
                seller = Shopkeeper.objects.create(user=users,is_shopkeeper=True)
                seller.save()
            if typeuser=='user':    
                create_cart=Carts.objects.create(active=True,user_id=user.id)
                create_cart.save()
                cart = Cart(request)
                print(cart)
                if cart is not None:#create cart for the logged in user
                    print("A")
                    user_cart = get_object_or_404(Carts, user_id=user.id)
                    print("b")
                    for item in cart:
                        print("c")
                        cart_product = get_object_or_404(Product, ProductName=item['product'])
                        print("d")
                        cart_item = CartItem.objects.create(quantity=item['quantity'],
                                                        active=True, cart_id=user_cart.id, product_id=cart_product.id)
                        print("E")
                        cart_item.save()
                        print("f")
                        #send_mail(subject,message,from_email,to_list,fail_silently=True)
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('darshan/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            send_verification_mail(user.email, message, subject)
            return render(request, 'darshan/account_activation_sent.html')
    else:
        print("abc")
        user_form = SignUpForm()
        mobile_form = MobileForm()
        

    context = {
        "user_form":user_form,
        "Mobile_form":mobile_form,
        

    }
    return render(request, 'darshan/home.html', context)



def account_activation_sent(request):
    return render(request, 'darshan/account_activation_sent.html')


def activate(request, uidb64, token,):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.mobile.email_confirmed = True
        user.mobile.save()
        user.save()
        login(request, user, backend='django.core.mail.backends.console.EmailBackend')
        return render(request,'darshan/home.html')
    else:
        return render(request, 'darshan/account_activation_invalid.html')

#Do change this when in production
email_address = 'amishaameyanish@gmail.com'
email_password = 'deployment123456789'

def send_verification_mail(email, msg,sub):
    print("send verification mail")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, email, msg,sub)
        server.close()
        print('successfully sent the mail')

    except:
        print("failed to send mail")


@login_required
def Usertype(request):
    temple_manager = TempleManager.objects.filter(user=request.user)
    shopkeeper = Shopkeeper.objects.filter(user=request.user)
    if temple_manager:
        return redirect('darshan:manager_profile')
    if shopkeeper:
        return redirect('shop:seller_profile')
    else:
        return redirect('darshan:user_profile')



@login_required
def user_profile(request):
    b=[]
    user=request.user
    profile=Profile.objects.get(user_id=user.id)
    print(profile.Select_Temple)
    cart = Cart(request)
    if cart is not None:
        user_cart = get_object_or_404(Carts, user_id=user.id)
        for item in cart:

            cart_product = get_object_or_404(Product, ProductName=item['product'])
            cart_item = CartItem.objects.create(quantity=item['quantity'],
                                                active=True, cart_id=user_cart.id, product_id=cart_product.id)
            cart_item.save()
    print(cart)
    if request.method=="POST" and "Select_Temple" in request.POST:
        print("b")
        #print(profile.Temple1)
        selected_temple=profile.Select_Temple

        form = TempleForm(request.POST,instance=profile)
        print("c")
        if form.is_valid():
            #print(profile.Temple1)
            profile=form.save(commit=False)
            for temple in selected_temple:
                print(temple)
                profile.Select_Temple.append(temple)
            #print(profile.Temple1)
            profile.save()

            return redirect('darshan:user_profile')
        else:
            messages.error(request, "not created at all")
    else:
        form = TempleForm()
    print("e")
    query_list=Profile.objects.filter(user_id=user.id)
    get_user = User.objects.get(id=user.id)
    user_mobile = Mobile.objects.get(id=user.id)
    if request.POST:
        for t in query_list:
            print(t)
            for x in t.Select_Temple:
                city_pk_list = request.POST.getlist(x, None)
                for z in city_pk_list:
                    pic = Picture.objects.get(id=z)
                    profile.selected.append(pic.id)
                    profile.save()
    for n in query_list:
        for m in n.Select_Temple:
            b.append(m)
    paginator = Paginator(b, 5)
    page_change_var = 'page'  # change=request
    page = request.GET.get(page_change_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context={'set': user,
             "object_list": queryset,
            'query_list':query_list,
            'form':form,
             'u':get_user,
             'v':user_mobile,
             'page_change_var': page_change_var
                 }
    return render(request, 'darshan/user_profile.html', context)

@login_required
def accounts(request):
    #set = Profile.objects.all()
    user=request.user
    profile=Profile.objects.filter(user_id=user.id)
    for i in profile:
        print(i)
        for j in i.Select_Temple:
            print(j)
            temple = Temples.objects.filter(temple2=j)
            print(temple)
    context={'set':user,
        'pro':profile}
    return render(request,'darshan/accounts.html', context)

@login_required
def delete(request, value):
    print("a")
    user=request.user
    print(user)
    query_l = Profile.objects.get(user_id=user.id)
    print("b")
    for i in query_l.Select_Temple:
        if i==value:
            query_l.Select_Temple.remove(i)
            query_l.save()
    temple=Temples.objects.get(temple2=value)
    img=Picture.objects.filter(Temple_id=temple.id)
    for j in img:
        for k in query_l.selected:
            if k==j.id:
                query_l.selected.remove(k)
                query_l.save()

    return redirect('darshan:user_profile')

@login_required
def details(request, temp):
    #m = localtime().time()
    #FMT = '%H:%M:%S'
    #user = request.user
    #pro = Profile.objects.get(user_id=user.id)
    user=request.user
    temple=get_object_or_404(Temples,temple2 = temp)
    darshan = Darshans.objects.filter(temple_id=temple.id)
    #b = Picture.objects.filter(Temple_id=q.id)
    context={
        'set':user,
        's':darshan,
        'q':temple,
        }
    return render(request, 'darshan/details.html', context)

def detail(request, temp1):
    #m = localtime().time()
    #FMT = '%H:%M:%S'
    temple = get_object_or_404(Temples,temple2 = temp1)
    darshan = Darshans.objects.filter(temple_id=temple.id)
    context={
        's':darshan,
        'q':temple,
        }
    return render(request, 'darshan/detail.html', context)

def Online_Donation(request, v):
    if request.method == "POST":
        temple = get_object_or_404(Temples,temple2 = v)
        form = DonationForm(request.POST)
        print("Aw")
        if form.is_valid():
            print("Ab")
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.temple = temple
            donation.Amount = form.cleaned_data.get('Amount')
            donation.Purpose = form.cleaned_data.get('Purpose')
            donation.status=True
            donation.save()
            return redirect('orders:payment')
    else:
        form = DonationForm()

    context = {'form':form,}
    return render(request,'darshan/Online_Donation.html', context)


#--------------For Temple-Managers---------------------
 
def signup1(request): 
    print("D")
    if request.method == 'POST':
        print("p")
        user_form = SignUpForm(request.POST)
        mobile_form = MobileForm(request.POST)
        manager_form =TempleManagerForm(request.POST)
        print("o")

        if user_form.is_valid() and mobile_form.is_valid() and manager_form.is_valid():
            print("asd")
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()

            user.mobile.Mobile_No = mobile_form.cleaned_data.get('Mobile_No')
            user.mobile.save()

            users = user_form.cleaned_data.get('username')
            get_user = get_object_or_404(User,username=users)
            Temple_name = manager_form.cleaned_data.get('Temple_Name')
            tempman = TempleManager.objects.create(user=get_user, is_manager=True, Temple_Name=Temple_name)
            tempman.save()
          
            #send_mail(subject,message,from_email,to_list,fail_silently=True)
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('darshan/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            send_verification_mail(user.email, message, subject)
            return render(request, 'darshan/account_activation_sent.html')
    else:
        print("abc")
        user_form = SignUpForm()
        mobile_form = MobileForm()
        manager_form = TempleManagerForm()

    context = {
        "user_form":user_form,
        "Mobile_form":mobile_form,
        "manager_form":manager_form,

    }
    return render(request, 'darshan/home.html', context)

@login_required
@user_is_temple_manager
def manager_profile(request):
    #t = get_object_or_404(TempleManager, user=request.user)
    darshan =Darshans.objects.all()
    picture = Picture.objects.filter(user=request.user)
    temples = Temples.objects.filter(user=request.user)
    context={
     'temples':temples,
     'pictures':picture,
     'darshans':darshan
    }
    return render(request,'darshan/manager_profile.html', context)

#--------------For Temples----------------
@login_required
@user_is_temple_manager
def temple_add(request):
    temple = get_object_or_404(TempleManager,user=request.user)
    add_form = TempleAddForm(request.POST or None, request.FILES or None)
    if add_form.is_valid():
        instance = add_form.save(commit=False)
        instance.user=request.user
        instance.temple2 = temple.Temple_Name
        instance.save()
        
        return redirect('darshan:manager_profile')
    else:
        add_form = TempleAddForm()

    context = {'add_form':add_form, }            

    return render(request,'darshan/temple_add.html', context ) 

@login_required
@user_is_temple_manager
def temple_update(request,s=None):
    instance = get_object_or_404(Temples,temple2=s)
    add_form = TempleAddForm(request.POST or None,request.FILES or None, instance=instance)
    
    if add_form.is_valid() == True:
        instance = add_form.save(commit=False)
        instance.save()
        print("o")
        return redirect('darshan:manager_profile')
            
          
    context = {
                'add_form':add_form,
    }

    return render(request,'darshan/temple_add.html', context)

@login_required
@user_is_temple_manager
def temple_remove(request,s):

    instance = get_object_or_404(Temples,temple2=s)
    instance.delete()

    return redirect('darshan:manager_profile')               

#---------For Pictures-----------------

@login_required
@user_is_temple_manager
def picture_add(request):
    temple_manager = get_object_or_404(TempleManager, user=request.user)
    temples = get_object_or_404(Temples,temple2=temple_manager.Temple_Name)
    pic_add_form = PictureAddForm(request.POST or None, request.FILES or None)
    if pic_add_form.is_valid():
        instance = pic_add_form.save(commit=False)
        instance.user=request.user
        instance.Temple=temples
        instance.save()

        
        return redirect('darshan:manager_profile')
    else:
        pic_add_form = PictureAddForm()

    context = {'pic_add_form':pic_add_form, }            

    return render(request,'darshan/Picture_add.html', context ) 

@login_required
@user_is_temple_manager
def picture_update(request,s1=None):
    u=[]
    sender = get_object_or_404(TempleManager, user=request.user)
    instance = get_object_or_404(Picture,id=s1)
    pic_add_form = PictureAddForm(request.POST or None,request.FILES or None, instance=instance)
    
    if pic_add_form.is_valid() == True:
        instances = pic_add_form.save(commit=False)
        instances.save()
        if Picture().is_dirty():#-----------For Notifying of the update--------------
            user = User.objects.filter(is_superuser=False)
            for x in user:
                for y in x.profile.selected:
                    if y==instance.id:
                       u.append(x)
            print(u)
            if not u:
                recipient = user
            else:
                recipient = u
            notify.send(sender=sender, target=instance, recipient_list=list(recipient), verb="updated")
            for person in recipient:
                subject = 'Notification'
                verb="updated"
                message = render_to_string('darshan/notification_email.html', {
                'target':instance,'verb':verb })
                person.email_user(subject, message)
                send_verification_mail(person.email, message, subject)
            

        print("o")

        return redirect('darshan:manager_profile')
            
          
    context = {
                'pic_add_form':pic_add_form,
    }

    return render(request,'darshan/Picture_add.html', context)

@login_required
@user_is_temple_manager
def picture_remove(request,s1):

    instance = get_object_or_404(Picture,id=s1)
    instance.delete()

    return redirect('darshan:manager_profile')        

#--------------For Darshans----------------
@login_required
@user_is_temple_manager
def darshan_add(request):
    temple_manager = get_object_or_404(TempleManager,user=request.user)
    temples = get_object_or_404(Temples,temple2=temple_manager.Temple_Name)
    dar_add_form = DarshanAddForm(request.POST or None)
    if dar_add_form.is_valid():
        instance = dar_add_form.save(commit=False)
        instance.user=request.user
        instance.temple = temples
        instance.save()
        
        return redirect('darshan:manager_profile')
    else:
        dar_add_form = DarshanAddForm()

    context = {'dar_add_form':dar_add_form, }            

    return render(request,'darshan/darshan_add.html', context ) 


@login_required
@user_is_temple_manager
def darshan_update(request,s2=None):
    instance = get_object_or_404(Darshans,id=s2)
    dar_add_form = DarshanAddForm(request.POST or None, instance=instance)
    
    if dar_add_form.is_valid() == True:
        instance = dar_add_form.save(commit=False)
        instance.save()
        print("o")
        return redirect('darshan:manager_profile')
            
          
    context = {
                'dar_add_form':dar_add_form,
    }

    return render(request,'darshan/darshan_add.html', context)

@login_required
@user_is_temple_manager
def darshan_remove(request,s2):

    instance = get_object_or_404(Darshans,id=s2)
    instance.delete()

    return redirect('darshan:manager_profile')   

               
