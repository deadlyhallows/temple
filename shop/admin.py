from django.contrib import admin
from darshan.models import Picture, Profile, Temples
from shop.models import Product, Photo, Shopkeeper
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from notify.signals import notify
from cart.models import Carts, CartItem
from django.shortcuts import get_object_or_404

class ProductAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        us = []
        tm = Product().is_dirty()
        user1 = User.objects.filter(is_superuser=False)
        user = CartItem.objects.filter(product_id=obj.id)
        for x in user:
            users = get_object_or_404(Carts, id=x.cart_id)
            c = get_object_or_404(User, id=users.user_id)
            us.append(c)

        if not us:
            recipient = user1
        else:
            recipient = us
        if tm:
            t = Product().get_dirty_fields()
            print(t)
            for z in t:
                if z=='OutofStock' and obj.OutofStock==True:
                   notify.send(sender=self, target=obj, recipient_list=list(recipient), verb="Out of stock")
                if z=='OutofStock' and obj.OutofStock==False:
                   notify.send(sender=self, target=obj, recipient_list=list(recipient), verb="Available")

        obj.save()


admin.site.register(Product,ProductAdmin)
admin.site.register(Shopkeeper)
admin.site.register(Photo)
# Register your models here.
