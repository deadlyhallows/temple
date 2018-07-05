from __future__ import unicode_literals
from django.utils import timezone

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from dirtyfields import DirtyFieldsMixin

import datetime


class Temples(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    temple2 = models.CharField(max_length=250, default=None)
    Display_image = models.ImageField(
        null=True, blank=True,
        height_field="height_field",
        width_field="width_field")
    Latest_to_be_updated_image = models.ImageField(
        null=True, blank=True,
        height_field="height_field",
        width_field="width_field")
    height_field = models.IntegerField(default=None, blank=True)
    width_field = models.IntegerField(default=None, blank=True)
    Deity = models.CharField(max_length=100, default=None)
    About_Temple = models.TextField(default=None)
    City = models.CharField(max_length=40, default=None)
    Contacts = models.CharField(max_length=300, default=None)
    Phone_Number = models.CharField(max_length=300, default=None)
    Address = models.TextField(default=None)
    Email = models.EmailField()
    Temple_Purohit = models.CharField(max_length=250, default=None)
    Religion = models.CharField(max_length=200, default="Hindu",blank=True,null=True)#About temple
    Related_Faith = models.TextField(default=None,blank=True,null=True)
    Website = models.URLField(default=None,blank=True,null=True)
    Temple_History = models.TextField(default=None,blank=True,null=True)
    Significance = models.TextField(default=None,blank=True,null=True)
    Celebration = models.TextField(default=None,blank=True,null=True)
    Live_Darshan_link = models.URLField(default=None, blank=True,null=True)
    Management = models.TextField(default=None,blank=True,null=True)
    Other_Deities=models.TextField(default=None,blank=True,null=True)
    Related_Temple=models.TextField(default=None,blank=True,null=True)
    Accomodation_Link = models.URLField(default=None, blank=True,null=True)#TempleFacilities
    Annakshetra = models.BooleanField(default=False)
    Online_Pooja = models.URLField(default=None, blank=True, null=True)
    Online_Donation = models.URLField(default=None, blank=True,null=True)
    Online_Prasad = models.URLField(default=None, blank=True, null=True)
    Online_Facility = models.URLField(default=None, blank=True, null=True)
    Transportation = models.TextField(default=None,blank=True,null=True)
    About_City = models.TextField(default=None,blank=True,null=True)#visit Temple
    How_To_Reach = models.TextField(default=None,blank=True,null=True)
    Do_And_Dont = models.TextField(default=None,blank=True,null=True)
    Amenities = models.TextField(default=None,blank=True,null=True)
    Precaution_While_Visiting = models.TextField(default=None,blank=True,null=True)
    State = models.CharField(max_length=50, default=None,blank=True,null=True)
    Country = models.CharField(max_length=60, default=None,blank=True,null=True)
    Tender = models.FileField(upload_to='file_uploads/',blank=True,null=True)#Temple Miscelleneous
    Recruitment = models.TextField(default=None, blank=True,null=True)
    Notice_and_Updates = models.TextField(default=None, blank=True,null=True)
    

    def __str__(self):
        return self.temple2

    class Meta:
        ordering = [
            'temple2'
        ]

class Picture(DirtyFieldsMixin, models.Model):
    Temple = models.ForeignKey(Temples, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(
        null=True, blank=True,
        height_field="height_field",
        width_field="width_field")
    height_field = models.IntegerField(default=None, null=True, blank=True)
    width_field = models.IntegerField(default=None, null=True, blank=True)
    Time = models.TimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    Ritual = models.CharField(max_length=200,default=None)
    publish = models.DateField(auto_now_add=False, auto_now=False)
    timestamp = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)

    # objects = PostManager()
    def __unicode__(self):
        return self.Temple.temple2

    def __str__(self):
        return str(self.Temple.temple2) + ',' + str(self.Time)


# class Meta:
# ordering = ['-timestamp','-updated']#important

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Select_Temple = ArrayField(models.CharField(max_length=250, default=None, blank=True, null=True), default=list,
                               blank=True, null=True)
    selected = ArrayField(models.IntegerField(default=None), default=list, blank=True, null=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)


class Mobile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Mobile_Number = models.CharField(max_length=15, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_mobile(sender, instance, created, **kwargs):
        if created:
            Mobile.objects.create(user=instance)


class Darshans(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    temple = models.ForeignKey(Temples, on_delete=models.CASCADE)
    rituals = models.CharField(max_length=250, default=None)
    timings = models.CharField(max_length=250, default=None)

    

    def __str__(self):
        return str(self.rituals)




class TempleManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)
    Temple_Name = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.user.username

class ContactInspire(models.Model):
    Name = models.CharField(max_length=100, default=None)
    Email = models.CharField(max_length=400, default=None)
    Comment = models.TextField()

    def __str__(self):
        return self.Name