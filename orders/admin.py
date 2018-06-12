from django.contrib import admin
from .models import Order, OrderItem
from django.contrib.auth.models import User
from notify.signals import notify



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        tm = Order().is_dirty()
        if tm:
            t = Order().get_dirty_fields()
            print(t)
            for z in t:
                if z=='is_delivered' and z!='is_accepted' and obj.is_delivered==True:
                    obj.is_accepted=False
                    obj.save()
                    user = User.objects.get(id=obj.buyer_id)
                    notify.send(sender=self, target=obj, recipient=user, verb="delivered")
                if z=='is_accepted' and z!='is delivered' and obj.is_accepted==True:
                    user = User.objects.get(id=obj.buyer_id)
                    notify.send(sender=self, target=obj, recipient=user, verb="accepted")

        obj.save()

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)

#class OrderAdmin(admin.ModelAdmin):
#    list_display = ['id','first_name','last_name','email','address','postal_code','city','created','updated','paid']
 #   list_filter = ['paid','created','updated']
  #  inlines = [OrderItemInline]

#admin.site.register(Order,OrderAdmin)

