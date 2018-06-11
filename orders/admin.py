from django.contrib import admin
from .models import Order, OrderItem
from django.contrib.auth.models import User
from notify.signals import notify



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if Order().is_dirty():
            user = User.objects.get(id=obj.buyer_id)
            notify.send(sender=self, target=obj, recipient=user, verb="accepted")
        obj.save()

admin.site.register(Order,OrderAdmin)

#class OrderAdmin(admin.ModelAdmin):
#    list_display = ['id','first_name','last_name','email','address','postal_code','city','created','updated','paid']
 #   list_filter = ['paid','created','updated']
  #  inlines = [OrderItemInline]

#admin.site.register(Order,OrderAdmin)

