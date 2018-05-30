from django import template
from darshan.models import Picture, Profile, Temples
from shop.models import Product
from django.utils.timezone import now, localtime
from operator import attrgetter
import datetime

register = template.Library()

@register.filter("temple")
def temple(value):
    return Temples.objects.filter(temple2=value)


@register.filter("picture")
def picture(value):
    return Picture.objects.filter(Temple_id=value.id)

@register.filter("pics")
def pics(value):
    return Picture.objects.filter(id=value)

@register.filter("darshan")
def darshan(value):
    return Temples.objects.filter(id=value)

@register.filter("product")
def product(value):
    return Product.objects.filter(TempleName_id=value)

@register.filter("ascend")
def ascend(value):
    return sorted(value, key= attrgetter('Price'),reverse=False)

@register.filter("descend")
def descend(value):
    return Product.objects.filter(TempleName_id=value).order_by('-Price')

@register.filter("time")
def time(value):
    m = localtime().time()
    s1 = str(m)
    s2 = str(value)
    c = datetime.datetime.strptime(s1, '%H:%M:%S.%f') - datetime.datetime.strptime(s2, '%H:%M:%S')
    return (c.total_seconds())/60
