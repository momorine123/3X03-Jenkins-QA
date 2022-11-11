from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from django.forms import ModelForm, TextInput
from .models import CustomUser, Inventory, Items
from django.contrib import messages


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username','role','hospital')

    def save(self,commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username','role','hospital')
        exclude = ['slug']

class CustomChangeFormPassword(SetPasswordForm):
    class Meta:
        model = CustomUser
        fields = ['new_password1', 'new_password2']


class addItemForm(ModelForm):
    class Meta:
        model = Items
        exclude = ['slug']

class managerItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(managerItemForm, self).__init__(*args, **kwargs)
        self.fields['item'].disabled = True
    class Meta:
        model = Inventory
        exclude = ['hospital', 'status']
        # fields = '__all__'


class UnlockUsernameForm(forms.Form):
    username_to_unlock = forms.CharField(max_length=50)


class UnlockIPForm(forms.Form):
    ip_to_unlock = forms.CharField( max_length=50)