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
    # # comment it while migration
    # OPTIONS = []
    # a = Temples.objects.all()
    # for x in a:
    #     y = (x.temple2, x.temple2)
    #     OPTIONS.append(y)

    Select_Temple = forms.ModelMultipleChoiceField(
        widget=Select2MultipleWidget(),

        queryset=Temples.objects.all()
        # choices=OPTIONS
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
    Religion = forms.CharField(max_length=200,required=True)
    City = forms.CharField(max_length=200,required=True)
    State = forms.CharField(max_length=200,required=True)
    Country = forms.CharField(max_length=200,required=True)
    Deity = forms.CharField(max_length=200,required=True)
    Contacts = forms.CharField(max_length=200,required=True)
    Phone_Number = forms.CharField(max_length=200,required=True)
    Temple_Purohit = forms.CharField(max_length=200,required=True)
    Address = forms.CharField(widget=PagedownWidget(show_preview=False),required=True)
    About_Temple = forms.CharField(widget=PagedownWidget(show_preview=False),required=True)
    Temple_History= forms.CharField(widget=PagedownWidget(show_preview=False),required=True)
    Significance= forms.CharField(widget=PagedownWidget(show_preview=False),required=True)
    Management= forms.CharField(widget=PagedownWidget(show_preview=False),required=True)
    Related_Faith= forms.CharField(widget=PagedownWidget(show_preview=False),required=True)
    About_City = forms.CharField(widget=PagedownWidget(show_preview=False),required=True)
    How_To_Reach = forms.CharField(widget=PagedownWidget(show_preview=False),required=True)
    Do_And_Dont = forms.CharField(widget=PagedownWidget(show_preview=False),required=True)
    Amenities = forms.CharField(widget=PagedownWidget(show_preview=False),required=True)
    Celebration = forms.CharField(widget=PagedownWidget(show_preview=False),required=True)
    Precaution_While_Visiting = forms.CharField(widget=PagedownWidget(show_preview=False),required=True)
    Tender = forms.CharField(widget=PagedownWidget(show_preview=False),required=False)
    Recruitment = forms.CharField(widget=PagedownWidget(show_preview=False),required=True)
    Notice_and_Updates = forms.CharField(widget=PagedownWidget(show_preview=False),required=True)
    class Meta:
        model = Temples
        fields = ('Icon_images', 'images', 'Religion', 'City', 'State', 'Country', 'Deity', 'Website',
                  'Live_Darshan_link', 'Online_Donation',
                  'Online_Pooja', 'Online_Facility', 'Contacts', 'Phone_Number', 'Email','Temple_Purohit',
                  'Annakshetra', 'Accomodation_Link',
                  'Address','About_Temple',
                  'Temple_History', 'Significance', 'Management',
                  'Related_Faith', 'About_City', 'How_To_Reach', 'Do_And_Dont', 'Amenities', 'Celebration',
                  'Precaution_While_Visiting', 'Tender', 'Recruitment', 'Notice_and_Updates')


class PictureAddForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    publish = forms.DateField(widget=SelectDateWidget,required=True)  
    Time = forms.TimeField(required=True)
    class Meta:
        model=Picture
        fields=('image','Time','publish')



class DarshanAddForm(forms.ModelForm):
    rituals = forms.CharField(required=True)
    timings = forms.CharField(required=True)

    class Meta:
        model = Darshans
        fields = ('rituals', 'timings')

# class UserTypeForm(forms.Form):

#   CHOICES = (
#      ('seller', 'Seller'),
#     ('user', 'User'),
# )
# choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
