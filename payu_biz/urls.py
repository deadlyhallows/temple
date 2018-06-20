from django.conf.urls import include, url
from payu_biz import views
from payu_biz import views1
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [

	url(r'^make_transaction/$',views.make_transaction, name='make_transaction'),

    url(r'^payubiz-success/$',views.payu_success, name='payu_success'),

    url(r'^payubiz-failure/$', views.payu_failure, name='payu_failure'),
 
    url(r'^payubiz-cancel/$', views.payu_cancel, name='payu_cancel'),

]
