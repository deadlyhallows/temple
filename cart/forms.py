from django import forms
from .models import CartItem


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1,21)]


class CartAddProductForm(forms.ModelForm):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    class Meta:
        model = CartItem
        fields = ('quantity', )


PRODUCT_QUANTITY_CHOICES1 = [(i, str(i)) for i in range(1, 26)]


class CartAddProductForms(forms.Form):#--------For Anonymous User---------------------------
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES1, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)