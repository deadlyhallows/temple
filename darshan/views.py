from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Picture, Profile, Temples, Mobile
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from darshan.forms import SignUpForm, TempleForm, MobileForm
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




def home(request):
    return render(request, 'darshan/home.html',{'form':AuthenticationForm,'Mobile_form':MobileForm,
                                                'user_form':SignUpForm})


def signup(request):

    print("D")
    if request.method == 'POST':
        print("p")
        user_form = SignUpForm(request.POST)
        mobile_form = MobileForm(request.POST)
        print("o")

        if user_form.is_valid() and mobile_form.is_valid():
            print("asd")
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()

            user.mobile.Mobile_No = mobile_form.cleaned_data.get('Mobile_No')
            user.mobile.save()
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
        "Mobile_form":mobile_form

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
def user_profile(request):
    user=request.user
    profile=Profile.objects.get(user_id=user.id)
    print("a")
    if request.POST:
        print("b")
        form = TempleForm(request.POST,instance=profile)
        print("c")
        if form.is_valid():
            print("d")
            profile=form.save(commit=False)
            profile.save()

            return redirect('/login/user_profile/', {'form':form})
        else:
            messages.error(request, "not created at all")
    else:
        form = TempleForm()
    print("e")
    query_list=Profile.objects.filter(user_id=user.id)

    if request.POST:
        for t in query_list:
            print(t)
            for x in t.Temple1:
                city_pk_list = request.POST.getlist(x, None)
                for z in city_pk_list:
                    s = Picture.objects.get(id=z)
                    s.selected=True
                    s.save()

    context={'set': user,
            'query_list':query_list,
            'form':form,
                 }
    return render(request, 'darshan/user_profile.html', context)

def TempleTimeSelected(request):
    city_pk_list = request.POST.getlist('x', None)
    for z in city_pk_list:
        z.selected=True
    return render(request, 'darshan/user_profile.html')


def accounts(request):
    #set = Profile.objects.all()
    img=Picture.objects.filter(selected=True)
    context = {
        'img':img
    }
    return render(request,'darshan/accounts.html', context)





