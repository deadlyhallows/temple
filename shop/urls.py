from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from darshan import views
from shop import views as core_views
from django.conf import settings




urlpatterns = [
    url(r'^allproducts/$', core_views.allproducts, name='home'),

]