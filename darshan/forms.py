from django import forms

from .models import Profile, Temples,TempleManager, Picture, Darshans
from shop.models import Product 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from pagedown.widgets import PagedownWidget
from django.forms.extras.widgets import SelectDateWidget

from django.contrib.admin.widgets import AdminTimeWidget
from django.contrib.auth.forms import AuthenticationForm

from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)


class TempleForm(forms.ModelForm):



    def __init__(self,*args, **kwargs):
        super(TempleForm, self).__init__(*args, **kwargs)
        self.fields['Select_Temple'] = forms.MultipleChoiceField(
            choices=[(i.temple2, i.temple2) for i in Temples.objects.all()]
        )
  
    class Meta:
        model = Profile
        fields = ('Select_Temple',)



class TempleManagerForm(forms.ModelForm):
    class Meta:
        model = TempleManager
        fields = ('Temple_Name',)


class TempleAddForm(forms.ModelForm):
    Display_image = forms.ImageField(required=True)
    Latest_to_be_updated_image = forms.ImageField(required=True)
    Deity = forms.CharField(max_length=200,required=True)
    City = forms.CharField(max_length=200,required=True)
    About_Temple = forms.CharField(widget=PagedownWidget,required=True)
    Contacts = forms.CharField(max_length=200,required=True)
    Phone_Number = forms.CharField(max_length=200,required=True)
    Temple_Purohit = forms.CharField(max_length=200,required=True)
    Address = forms.CharField(widget=PagedownWidget,required=True)
    Religion = forms.CharField(max_length=200,required=False)
    Management= forms.CharField(widget=PagedownWidget,required=False)
    Related_Faith= forms.CharField(widget=PagedownWidget,required=False)
    Temple_History= forms.CharField(widget=PagedownWidget,required=False)
    Significance= forms.CharField(widget=PagedownWidget,required=False)
    Other_Deities= forms.CharField(widget=PagedownWidget,required=False)
    Related_Temple = forms.CharField(widget=PagedownWidget,required=False)
    Celebration = forms.CharField(widget=PagedownWidget,required=False)
    Transportation = forms.CharField(widget=PagedownWidget,required=False)
    State = forms.CharField(max_length=200,required=False)
    Country = forms.CharField(max_length=200,required=False)
    About_City = forms.CharField(widget=PagedownWidget,required=False)
    How_To_Reach = forms.CharField(widget=PagedownWidget,required=False)
    Do_And_Dont = forms.CharField(widget=PagedownWidget,required=False)
    Amenities = forms.CharField(widget=PagedownWidget,required=False)
    Precaution_While_Visiting =forms.CharField(widget=PagedownWidget,required=False)
    Tender = forms.FileField(required=False)
    Recruitment = forms.CharField(widget=PagedownWidget,required=False)
    Notice_and_Updates = forms.CharField(widget=PagedownWidget,required=False)
    Website = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Ex: https://www.abc.com,http://www.abc.com '}),required=False)
    Accomodation_Link = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Ex: https://www.abc.com,http://www.abc.com '}),required=False)
    Online_Pooja = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Ex: https://www.abc.com,http://www.abc.com '}),required=False)
    Online_Donation = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Ex: https://www.abc.com,http://www.abc.com '}),required=False)
    Online_Facility = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Ex: https://www.abc.com,http://www.abc.com '}),required=False)
    Live_Darshan_link = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Ex: https://www.abc.com,http://www.abc.com '}),required=False)

    field_groups = (

        {'name':'form1', 'fields':('Display_image', 'Latest_to_be_updated_image','Deity','Contacts', 'Phone_Number', 'Email','Temple_Purohit','City','Address','About_Temple','City')},
        {'name':'form2', 'fields':('Religion', 'Live_Darshan_link','Website','Related_Temple','Related_Faith', 'Temple_History','Significance','Management','Other_Deities', )},
        {'name':'form3', 'fields':('Online_Donation','Online_Pooja', 'Online_Facility','Annakshetra', 'Accomodation_Link','Transportation')},
        {'name':'form4', 'fields':('State', 'Country','About_City', 'How_To_Reach', 'Do_And_Dont', 'Amenities', 'Celebration','Precaution_While_Visiting',)},
        {'name':'form5', 'fields':('Tender', 'Recruitment', 'Notice_and_Updates')},
    )

    class Meta:
            model = Temples
            fields = ('Display_image', 'Latest_to_be_updated_image', 'Religion', 'City', 'State', 'Country', 'Deity', 'Website',
                  'Live_Darshan_link', 'Online_Donation',
                  'Online_Pooja', 'Online_Facility', 'Contacts', 'Phone_Number', 'Email','Temple_Purohit',
                  'Annakshetra', 'Accomodation_Link',
                  'Address','About_Temple',
                  'Temple_History', 'Significance', 'Management',
                  'Related_Faith', 'About_City', 'How_To_Reach', 'Do_And_Dont', 'Amenities', 'Celebration',
                  'Precaution_While_Visiting', 'Tender', 'Recruitment', 'Notice_and_Updates','Related_Temple','Other_Deities','Transportation')
            
class DarshanAddForm(forms.ModelForm):

    rituals = forms.CharField(required=True)
    timings = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Can be of form 7:00 or 7:00-8:00'}),required=True)

    class Meta:
        model = Darshans
        fields = ('rituals', 'timings')

class PictureAddForm(forms.ModelForm):

    def __init__(self,user,*args, **kwargs):
        super(PictureAddForm, self).__init__(*args, **kwargs)

        
        self.fields['Ritual'] = forms.ModelChoiceField(
            queryset=Darshans.objects.filter(user=user),empty_label=None)

    image = forms.ImageField(required=True)
    publish = forms.DateField(widget=SelectDateWidget,required=True)  
    Time = forms.TimeField(widget=forms.TextInput(attrs={'placeholder': 'Time Format:24-Hrs Clock, Ex:7:00 P.M should be 19:00'}),required=True)
    
    class Meta:
        model=Picture
        fields=('image','Time','publish','Ritual')



class PrasadAddForm(forms.ModelForm):
    
    Product_Name = forms.CharField(required=True)
    Price = forms.CharField(required=True)
    is_Prasad = forms.BooleanField(required=True)
    Product_Description = forms.CharField(widget=PagedownWidget,required=True)
    Out_of_Stock = forms.BooleanField(required=False)
    Offer_or_Discount = forms.CharField(required=False)
    class Meta:
        model=Product
        fields = ('Product_Name', 'Out_of_Stock', 'Price', 'Photo','Offer_or_Discount','is_Prasad','Product_Description')


