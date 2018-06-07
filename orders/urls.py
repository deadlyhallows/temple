from django.conf.urls import url
from . import views
'^'

urlpatterns = [
    url(r'^order_create/$', views.order_create, name='order_create'),
    url(r'^payment/$',views.payment, name='payment'),

    url(r'^payment/success$', views.payment_success, name="payment_success"),
    url(r'^payment/failure$', views.payment_failure, name="payment_failure"),
]