from django.db import models
from shop.models import Product
from decimal import Decimal
from cart import cart



class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email= models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    order_date = models.DateField(auto_now=True)
    # buyer = models.ForeignKey(Buyer)
    txnid = models.CharField(max_length=36, primary_key=True, default=None)
    amount = models.FloatField(null=True, blank=True, default=0.0)
    hash = models.CharField(max_length=500, null=True, blank=True)
    billing_name = models.CharField(max_length=500, null=True, blank=True)
    billing_street_address = models.CharField(max_length=500, null=True, blank=True)
    billing_country = models.CharField(max_length=500, null=True, blank=True)
    billing_state = models.CharField(max_length=500, null=True, blank=True)
    billing_city = models.CharField(max_length=500, null=True, blank=True)
    billing_pincode = models.CharField(max_length=500, null=True, blank=True)
    billing_mobile = models.CharField(max_length=500, null=True, blank=True)
    billing_email = models.CharField(max_length=500, null=True, blank=True)

    shipping_name = models.CharField(max_length=500, null=True, blank=True)
    shipping_street_address = models.CharField(max_length=500, null=True, blank=True)
    shipping_country = models.CharField(max_length=500, null=True, blank=True)
    shipping_state = models.CharField(max_length=500, null=True, blank=True)
    shipping_city = models.CharField(max_length=500, null=True, blank=True)
    shipping_pincode = models.CharField(max_length=500, null=True, blank=True)
    shipping_mobile = models.CharField(max_length=500, null=True, blank=True)
    shipping_rate = models.FloatField(null=False, blank=False, default=0.0)
    status = models.CharField(max_length=500, null=True, blank=True)
    shipping_email = models.CharField(max_length=500, null=True, blank=True)

    payment_method = models.CharField(max_length=1000, verbose_name='Payment-method', default=None, null=True)
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=None)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


