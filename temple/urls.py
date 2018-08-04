"""temple URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from shop import views as core_views
#from django.views.i18n import javascript_catalog


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('accountregistrations.urls', namespace='accountregistrations')),
    url(r'', include('darshan.urls', namespace='darshan')),
    url(r'', include('shop.urls', namespace='shop')),
    url(r'cart/', include('cart.urls', namespace='cart')),
    url(r'orders/', include('orders.urls', namespace='orders')),
    url(r'^notifications/', include('notify.urls', namespace='notifications')),
    #url(r'^pay/', include('payu_biz.urls', namespace='pay')),
    #url(r'^search/', include('haystack.urls')),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url('^', include('django.contrib.auth.urls')),
    #url(r'^admin/jsi18n', javascript_catalog),

]

handler400 = core_views.error400  # noqa
handler403 = core_views.error403  # noqa
handler404 = core_views.error404  # noqa
handler500 = core_views.error500  # noqa
handler200 = core_views.error200  # noqa



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG is False:
#     urlpatterns += [url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
#                     url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}), ]

