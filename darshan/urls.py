from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from darshan import views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signupManager/$', views.signup1, name='signup1'),

    url(r'^login/$', views.Login, name='Login'),

    url(r'^user_profile/$', views.user_profile, name='user_profile'),
    url(r'^manager_profile/$', views.manager_profile, name='manager_profile'),
    url(r'^pandit_profile/$', views.pandit_profile, name='pandit_profile'),
    url(r'^selectedDarshan/$', views.selectedDharshan, name='accounts'),
    url(r'^details/(?P<temp>.+)$', views.details, name='details'),
    url(r'^detail/(?P<temp1>.+)$', views.detail, name='detail'),
    url(r'^selectedTemple/(?P<pk>\d+)$', views.selectedTemple, name='selectedTemple'),
    url(r'^allPrasad/(?P<pk>\d+)$', views.all_Prasad, name='all_Prasad'),
    url(r'^delete/(?P<value>.+)/$', views.delete, name='delete'),

    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    # -----------For gmail login-------------
    url(r'^auth/complete/google-oauth2/Usertype/$', views.Usertype, name='Usertype'),

    # -----------For Facebook login-----------
    url(r'^auth/complete/facebook/Usertype/$', views.Usertype, name='Usertype'),

    # -------------For Password Reset----------------------

    url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'registrations/password_reset_form.html'},
        name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done,
        {'template_name': 'registrations/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'template_name': 'registrations/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'registrations/password_reset_complete.html'}, name='password_reset_complete'),

    # ------------ For knowing the type of users-------------
    url(r'^login/Usertype/$', views.Usertype, name='Usertype'),

    # ------------ For Temples--------
    url(r'^temple_add/$', views.temple_add, name='temple_add'),
    url(r'^temple_update/(?P<s>.+)/$', views.temple_update, name='temple_update'),
    url(r'^temple_remove/(?P<s>.+)/$', views.temple_remove, name='temple_remove'),

    # ------------- For Pictures----------
    url(r'^picture_add/$', views.picture_add, name='picture_add'),
    url(r'^picture_update/(?P<s1>.+)/$', views.picture_update, name='picture_update'),
    url(r'^picture_remove/(?P<s1>.+)/$', views.picture_remove, name='picture_remove'),

    # -----------For Darshans------------
    url(r'^darshan_add/$', views.darshan_add, name='darshan_add'),
    url(r'^darshan_update/(?P<s2>.+)/$', views.darshan_update, name='darshan_update'),
    url(r'^darshan_remove/(?P<s2>.+)/$', views.darshan_remove, name='darshan_remove'),
    url(r'^alldarshan/$', views.allDarshan, name='alldarshan'),

    # ----------------For Prasad-----------------

    url(r'^prasad_add/$', views.prasad_add, name='prasad_add'),
    url(r'^prasad_update/(?P<p>.+)/$', views.prasad_update, name='prasad_update'),
    url(r'^prasad_remove/(?P<p>.+)/$', views.prasad_remove, name='prasad_remove'),

]
