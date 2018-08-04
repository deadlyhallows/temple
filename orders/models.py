from django.db import models
from shop.models import Product
from django.contrib.auth.models import User
from dirtyfields import DirtyFieldsMixin
from decimal import Decimal
from cart import cart
from darshan.models import Temples


class OnlineDonation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    temple = models.ForeignKey(Temples, on_delete=models.CASCADE)
    Amount = models.PositiveIntegerField(default=0)
    Purpose = models.TextField(blank=True)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.donor) + "," + str(self.temple)

class Order(DirtyFieldsMixin, models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    order_date = models.DateField(auto_now=True)
    is_delivered = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id) + "," + str(self.buyer)


    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=None)

    def __str__(self):
        return '{}'.format(self.id) + ',' + str(self.order)

    def get_cost(self):
        return self.price * self.quantity

class Payment(models.Model):
    order_no=models.OneToOneField(Order, on_delete=models.CASCADE)
    txnid = models.CharField(max_length=36, primary_key=True, default=None)
    amount = models.FloatField(null=True, blank=True, default=0.0)
    hash = models.CharField(max_length=500, null=True, blank=True)
    payment_method = models.CharField(max_length=1000, verbose_name='Payment-method', default=None, null=True)



