from django.db import models
from darshan.models import Temples
from django.contrib.postgres.fields import ArrayField
from dirtyfields import DirtyFieldsMixin
from django.contrib.auth.models import User

# Create your models here.

class Shopkeeper(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    is_shopkeeper=models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class Product(DirtyFieldsMixin, models.Model):
    seller=models.ForeignKey(Shopkeeper, on_delete=models.CASCADE,default=None)
    Product_Name=models.CharField(max_length=250, default=None)
    Temple_Name=models.ForeignKey(Temples, on_delete=models.CASCADE,blank=False)
    Out_of_Stock=models.BooleanField(default=False)
    Price=models.DecimalField(max_digits=19,decimal_places=2,default=None)
    Photo = models.ImageField(
        null=True, blank=True,
        height_field="height_field",
        width_field="width_field")
    height_field = models.IntegerField(default=None, null=True, blank=True)
    width_field = models.IntegerField(default=None, null=True, blank=True)
    Offer_or_Discount = models.CharField(max_length=50, default=None, blank=True,null=True)
    #Add 'Available' field if needed
    def __str__(self):
        return str(self.Product_Name)

    class Meta:
        ordering = [
            'Price'
        ]

class Photo(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    photos = models.ImageField(
        null=True, blank=True,
        height_field="height_field",
        width_field="width_field")
    height_field = models.IntegerField(default=None, null=True, blank=True)
    width_field = models.IntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return self.product

class ProductSelected(models.Model):
    products = ArrayField(models.IntegerField(default=None,blank=True,null=True),default=list,blank=True,null=True)

    def __str__(self):
        return self.id





