from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelect

from certificate.models import Certificate, PublishCertificate


class MyForm(forms.ModelForm):
    class Meta:
        widgets = {
            'manufacturer_address': AutocompleteSelect(
                Certificate._meta.get_field('manufacturer_address'),
                admin.site,
                attrs={'data-dropdown-auto-width': 'true'}
            ),
            'manufacturer': AutocompleteSelect(
                Certificate._meta.get_field('manufacturer'),
                admin.site,
                attrs={'data-dropdown-auto-width': 'true'}
            ),
            'holder_address': AutocompleteSelect(
                Certificate._meta.get_field('holder_address'),
                admin.site,
                attrs={'data-dropdown-auto-width': 'true'}
            ),
            'certificate_holder': AutocompleteSelect(
                Certificate._meta.get_field('certificate_holder'),
                admin.site,
                attrs={'data-dropdown-auto-width': 'true'}
            ),
            'product_standard': AutocompleteSelect(
                Certificate._meta.get_field('product_standard'),
                admin.site,
                attrs={'data-dropdown-auto-width': 'true'}
            ),
        }
