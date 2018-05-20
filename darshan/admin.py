from .models import Picture, Profile, Temples
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(Temples)
admin.site.register(Picture)
admin.site.register(Profile)
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