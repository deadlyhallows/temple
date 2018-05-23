from django.contrib import admin
from darshan.models import Picture, Profile, Temples
from shop.models import Product, Photo
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(Product)
admin.site.register(Photo)
# Register your models here.
