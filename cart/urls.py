from django.conf.urls import url
from . import views

urlpatterns = [
    #for UN-authenticated user
    url(r'^cart_detail/$', views.cart_detail, name='cart_detail'),
    url(r'^cart_add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    url(r'^cart_remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),

    #for authenticated user
    url(r'^$', views.view_cart, name='view_cart'),
    url(r'^add/(?P<product_id>\d+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^update_quantity/(?P<product_id>\d+)/$', views.update_quantity, name='update_quantity'),
    url(r'^remove/(?P<product_id>\d+)/$', views.remove_from_cart, name='remove_from_cart'),
]