from django.shortcuts import render, redirect, get_object_or_404
from .models import TempleManager
from django.contrib.auth.forms import AuthenticationForm
from darshan.forms import SignUpForm, TempleForm, MobileForm, TempleManagerForm


def Manager(request):
    return {
        'login_form': AuthenticationForm,
        'Mobile_form': MobileForm,
        'user_form': SignUpForm,
        'manager_form': TempleManagerForm, }
