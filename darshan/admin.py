from .models import Picture, Profile, Temples, Darshans, Mobile,TempleManager, ContactInspire, Pandit
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from notify.signals import notify
from pagedown.widgets import AdminPagedownWidget
from django.db import models
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .views import send_verification_mail
from django.utils.http import urlsafe_base64_decode


class TempleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }

class PictureAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        u=[]

        if obj.is_dirty():
          dirty_fields = obj.get_dirty_fields()
          #print(dirty_fields)
          for field in dirty_fields:
            if field == 'image':
              user = User.objects.filter(is_superuser=False)
              for x in user:
                  for y in x.profile.selected:
                      if y==obj.id:
                         u.append(x)
              #print(u)
              if not u:
                  recipient = user
              else:
                  recipient = u
              notify.send(sender=self, target=obj, recipient_list=list(recipient), verb="updated")
              for person in recipient:
                  subject = 'Notification of update'
                  verb = "updated"
                  message = render_to_string('darshan/notification_email.html', {
                      'target': obj, 'verb': verb})
                  person.email_user(subject, message)
              obj.save()





admin.site.register(TempleManager)
admin.site.register(Temples, TempleAdmin)
admin.site.register(Mobile)
admin.site.register(Darshans)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Profile)
admin.site.register(ContactInspire)
admin.site.register(Pandit)

#class ProfileInline(admin.StackedInline):
 #   model = Profile
  #  can_delete = False
   # verbose_name_plural = 'Profile'
    #fk_name = 'user'

#class CustomerUserAdmin(UserAdmin):
 #   inlines = (ProfileInline, )
  #  list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_temple', 'get_Mobile_No')
    # list_select_related = ('profile',)

    #def get_temple(self, instance):
    #   return instance.profile.Temple
    #get_temple.short_description = 'Temple'

    #def get_Mobile_No(self, instance):
    #   return instance.profile.Mobile_No
    #get_Mobile_No.short_description = 'Mobile_No'

    #def get_inline_instances(self, request, obj=None):
     #   if not obj:
      #      return list()
       # return super(CustomerUserAdmin, self).get_inline_instances(request, obj)


#admin.site.unregister(User)
#admin.site.register(Picture)
#admin.site.register(User, CustomerUserAdmin)