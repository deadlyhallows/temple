from django.conf.urls import url
from django.contrib.auth import views as auth_views
from accountregistrations import views
from django.conf import settings


urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signupManager/$', views.signup1, name='signup1'),

    url(r'^login/$', views.Login, name='Login'),

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

]