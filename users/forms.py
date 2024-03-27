from dal import autocomplete
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ModelForm, PasswordInput

from users.models import CustomUser, ClientAddress


class EditUserForm(ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_password(self):
        return self.initial["password"]


# class UserChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = User
#         fields = ('email', 'password', 'date_of_birth',
#                   'is_active', 'is_admin')
#
#     def clean_password(self):
#         return self.initial["password"]

class ClientAddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(ClientAddressForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ClientAddress
        fields = '__all__'
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete', forward=['country'])
        }

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if city and city.country != self.cleaned_data.get('country'):
            raise forms.ValidationError("Invalid city for this country!")

        return city

