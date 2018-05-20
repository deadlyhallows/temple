from django import forms
from .models import Profile,Temples, Mobile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_select2.forms import (Select2MultipleWidget,
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
    OPTIONS = []
    a = Temples.objects.all()
    for x in a:
        y=(x.temple2, x.temple2)
        OPTIONS.append(y)
    Temple1 =forms.MultipleChoiceField(
            widget=Select2MultipleWidget(),
            required=True,
            choices=OPTIONS
            )

    class Meta:
        model=Profile
        fields = ('Temple1',)






