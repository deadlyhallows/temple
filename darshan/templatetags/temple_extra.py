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
    return Product.objects.filter(Temple_Name_id=value)

@register.filter("products1")
def products1(value):
    return Product.objects.filter(id=value)

@register.filter("products")
def products(value):
    return Product.objects.filter(Product_Name=value)

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty * unit_price

@register.filter("descend")
def descend(value):
    return Product.objects.filter(Temple_Name_id=value).order_by('-Price')

@register.filter("time")
def time(value):
    m = localtime().time()
    s1 = str(m)
    s2 = str(value)
    c = datetime.datetime.strptime(s1, '%H:%M:%S.%f') - datetime.datetime.strptime(s2, '%H:%M:%S')
    return (c.total_seconds())/60
