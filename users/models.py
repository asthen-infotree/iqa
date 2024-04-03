from cities_light.models import City
from django.contrib.auth.models import AbstractUser
from dal import autocomplete
from django.db import models
from django.utils.html import format_html


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return City.objects.none()

        qs = City.objects.all()

        country = self.forwarded.get('country', None)

        if country:
            qs = qs.filter(country=country)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


# Create your models here.
class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Client(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.name


class ClientAddress(models.Model):

    STATUS_CHOICES = (
        ("1", "ACTIVE"),
        ("2", "NOT ACTIVE"),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    address = models.TextField(max_length=255)
    address2 = models.TextField(max_length=255, blank=True)
    address3 = models.TextField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True,null=True)
    postcode = models.IntegerField()
    country = models.CharField(max_length=255, blank=True,null=True)
    status = models.CharField(default='1', max_length=1, choices=STATUS_CHOICES)

    class Meta:
        verbose_name_plural = "Client Addresses"

    # widgets = {
    #     'city': autocomplete.ModelSelect2(url='city-autocomplete')
    # }

    # def __str__(self):
    #     return self.client.name + ', ' + self.address + ', ' + self.address2 + ', ' + self.address3 + ', ' + str(self.postcode) + ', ' + str(self.city)

    def __str__(self):
        full_address=[self.client.name, self.address, self.address2, self.address3, self.city, self.postcode, self.state]
        new_full_address=''
        for field in full_address:
            if field is not None and field != "":
                new_full_address+=str(field)+"<br/>"
        return format_html(new_full_address)
        # return format_html(
        #      "{} <br/> {} <br/> {} <br/> {} <br/> {} <br/> {} <br/> {} <br/>", self.client.name, self.address, self.address2,
        #     self.address3, self.city, self.postcode, self.state
        # )

class Manufacturer(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Manufacturer"

    def __str__(self):
        return self.name


class ManufacturerAddress(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    address = models.TextField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    address3 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.IntegerField()
    # country = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Manufacturer Addresses"

    def __str__(self):
        full_address = [self.manufacturer.name, self.address, self.address2, self.address3, self.city, self.postcode,
                        self.state]
        new_full_address = ''
        for field in full_address:
            if field is not None and field != "":
                new_full_address += str(field) + "<br/>"
        return format_html(new_full_address)
        # return format_html(
        #     "{} <br/> {} <br/> {} <br/> {} <br/> {} <br/> {} <br/> {} <br/>", self.manufacturer.name, self.address, self.address2,
        #     self.address3, self.city, self.postcode, self.state
        # )


class Licensee(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class LicenseeAddress(models.Model):
    licensee = models.ForeignKey(Licensee, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, null=True)
    address3 = models.CharField(max_length=255, null=True)
    postcode = models.IntegerField()
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.licensee

