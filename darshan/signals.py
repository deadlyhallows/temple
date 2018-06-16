from django.contrib.auth.models import User
from .models import Picture
from django.db.models.signals import post_save
from django.dispatch import receiver

from notify.models import Notification
import django.dispatch







