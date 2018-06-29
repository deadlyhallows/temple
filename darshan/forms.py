from django import forms
from .models import Profile, Temples, Mobile, OnlineDonation, TempleManager, Picture, Darshans
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from pagedown.widgets import PagedownWidget
from django.forms.extras.widgets import SelectDateWidget

from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email',)

    def __init__(self, *args, **kwargs):

        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            username="username"
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {'class': 'has-popover', 'data-content': help_text, 'data-placement': 'right',
                     'data-container': 'body'})
                self.fields[username].widget.attrs.update(
                    {'id': username})    

  


class MobileForm(forms.ModelForm):
    class Meta:
        model = Mobile
        fields = ('Mobile_No',)

    

class TempleForm(forms.ModelForm):

    #comment it while migration
    OPTIONS = []
    Tem = Temples.objects.all()
    for x in Tem:
        tem_option = (x.temple2, x.temple2)
        OPTIONS.append(tem_option)

    Select_Temple = forms.MultipleChoiceField(
        widget=Select2MultipleWidget(),

        # queryset=Temples.objects.all()
        choices=OPTIONS

    )

    class Meta:
        model = Profile
        fields = ('Select_Temple',)


class DonationForm(forms.ModelForm):
    class Meta:
        model = OnlineDonation
        fields = ('Amount', 'Purpose',)


class TempleManagerForm(forms.ModelForm):
    class Meta:
        model = TempleManager
        fields = ('Temple_Name',)


class TempleAddForm(forms.ModelForm):
    Icon_images = forms.ImageField(required=True)
    images = forms.ImageField(required=True)
    Deity = forms.CharField(max_length=200,required=True)
    City = forms.CharField(max_length=200,required=True)
    About_Temple = forms.CharField(widget=PagedownWidget(),required=True)
    Contacts = forms.CharField(max_length=200,required=True)
    Phone_Number = forms.CharField(max_length=200,required=True)
    Temple_Purohit = forms.CharField(max_length=200,required=True)
    Address = forms.CharField(widget=PagedownWidget(),required=True)
    Religion = forms.CharField(max_length=200,required=False)
    Management= forms.CharField(widget=PagedownWidget(),required=False)
    Related_Faith= forms.CharField(widget=PagedownWidget(),required=False)
    Temple_History= forms.CharField(widget=PagedownWidget(),required=False)
    Significance= forms.CharField(widget=PagedownWidget(),required=False)
    Other_Deities= forms.CharField(widget=PagedownWidget(),required=False)
    Related_Temple = forms.CharField(widget=PagedownWidget(),required=False)
    Celebration = forms.CharField(widget=PagedownWidget(),required=False)
    Transportation = forms.CharField(widget=PagedownWidget(),required=False)
    State = forms.CharField(max_length=200,required=False)
    Country = forms.CharField(max_length=200,required=False)
    About_City = forms.CharField(widget=PagedownWidget(),required=False)
    How_To_Reach = forms.CharField(widget=PagedownWidget(),required=False)
    Do_And_Dont = forms.CharField(widget=PagedownWidget(),required=False)
    Amenities = forms.CharField(widget=PagedownWidget(),required=False)
    Precaution_While_Visiting =forms.CharField(widget=PagedownWidget(),required=False)
    Tender = forms.FileField(required=False)
    Recruitment = forms.CharField(widget=PagedownWidget(),required=False)
    Notice_and_Updates = forms.CharField(widget=PagedownWidget(),required=False)

    field_groups = (
        {'name':'form1', 'fields':('Icon_images', 'images','Deity','Contacts', 'Phone_Number', 'Email','Temple_Purohit','City','Address','About_Temple','City')},
        {'name':'form2', 'fields':('Religion', 'Live_Darshan_link','Website','Related_Temple','Related_Faith', 'Temple_History','Significance','Management','Other_Deities', )},
        {'name':'form3', 'fields':('Online_Donation','Online_Pooja', 'Online_Facility','Annakshetra', 'Accomodation_Link','Transportation')},
        {'name':'form4', 'fields':('State', 'Country','About_City', 'How_To_Reach', 'Do_And_Dont', 'Amenities', 'Celebration','Precaution_While_Visiting',)},
        {'name':'form5', 'fields':('Tender', 'Recruitment', 'Notice_and_Updates')},
    )

    class Meta:
            model = Temples
            fields = ('Icon_images', 'images', 'Religion', 'City', 'State', 'Country', 'Deity', 'Website',
                  'Live_Darshan_link', 'Online_Donation',
                  'Online_Pooja', 'Online_Facility', 'Contacts', 'Phone_Number', 'Email','Temple_Purohit',
                  'Annakshetra', 'Accomodation_Link',
                  'Address','About_Temple',
                  'Temple_History', 'Significance', 'Management',
                  'Related_Faith', 'About_City', 'How_To_Reach', 'Do_And_Dont', 'Amenities', 'Celebration',
                  'Precaution_While_Visiting', 'Tender', 'Recruitment', 'Notice_and_Updates','Related_Temple','Other_Deities','Transportation')
            
class DarshanAddForm(forms.ModelForm):
    rituals = forms.CharField(required=True)
    timings = forms.CharField(required=True)

    class Meta:
        model = Darshans
        fields = ('rituals', 'timings')

class PictureAddForm(forms.ModelForm):
    OPTION = []
    darshans = Darshans.objects.all()
    for x in darshans:
        darshan_option = (str(x.rituals), str(x.rituals))
        OPTION.append(darshan_option)
    image = forms.ImageField(required=True)
    publish = forms.DateField(widget=SelectDateWidget,required=True)  
    Time = forms.CharField(max_length=250)
    Ritual = forms.ChoiceField(choices=OPTION)
    print("Ritual", Ritual)
    class Meta:
        model=Picture
        fields=('image','Time','publish','Ritual')




# class UserTypeForm(forms.Form):

#   CHOICES = (
#      ('seller', 'Seller'),
#     ('user', 'User'),
# )
# choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
