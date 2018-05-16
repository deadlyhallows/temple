from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Picture,Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from darshan.forms import SignUpForm, ChoiceForm
from darshan.tokens import account_activation_token
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
import smtplib
from django.core import serializers
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from django.template import Context




def home(request):
    return render(request, 'darshan/home.html')


def signup(request):

    print("D")
    if request.method == 'POST':
        print("p")
        user_form = SignUpForm(request.POST)
        print("o")
        profile_form = ChoiceForm(request.POST)
        print("k")
        if user_form.is_valid() and profile_form.is_valid():
            print("asd")
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()

            user.profile.Mobile_No = profile_form.cleaned_data.get('Mobile_No')
            user.profile.save()
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
            send_verification_mail(user.email, message,subject)
            return render(request, 'darshan/account_activation_sent.html')
    else:
        print("abc")
        user_form = SignUpForm()
        profile_form = ChoiceForm()

    context = {
        "user_form":user_form,
        "profile_form":profile_form
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
        user.profile.email_confirmed = True
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



def user_profile(request):
        set = request.user
        print(set)
        a = Picture.objects.all()
        print(a)
        print(set.id)
        if request.POST:
            city_pk_list = request.POST.getlist('Temple', None)
            print(request.POST.getlist('Temple', None))

            selected_city_obj_list = Picture.objects.filter(pk__in=city_pk_list)
            print(selected_city_obj_list)
            print(set.profile)
            for temp in selected_city_obj_list:
                print(temp.Temple)
                ab = str(temp.Temple)
                print(ab)
                set.profile.Temple1.append(ab)
                print(set.profile.Temple1)
            set.profile.save()
        query_set2 = Profile.objects.filter(user_id=set.id)
        for t in query_set2:
            for x in t.Temple1:
                print(x)

        context={'set': set,
                 'object_list':a,
                 'query_list':query_set2}

        return render(request, 'darshan/user_profile.html', context)

def accounts(request):
    #set = Profile.objects.all()
    set = request.user
    query_set2 = Profile.objects.get(id=set.id)
    query = query_set2.Temple
    pro = Picture.objects.filter(Temple=query)
    context = {
        "set":set,
        "query_set":pro

    }
    return render(request,'darshan/accounts.html', context)





