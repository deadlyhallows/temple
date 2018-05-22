from django import template
from darshan.models import Picture, Profile, Temples

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
    return Temples.objects.filter(temple2=value)