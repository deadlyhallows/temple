from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from darshan import views
from django.conf import settings







urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signupManager/$', views.signup1, name='signup1'),

    url(r'^login/$', auth_views.login,{'template_name':'darshan/home.html'}, name='login'),
    url(r'^user_profile/$',views.user_profile, name='user_profile'),
    url(r'^manager_profile/$',views.manager_profile, name='manager_profile'),
    url(r'^accounts/$',views.accounts, name='accounts'),
    url(r'^details/(?P<temp>.+)$',views.details, name='details'),
    url(r'^detail/(?P<temp1>.+)$', views.detail, name='detail'),
    url(r'^delete/(?P<value>.+)/$',views.delete, name='delete'),
    url(r'^online_donation/(?P<v>.+)/$',views.Online_Donation, name='Online_Donation'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    #------------ For knowing the type of users-------------
    url(r'^login/Usertype/$',views.Usertype, name='Usertype'),

    #------------ For Temples--------
    url(r'^temple_add/$',views.temple_add, name='temple_add'),
    url(r'^temple_update/(?P<s>.+)/$',views.temple_update, name='temple_update'),
    url(r'^temple_remove/(?P<s>.+)/$',views.temple_remove, name='temple_remove'),

    #------------- For Pictures----------
    url(r'^picture_add/$',views.picture_add, name='picture_add'),
    url(r'^picture_update/(?P<s1>.+)/$',views.picture_update, name='picture_update'),
    url(r'^picture_remove/(?P<s1>.+)/$',views.picture_remove, name='picture_remove'),

    #-----------For Darshans------------
    url(r'^darshan_add/$',views.darshan_add, name='darshan_add'),
    url(r'^darshan_update/(?P<s2>.+)/$',views.darshan_update, name='darshan_update'),
    url(r'^darshan_remove/(?P<s2>.+)/$',views.darshan_remove, name='darshan_remove'),


]



