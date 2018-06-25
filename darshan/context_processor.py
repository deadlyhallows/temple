from django.shortcuts import render, redirect, get_object_or_404
from .models import TempleManager


def Manager(request):
	set = request.user
	return {'set':set,}
	    # 'form': AuthenticationForm,
     #           'Mobile_form': MobileForm,
     #           'user_form': SignUpForm,}