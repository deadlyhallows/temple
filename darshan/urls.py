from django.conf.urls import url
from darshan import views


urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^user_profile/$', views.user_profile, name='user_profile'),
    url(r'^manager_profile/$', views.manager_profile, name='manager_profile'),
    url(r'^selectedDarshan/$', views.selectedDharshan, name='accounts'),
    url(r'^details/(?P<temp>.+)$', views.details, name='details'),
    url(r'^detail/(?P<temp1>.+)$', views.detail, name='detail'),
    url(r'^selectedTemple/(?P<pk>\d+)$', views.selectedTemple, name='selectedTemple'),
    url(r'^allPrasad/(?P<pk>\d+)$', views.all_Prasad, name='all_Prasad'),
    url(r'^delete/(?P<value>.+)/$', views.delete, name='delete'),


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
