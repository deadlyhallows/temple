from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from darshan import views
from django.conf import settings







urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login,{'template_name':'darshan/home.html'}, name='login'),
    url(r'^login/user_profile/$',views.user_profile, name='user_profile'),
    url(r'^accounts/$',views.accounts, name='accounts'),
    url(r'^details/(?P<temp>.+)$',views.details, name='details'),
    url(r'^detail/(?P<temp1>.+)$', views.detail, name='detail'),
    url(r'^delete/(?P<value>.+)/$',views.delete, name='delete'),

    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),




]



