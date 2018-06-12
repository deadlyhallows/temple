from django.db import models
from darshan.models import Temples
from django.contrib.postgres.fields import ArrayField
from dirtyfields import DirtyFieldsMixin
# Create your models here.

class Product(DirtyFieldsMixin, models.Model):
    ProductName=models.CharField(max_length=250, default=None)
    TempleName=models.ForeignKey(Temples, on_delete=models.CASCADE)
    OutofStock=models.BooleanField(default=False)
    Price=models.DecimalField(max_digits=4,decimal_places=2,default=None)
    Photo = models.ImageField(
        null=True, blank=True,
        height_field="height_field",
        width_field="width_field")
    height_field = models.IntegerField(default=None, null=True, blank=True)
    width_field = models.IntegerField(default=None, null=True, blank=True)
    OfferorDiscount= models.CharField(max_length=50, default=None, blank=True)
    #Add Available field if needed
    def __str__(self):
        return self.ProductName

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