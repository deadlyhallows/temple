from django import forms
from darshan.models import Temples
from shop.models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from haystack.forms import SearchForm
from django.utils.translation import ugettext_lazy as _
from haystack.forms import ModelSearchForm



class ProductAddForm(forms.ModelForm):
    class Meta:
        model=Product
        fields = ('ProductName', 'TempleName', 'OutofStock', 'Price', 'Photo')

    

class CustomSearchForm(ModelSearchForm):
    order_choices=[('y', 'Descending'), ('n', 'Ascending')]
    order = forms.ChoiceField(choices=order_choices, widget=forms.RadioSelect(), required=False)



    def search(self):
        sqs = super(CustomSearchForm, self).search()
        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['order'] == 'y':
            sqs = sqs.order_by('-Price')
        else:
                sqs = sqs.order_by('Price')
        return sqs