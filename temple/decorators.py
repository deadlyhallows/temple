from django.core.exceptions import PermissionDenied
from darshan.models import TempleManager
from shop.models import Shopkeeper

def user_is_temple_manager(function):
    def wrap(request, *args, **kwargs):
        users = TempleManager.objects.filter(user=request.user)
        if users:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_shopkeeper(function):
    def wrap(request, *args, **kwargs):
        usershop = Shopkeeper.objects.filter(user=request.user)
        if usershop:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap    