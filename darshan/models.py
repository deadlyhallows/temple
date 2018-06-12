from  __future__ import unicode_literals
from django.utils import timezone

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from dirtyfields import DirtyFieldsMixin

import datetime



     # Required

class Temples(models.Model):
    temple2 = models.CharField(max_length=250,default=None)
    Iconimages = models.ImageField(
        null=True, blank=True,
        height_field="height_field",
        width_field="width_field")
    images= models.ImageField(
        null=True, blank=True,
        height_field="height_field",
        width_field="width_field")
    height_field = models.IntegerField(default=None, null=True, blank=True)
    width_field = models.IntegerField(default=None, null=True, blank=True)
    Religion = models.CharField(max_length=200,default=None)
    Address = models.TextField(default=None)
    City = models.CharField(max_length=40, default=None)
    State = models.CharField(max_length=50, default=None)
    Country = models.CharField(max_length=60, default=None)
    Deity = models.CharField(max_length=100, default=None)
    Website = models.URLField(default=None)
    LiveDarshan = models.BooleanField(default=False)
    LiveDarshanlink = models.URLField(default=None,blank=True)
    OnlineDonationStatus = models.BooleanField(default=False,blank=True)
    OnlineDonation = models.URLField(default=None,blank=True)
    LivePooja = models.BooleanField(default=False)
    OnlinePooja = models.URLField(default=None,blank=True)
    OnlinePrasadStatus = models.BooleanField(default=False)
    OnlinePrasad = models.URLField(default=None, blank=True)
    OtherOnlineFacilityStatus = models.BooleanField(default=False)
    OtherOnlineFacility = models.URLField(default=None,blank=True)
    Contacts = models.CharField(max_length=300, default=None)
    PhoneNumber = models.CharField(max_length=300, default=None)
    Email = models.EmailField()
    AboutTemple = models.TextField(default=None)
    TempleHistory= models.TextField(default=None)
    TemplePurohit = models.CharField(max_length=250,default=None)
    Significance= models.TextField(default=None)
    Management= models.TextField(default=None)
    RelatedFaith=models.TextField(default=None)
    AboutCity = models.TextField(default=None)
    HowToReach = models.TextField(default=None)
    DoAndDont = models.TextField(default=None)
    Amenities = models.TextField(default=None)
    Celebration = models.TextField(default=None)
    PrecautionWhileVisiting = models.TextField(default=None)
    Tender = models.TextField(default=None, blank=True)
    Recruitment = models.TextField(default=None, blank=True, null=True)
    NoticeandUpdates = models.TextField(default=None, blank=True, null=True)
    Accomodation = models.BooleanField(default=False)
    AccomodationLink = models.URLField(default=None,blank=True)
    Annakshetra = models.BooleanField(default=False)


    def __str__(self):
        return self.temple2

    class Meta:
        ordering = [
            'temple2'
        ]

class Picture(DirtyFieldsMixin,models.Model):
    Temple = models.ForeignKey(Temples , on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(
        null=True,blank=True,
        height_field="height_field",
        width_field="width_field")
    height_field=models.IntegerField(default=None, null=True,blank=True)
    width_field=models.IntegerField(default=None,null=True,blank=True)
    TimeD=models.TimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    publish = models.DateField(auto_now_add=False,auto_now=False)
    timestamp = models.DateField(auto_now=False,auto_now_add=True)
    updated = models.DateField(auto_now=True,auto_now_add=False)

   # objects = PostManager()
    def __unicode__(self):
        return self.Temple.temple2


    def __str__(self):
        return self.Temple.temple2


#class Meta:
       # ordering = ['-timestamp','-updated']#important

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Temple1 = ArrayField(models.CharField(max_length=250,default=None,blank=True,null=True),default=list,blank=True,null=True)
    selected = ArrayField(models.IntegerField(default=None),default=list,blank=True,null=True)

    def __str__(self):
        return self.user.username


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)


class Mobile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Mobile_No = models.CharField(max_length=15,blank=True,null=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_mobile(sender, instance, created, **kwargs):
        if created:
            Mobile.objects.create(user=instance)


class Darshans(models.Model):
    temple = models.ForeignKey(Temples,on_delete= models.CASCADE)
    rituals = models.CharField(max_length=250,default=None)
    timings = models.CharField(max_length=250,default=None)
    #rituals = ArrayField(models.CharField(max_length=250,default=None,blank=True,null=True),default=list,blank=True,null=True)
    #timings = ArrayField(models.CharField(max_length=250,default=None,blank=True,null=True),default=list,blank=True,null=True)

    def __str__(self):
        return self.temple.temple2

class OnlineDonation(models.Model):
    donor=models.ForeignKey(User,on_delete=models.CASCADE)
    temple=models.ForeignKey(Temples,on_delete=models.CASCADE)
    Amount=models.PositiveIntegerField(default=0)
    Purpose=models.TextField(blank=True)
    status=models.BooleanField(default=False)

    def __str__(self):
        return str(self.donor) + "," + str(self.temple)


