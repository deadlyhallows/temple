from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from darshan.forms import TempleForm,TempleManagerForm
from accountregistrations.forms import SignUpForm,MobileForm

def Manager(request):
    return {
        'login_form': AuthenticationForm,
        'Mobile_form': MobileForm,
        'user_form': SignUpForm,
        'manager_form': TempleManagerForm, }
