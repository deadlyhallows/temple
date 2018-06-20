from django import forms
from .models import Profile, Temples, Mobile, OnlineDonation, TempleManager, Picture, Darshans
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from pagedown.widgets import PagedownWidget
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
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {'class': 'has-popover', 'data-content': help_text, 'data-placement': 'right',
                     'data-container': 'body'})
# is_verified = forms.BooleanField(initial=False)
class MobileForm(forms.ModelForm):
    class Meta:
        model = Mobile
        fields = ('Mobile_No',)

    def __init__(self, *args, **kwargs):

        super(MobileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {'class': 'has-popover', 'data-content': help_text, 'data-placement': 'right',
                     'data-container': 'body'})


class TempleForm(forms.ModelForm):
    #comment it while migration
    OPTIONS = []
    a = Temples.objects.all()
    for x in a:
        y=(x.temple2, x.temple2)
        OPTIONS.append(y)

    Select_Temple =forms.MultipleChoiceField(
            widget=Select2MultipleWidget(),

            # queryset=Temples.objects.all()
            choices=OPTIONS
            )

    class Meta:
        model=Profile
        fields = ('Select_Temple',)

class DonationForm(forms.ModelForm):
    class Meta:
        model=OnlineDonation
        fields=('Amount','Purpose',)

class TempleManagerForm(forms.ModelForm):
    class Meta:
        model=TempleManager
        fields=('Temple_Name',)


class TempleAddForm(forms.ModelForm):
    Address = forms.CharField(widget=PagedownWidget(show_preview=False))
    AboutTemple = forms.CharField(widget=PagedownWidget(show_preview=False))
    TempleHistory= forms.CharField(widget=PagedownWidget(show_preview=False))
    Significance= forms.CharField(widget=PagedownWidget(show_preview=False))
    Management= forms.CharField(widget=PagedownWidget(show_preview=False))
    RelatedFaith= forms.CharField(widget=PagedownWidget(show_preview=False))
    AboutCity = forms.CharField(widget=PagedownWidget(show_preview=False))
    HowToReach = forms.CharField(widget=PagedownWidget(show_preview=False))
    DoAndDont = forms.CharField(widget=PagedownWidget(show_preview=False))
    Amenities = forms.CharField(widget=PagedownWidget(show_preview=False))
    Celebration = forms.CharField(widget=PagedownWidget(show_preview=False))
    PrecautionWhileVisiting = forms.CharField(widget=PagedownWidget(show_preview=False))
    Tender = forms.CharField(widget=PagedownWidget(show_preview=False))
    Recruitment = forms.CharField(widget=PagedownWidget(show_preview=False))
    NoticeandUpdates = forms.CharField(widget=PagedownWidget(show_preview=False))
    class Meta:
        model=Temples
        fields = ('Iconimages','images','Religion','City','State','Country','Deity','Website','LiveDarshan','LiveDarshanlink','OnlinePrasadStatus','OnlineDonation'
        ,'LivePooja', 'OnlinePooja','OnlinePrasadStatus','OtherOnlineFacilityStatus','OnlineFacility','Contacts','PhoneNumber','Email','Accomodation','AccomodationLink','Annakshetra','TemplePurohit','Address','AboutTemple','TempleHistory'
        ,'Significance','Management','RelatedFaith','AboutCity','HowToReach','DoAndDont','Amenities','Celebration','PrecautionWhileVisiting','Tender','Recruitment','NoticeandUpdates'
         )


class PictureAddForm(forms.ModelForm):
    class Meta:
        model=Picture
        fields=('image','TimeD','publish')



class DarshanAddForm(forms.ModelForm):
    class Meta:
        model=Darshans
        fields=('rituals','timings')

#class UserTypeForm(forms.Form):
   
 #   CHOICES = (
  #      ('seller', 'Seller'),
   #     ('user', 'User'),
   # )
    #choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())



