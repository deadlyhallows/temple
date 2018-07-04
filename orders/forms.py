from django import forms
from .models import Order,OnlineDonation



class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['address', 'postal_code', 'city', ]

class DonationForm(forms.ModelForm):
    Amount = forms.IntegerField(required=True)

    class Meta:
        model = OnlineDonation
        fields = ('Amount', 'Purpose',)        