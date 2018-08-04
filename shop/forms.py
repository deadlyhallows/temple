from django import forms
from shop.models import Product
from pagedown.widgets import PagedownWidget


class ProductAddForm(forms.ModelForm):
    Product_Name = forms.CharField(required=True)
    Price = forms.DecimalField(required=True)
    is_Prasad = forms.BooleanField(required=False)
    Product_Description = forms.CharField(widget=PagedownWidget, required=True)
    Out_of_Stock = forms.BooleanField(required=False)
    Offer_or_Discount = forms.CharField(required=False)

    class Meta:
        model = Product
        fields = ('Temple_Name', 'Product_Name', 'Out_of_Stock', 'Price', 'Photo','Photo1','Photo2','Photo3','Photo4','Photo5','Photo6','Offer_or_Discount',
                  'is_Prasad','Product_Description')

# class ProductExtraImagesForm(forms.ModelForm):
#
#     class Meta:
#         model = Photo
#         fields = ('photos','height_field','width_field')
# class CustomSearchForm(ModelSearchForm):
#     order_choices = [('y', 'Descending'), ('n', 'Ascending')]
#     order = forms.ChoiceField(choices=order_choices, widget=forms.RadioSelect(), required=False)

#     def search(self):
#         sqs = super(CustomSearchForm, self).search()
#         if not self.is_valid():
#             return self.no_query_found()

#         if self.cleaned_data['order'] == 'y':
#             sqs = sqs.order_by('-Price')
#         else:
#             sqs = sqs.order_by('Price')
#         return sqs
