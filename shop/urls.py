from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from darshan import views
from shop import views as core_views
from django.conf import settings

urlpatterns = [
    url(r'^allproducts/$', core_views.allproducts, name='allproducts'),
    url(r'^productdetails/(?P<pk>\d+)$', core_views.details1, name='details1'),

    # ----------For Shopkeeper-------------
    url(r'^seller_profile/$', core_views.seller_profile, name='seller_profile'),

    # ------------ For Shopkeeper--------
    url(r'^product_add/$', core_views.product_add, name='product_add'),
    url(r'^product_update/(?P<p>.+)/$', core_views.product_update, name='product_update'),
    url(r'^product_remove/(?P<p>.+)/$', core_views.product_remove, name='product_remove'),
]
