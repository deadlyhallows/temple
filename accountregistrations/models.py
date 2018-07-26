from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from dirtyfields import DirtyFieldsMixin
# Create your models here.



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



class ContactInspire(models.Model):
    Name = models.CharField(max_length=100, default=None)
    Email = models.CharField(max_length=400, default=None)
    Comment = models.TextField()

    def __str__(self):
        return self.Name