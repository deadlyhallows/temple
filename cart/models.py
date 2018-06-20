from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import User
import datetime

from django.contrib.auth.models import User
from django.db import models
from shop.models import Product


class Carts(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return 'Cart #' + str(self.id) + ',' +str(self.user.username)


class CartItem(models.Model):
    cart = models.ForeignKey(Carts, null=True, blank=True)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return 'Order #' + str(self.id) + ' of ' + self.product.ProductName

    