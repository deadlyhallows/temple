from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Picture, Profile, Temples, Mobile
from django.utils import timezone
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
from django.contrib import messages
from django.utils.timezone import now, localtime
import datetime
import time
from django.db.models import F
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404



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
    b=[]
    user=request.user
    profile=Profile.objects.get(user_id=user.id)
    print(profile.Temple1)
    if request.POST:
        print("b")
        print(profile.Temple1)
        c=profile.Temple1

        form = TempleForm(request.POST,instance=profile)
        print("c")
        if form.is_valid():
            print(profile.Temple1)
            profile=form.save(commit=False)
            for a in c:
                print(a)
                profile.Temple1.append(a)
            print(profile.Temple1)
            profile.save()

            return redirect('/login/user_profile/')
        else:
            messages.error(request, "not created at all")
    else:
        form = TempleForm()
    print("e")
    query_list=Profile.objects.filter(user_id=user.id)
    u = User.objects.get(id=user.id)
    v = Mobile.objects.get(id=user.id)
    if request.POST:
        for t in query_list:
            print(t)
            for x in t.Temple1:
                city_pk_list = request.POST.getlist(x, None)
                for z in city_pk_list:
                    s = Picture.objects.get(id=z)
                    profile.selected.append(s.id)
                    profile.save()
    for n in query_list:
        for m in n.Temple1:
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
             'u':u,
             'v':v,
             'page_change_var': page_change_var
                 }
    return render(request, 'darshan/user_profile.html', context)

@login_required
def accounts(request):
    #set = Profile.objects.all()
    user=request.user
    pro=Profile.objects.filter(user_id=user.id)
    for i in pro:
        print(i)
        for j in i.Temple1:
            print(j)
            r = Temples.objects.filter(temple2=j)
            print(r)
    context={'pro':pro}
    return render(request,'darshan/accounts.html', context)

@login_required
def delete(request, value):
    print("a")
    user=request.user
    print(user)
    query_l = Profile.objects.get(user_id=user.id)
    print("b")
    for i in query_l.Temple1:
        if i==value:
            query_l.Temple1.remove(i)
            query_l.save()
    t=Temples.objects.get(temple2=value)
    s=Picture.objects.filter(Temple_id=t.id)
    for j in s:
        for k in query_l.selected:
            if k==j.id:
                query_l.selected.remove(k)
                query_l.save()

    return redirect('/login/user_profile/')

@login_required
def details(request, temp):
    #m = localtime().time()
    #FMT = '%H:%M:%S'
    user = request.user
    pro = Profile.objects.get(user_id=user.id)
    q=Temples.objects.get(temple2=temp)
    b = Picture.objects.filter(Temple_id=q.id)
    t = 200
    context={
        't':t,
        'q':q,
        'b':b,
        'pro':pro,

    }
    return render(request, 'darshan/details.html', context)

