from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from temple.decorators import user_is_temple_manager
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from darshan.models import Picture, Profile, Temples, Darshans, TempleManager
from pandit.models import Pandit
from accountregistrations.models import Mobile
from shop.models import Shopkeeper, Product
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from darshan.forms import TempleForm, TempleManagerForm, TempleAddForm, PictureAddForm, DarshanAddForm, PrasadAddForm
from accountregistrations.forms import SignUpForm, contactInspireForm,MobileForm
from darshan.tokens import account_activation_token
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import AuthenticationForm
import smtplib
from django.contrib import messages
from django.shortcuts import get_object_or_404
from cart.cart import Cart
from shop.models import Product
from cart.models import CartItem, Carts
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from notify.signals import notify

# Create your views here.

# ------------For Users -------------
def signup(request):
    if request.method == 'POST' and 'usertype' in request.POST:
        user_form = SignUpForm(request.POST)
        mobile_form = MobileForm(request.POST)
        typeuser = request.POST.get('usertype', None)
        if user_form.is_valid() and mobile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()
            user.mobile.Mobile_Number = mobile_form.cleaned_data.get('Mobile_Number')
            user.mobile.save()
            if typeuser == 'seller':
                username = user_form.cleaned_data.get('username')
                users = get_object_or_404(User, username=username)
                seller = Shopkeeper.objects.create(user=users, is_shopkeeper=True)
                seller.save()
            if typeuser == 'pandit':
                username = user_form.cleaned_data.get('username')
                users = get_object_or_404(User, username=username)
                pandit = Pandit.objects.create(user=users, is_pandit=True)
                pandit.save()
            if typeuser == 'user':
                create_cart = Carts.objects.create(active=True, user_id=user.id)
                create_cart.save()
                cart = Cart(request)
                if cart is not None:  # create cart for the logged in user
                    try:
                        user_cart = Carts.objects.get(user_id=user.id)
                    except Carts.DoesNotExist:
                        user_cart = Carts.objects.create(user_id=user.id, active=True)
                    for item in cart:
                        cart_product = get_object_or_404(Product, Product_Name=item['product'])
                        cart_item = CartItem.objects.create(quantity=item['quantity'],
                                                            active=True, cart_id=user_cart.id,
                                                            product_id=cart_product.id)
                        cart_item.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Divya Kripa Account'
            message = render_to_string('accountregistrations/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return render(request, 'accountregistrations/account_activation_sent.html')
        else:
            arr = []
            for field in user_form:
                arr.append(field.errors)
            messages.error(request, user_form.errors)
    else:
        user_form = SignUpForm()
        mobile_form = MobileForm()
    context = {
        "user_form": user_form,
        "Mobile_form": mobile_form,

    }
    return render(request, 'darshan/home.html', context)


def account_activation_sent(request):
    return render(request, 'accountregistrations/account_activation_sent.html')


def activate(request, uidb64, token, ):
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
        login(request, user, backend='django.core.mail.backends.smtp.EmailBackend')
        return redirect('darshan:home')
    else:
        return render(request, 'accountregistrations/account_activation_invalid.html')


# Do change this when in production
email_address = 'divyakripamail@gmail.com'
email_password = 'startinspire16'


def send_verification_mail(email, msg, sub):
    # print("send verification mail")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, email, msg, sub)
        server.close()
        # print('successfully sent the mail')

    except:
        print("failed to send mail")


def Login(request):
    error_message = ""

    if request.method == 'POST':
        login_form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('accountregistrations:Usertype')
        else:
            # print(login_form.errors)
            error_message = "Incorrect username or password."
            messages.error(request, error_message)
            login_form = AuthenticationForm(request.POST)


    else:
        login_form = AuthenticationForm()
    return render(request, 'darshan/home.html', {'login_form': login_form, 'error_message': error_message})


@login_required
def Usertype(request):
    temple_manager = TempleManager.objects.filter(user=request.user)
    shopkeeper = Shopkeeper.objects.filter(user=request.user)
    pandit = Pandit.objects.filter(user=request.user)
    print("Pandit", pandit)
    if temple_manager:
        return redirect('darshan:manager_profile')
    if shopkeeper:
        return redirect('shop:seller_profile')
    if pandit:
        return redirect('darshan:pandit_profile')

    return redirect('darshan:user_profile')

# --------------For Temple-Managers---------------------

def signup1(request):
    # print("D")
    arr = []
    if request.method == 'POST':
        # print("p")
        user_form = SignUpForm(request.POST)
        mobile_form = MobileForm(request.POST)
        manager_form = TempleManagerForm(request.POST)
        # print("o")

        if user_form.is_valid() and mobile_form.is_valid() and manager_form.is_valid():
            # print("asd")
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()

            user.mobile.Mobile_No = mobile_form.cleaned_data.get('Mobile_No')
            user.mobile.save()

            users = user_form.cleaned_data.get('username')
            get_user = get_object_or_404(User, username=users)
            Temple_name = manager_form.cleaned_data.get('Temple_Name')
            tempman = TempleManager.objects.create(user=get_user, is_manager=True, Temple_Name=Temple_name)
            tempman.save()

            # send_mail(subject,message,from_email,to_list,fail_silently=True)
            current_site = get_current_site(request)
            subject = 'Activate Your Divya Kripa Account'
            message = render_to_string('accountregistrations/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            # send_verification_mail(user.email, message, subject)
            return render(request, 'accountregistrations/account_activation_sent.html')
        else:

            for field in user_form:
                arr.append(field.errors)
                # print(field.errors)
                # print("\n")
            messages.error(request, user_form.errors)

    else:
        # print("abc")
        user_form = SignUpForm()
        mobile_form = MobileForm()
        manager_form = TempleManagerForm()

    context = {
        "user_form": user_form,
        "Mobile_form": mobile_form,
        "manager_form": manager_form,

    }
    return render(request, 'darshan/home.html', context)
