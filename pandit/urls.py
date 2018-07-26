from django.conf.urls import url
from pandit import views

urlpatterns = [

url(r'^pandit_profile/$', views.pandit_profile, name='pandit_profile'),

    ]