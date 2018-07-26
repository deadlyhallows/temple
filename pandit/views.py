from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def pandit_profile(request):
    return render(request, 'pandit/pandit_profile.html')
