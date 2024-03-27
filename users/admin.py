import cities_light
from cities_light.admin import Country, SubRegion, City, Region
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .forms import EditUserForm, ClientAddressForm
from .models import CustomUser, Client, ClientAddress, Manufacturer, ManufacturerAddress

# Register your models here.
admin.site.site_header = "Ikram QA Certification Portal"
admin.site.site_title = "IQA Certification Portal"
admin.site.index_title = "Welcome to Ikram QA Certification Portal"


class BaseReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AccountAdmin(UserAdmin):
    list_display = ('email', '_get_full_name', 'date_joined', 'last_login')

    # form = EditUserForm

    # def show_url(self, instance):
    #     url = reverse("admin:users_customuser_change", args=[instance.id])
    #     return mark_safe(f'<a href="{url}" target="_blank" rel="nofollow"">Follow</a>')

    def _get_full_name(self, obj):
        return obj.get_full_name()

    _get_full_name.short_description = 'Name'


# admin.site.unregister(Group)
admin.site.unregister(Country)
admin.site.unregister(City)
admin.site.unregister(SubRegion)
admin.site.unregister(Region)
admin.site.register(Client)


# class ClientAddressAdmin(admin.ModelAdmin):
#     form = ClientAddressForm


admin.site.register(ClientAddress)
admin.site.register(Manufacturer)
# admin.site.register(ManufacturerAddress)
admin.site.register(CustomUser, AccountAdmin)

@admin.register(ManufacturerAddress)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("manufacturer", "address", "address2", 'address3', 'postcode', 'city')