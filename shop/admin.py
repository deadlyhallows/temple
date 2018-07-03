from django.contrib import admin
from darshan.models import Picture, Profile, Temples
from shop.models import Product, Photo, Shopkeeper
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from notify.signals import notify
from cart.models import Carts, CartItem
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

class ProductAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        tm = obj.is_dirty()

        if tm:
            dirty_fields = obj.get_dirty_fields()
            print(dirty_fields)
            for field in dirty_fields:
                if field=='Out_of_Stock' and obj.Out_of_Stock==True:
                    us = []
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
                    notify.send(sender=self, target=obj, recipient_list=list(recipient), verb="Out of stock")
                    for person in recipient:
                      subject = 'Notification from Divya Kripa:Your Order'
                      verb="Out of Stock"
                      message = render_to_string('darshan/notification_email.html', {
                      'target':obj,'verb':verb })
                      person.email_user(subject, message)
                if field=='Out_of_Stock' and obj.Out_of_Stock==False:
                    us = []
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
                    notify.send(sender=self, target=obj, recipient_list=list(recipient), verb="Available")
                    for person in recipient:
                      subject = 'Notification from Divya Kripa:Your Order'
                      verb="Available"
                      message = render_to_string('darshan/notification_email.html', {
                      'target':obj,'verb':verb })
                      person.email_user(subject, message)

        obj.save()


admin.site.register(Product,ProductAdmin)
admin.site.register(Shopkeeper)
admin.site.register(Photo)
# Register your models here.
