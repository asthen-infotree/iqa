from datetime import datetime, timedelta, timezone
from io import BytesIO, StringIO
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage as storage
from PIL import Image as Img
import io
from django.core.files.uploadhandler import InMemoryUploadedFile

from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_countries.fields import CountryField

from users.models import Client, ClientAddress, Manufacturer, ManufacturerAddress


# Create your models here.
class Standards(models.Model):
    standard = models.CharField(max_length=255)
    standard_number = models.CharField(max_length=255)
    year = models.CharField(max_length=50)
    standard_name = models.CharField(max_length=255)
    remark = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return self.standard + ' ' + self.standard_number + ' ' + self.year

    class Meta:
        verbose_name_plural = "Standards"


class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.name

    def img_preview(self):  # new
        return mark_safe(f'<img src = "{self.logo.url}" width = "50"/>')

    def save(self):
        if self.logo:
            im = Img.open(io.BytesIO(self.logo.read()))
            x, y = im.size

            ratio = x / y
            desired_ratio = 80 / 45

            w = max(80, x)
            h = int(w / desired_ratio)
            if h < y:
                h = y
                w = int(h * desired_ratio)

            new_im = Img.new('RGBA', (w, h), (255, 255, 255))
            new_im.paste(im, ((w - x) // 2, (h - y) // 2))
            new_im.resize((80, 45))
            output = io.BytesIO()
            new_im.save(output, format='PNG')
            output.seek(0)
            self.logo = InMemoryUploadedFile(output, 'ImageField', "%s.png"
                                              % self.logo.name.split('.')[0], 'image/png', "Content-Type: charset = utf-8", None)
            super(Brand, self).save()


def one_year_hence():
    return datetime.now() + timedelta(days=365)


# class Product(models.Model):
#     product_name=models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.product_name


# class ProductDescription(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     brand=models.CharField(max_length=255)
#     model=models.CharField(max_length=255)
#     rating=models.CharField(max_length=255)
#     type=models.CharField(max_length=255)
#     size=models.CharField(max_length=255)
#     material=models.CharField(max_length=255, null=True, blank=True)
#     additional_info=models.TextField(max_length=255, null=True, blank=True)
#
#     def save(
#         self, force_insert=False, force_update=False, using=None, update_fields=None
#     ):
#         self.brand = self.brand.upper()
#         self.model = self.model.upper()
#         self.rating = self.rating.upper()
#         self.type = self.type.upper()
#         self.size = self.size.upper()
#         if self.material:
#             self.material = self.material.upper()
#         if self.additional_info:
#             self.additional_info = self.additional_info.upper()
#         super(ProductDescription, self).save()
#
#     def __str__(self):
#         return self.product.product_name


class Certificate(models.Model):
    STATUS_CHOICES = (
        ("1", "DRAFT"),
        ("2", "PUBLISHED"),
        ("3", "EXPIRED"),
    )

    TEMPLATE_CHOICES = (
        ("1", "TEMPLATE 1"),
        ("2", "TEMPLATE 2"),
        ("3", "TEMPLATE 3"),
        ("4", "TEMPLATE 4"),
    )

    certificate_no = models.CharField(max_length=30)
    template = models.CharField(default='1', max_length=1, choices=TEMPLATE_CHOICES)
    date_original_issue = models.DateField()
    date_renewal = models.DateField()
    date_amendment = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    certificate_holder = models.ForeignKey(Client, on_delete=models.CASCADE)
    holder_address = models.ForeignKey(ClientAddress, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    plant_identity = models.CharField(max_length=255, blank=True, null=True)
    # product=models.ForeignKey(Product,null=True, blank=True, on_delete=models.CASCADE)
    product_standard = models.ForeignKey(Standards, on_delete=models.CASCADE)
    product_description = models.TextField()
    brands = models.ManyToManyField(Brand, blank=True)
    country = CountryField(default='MY')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    manufacturer_address = models.ForeignKey(ManufacturerAddress, on_delete=models.CASCADE)
    # annex = models.TextField(blank=True)
    information = models.TextField(blank=True)
    status = models.CharField(default='1', max_length=1, choices=STATUS_CHOICES)
    # test = models.CharField(default='ac', max_length=3)
    qr_image = models.ImageField(blank=True, null=True, upload_to='QRCode/')

    def __str__(self):
        return self.certificate_no

        # save method

    def get_admin_url(self, request):
        return request.build_absolute_uri(
            reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,)))

    def get_absolute_url(self,request):
        return reverse('product_detail', args=[str(self.id)])

    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % (self.qr_image.url))

    image_tag.short_description = 'Image'

    # def clean(self):
    #     cleaned_data = super().clean()
    #     print('cd', cleaned_data)
    #     if self.template == "3" and self.product.rmc_producer_code is None:
    #         raise ValidationError(_("Error"))


class Product(models.Model):
    # product_name=models.CharField(max_length=255)
    certificate = models.ForeignKey(Certificate, null=True, blank=True, on_delete=models.CASCADE)
    brand = models.CharField(blank=True, null=True, max_length=255)
    model = models.TextField(null=True, blank=True)
    rating = models.TextField(null=True, blank=True)
    type = models.TextField(null=True, blank=True)
    size = models.TextField(null=True, blank=True)
    material = models.TextField(null=True, blank=True)
    rmc_producer_code=models.TextField("Ready-Mixed Concrete Producer's Code", null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.brand


class ProductDescription(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    rating = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    material = models.CharField(max_length=255, null=True, blank=True)
    additional_info = models.TextField(max_length=255, null=True, blank=True)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.brand = self.brand.upper()
        self.model = self.model.upper()
        self.rating = self.rating.upper()
        self.type = self.type.upper()
        self.size = self.size.upper()
        if self.material:
            self.material = self.material.upper()
        if self.additional_info:
            self.additional_info = self.additional_info.upper()
        super(ProductDescription, self).save()

    def __str__(self):
        return self.product.brand

