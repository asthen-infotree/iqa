from io import BytesIO

import qrcode
from django.contrib import admin
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin

from certificate.models import Certificate, Standards, Brand, ProductDescription, Product
from ikramqa import settings
from certificate.views import makeWatermark, render_pdf_view
from django.db.migrations.recorder import MigrationRecorder
from django.contrib import admin



# Register your models here.
class ProductInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        # count = 0
        # print('cd0', self.cleaned_data[0]['certificate'].template)

        for form in self.forms:
            try:
                if form.cleaned_data:
                    # count += 1
                    if form.cleaned_data['certificate'].template == '3' and form.cleaned_data['rmc_producer_code'] == "":
                        raise forms.ValidationError([{'rmc_producer_code':['You must have selected template 3 and rmc producer code \
                        cannot be null!']}])

            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        # if count < 1:
        #     raise forms.ValidationError('You must have at least one order')


class ProductInline(admin.StackedInline):
    model = Product
    readonly_fields = ('id',)
    extra = 0
    show_change_link = True
    verbose_name = "Annex"
    verbose_name_plural = "Annex"
    formset = ProductInlineFormset

class CertAdmin(SummernoteModelAdmin):
    summernote_fields = ('information',)
    # actions = [makeWatermark]
    list_display = ('certificate_no', 'date_original', 'date_renew', 'expire_date',
                    'product_standard', 'status', 'generate_pdf_preview_html')
    exclude_fields = ['qr_image']
    view_on_site = False
    readonly_fields = ('image_tag',)

    def date_original(self, obj):
        return obj.date_original_issue.strftime('%d.%m.%Y')

    def date_renew(self, obj):
        return obj.date_renewal.strftime('%d.%m.%Y')

    def expire_date(self, obj):
        return obj.expiry_date.strftime('%d.%m.%Y')

    def generate_pdf_preview_html(self, obj):
        return format_html('<a class="button" target="_blank" rel="noopener noreferrer" href="/download/%s">Generate '
                           'preview</a> <a class="button" target="_blank" rel="noopener noreferrer" href="%s">QR Code</a>'
                           % (obj.id, obj.qr_image.url))

    generate_pdf_preview_html.short_description = 'Actions'
    date_original.short_description = 'Original Issue Date'
    date_renew.short_description = 'Renewal Date'
    expire_date.short_description = 'Expiry Date'
    generate_pdf_preview_html.allow_tags = True
    date_original.admin_order_field = 'date_original_issue'
    date_renew.admin_order_field = 'date_renewal'
    expire_date.admin_order_field = 'expiry_date'
    date_original.allow_tags = True
    date_renew.allow_tags = True
    expire_date.allow_tags = True

    # def get_urls(self):
    #     urls = super().get_urls()
    #     return urls

    change_list_template = 'admin/custom_change_list.html'
    change_form_template = 'admin/custom_change_form.html'
    inlines = [ProductInline]

    fieldsets = (
        ('Certificate Details', {
               'fields': ('certificate_no', 'certificate_holder', 'holder_address', 'country', 'template', 'status', 'image_tag')
        }),
        ('Dates Info', {
            'fields': ('date_original_issue', 'date_renewal', 'date_amendment', 'expiry_date')
        }),
        ('Product Info', {
            'fields': ('product_name', 'plant_identity','brands', 'product_standard', 'product_description', 'manufacturer', 'manufacturer_address')
        }),
        ('Annex Info', {
            'fields': ('information',)
        }),
        # ('Address info', {
        #     'fields': ('address', ('city', 'zip'))
        # }),
    )

    def get_fieldsets(self, request, obj):
        if obj is None:
            return [
                ('Certificate Details', {
                    'fields': (
                    'certificate_no', 'certificate_holder', 'holder_address', 'country', 'template', 'status',)
                }),
                ('Dates Info', {
                    'fields': ('date_original_issue', 'date_renewal', 'date_amendment', 'expiry_date')
                }),
                ('Product Info', {
                    'fields': ('product_name', 'plant_identity', 'brands', 'product_standard', 'product_description',
                               'manufacturer', 'manufacturer_address')
                }),
                ('Annex Info', {
                    'fields': ('information',)
                }),
            ]
        return self.fieldsets

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id != None:
            extra_context['custom_button'] = True  # Here
        return super().changeform_view(request, object_id, form_url, extra_context)

    # def response_add(self, request, obj, post_url_continue=None):  # Here
    #
    #     if "_custom_button" in request.POST:
    #         # Do something
    #         return super().response_add(request, obj, post_url_continue)
    #     else:
    #         # Do something
    #         return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):  # Here

        if "_custom_button" in request.POST:
            # return render_pdf_view(request, obj)
            return redirect(reverse('download', kwargs={'cert_id':obj.id}))

            # Do something
            # return super().response_change(request, obj)
            # return HttpResponseRedirect(".")
        else:
            # print('123123')
            # Do something
            return super().response_change(request, obj)

    def save_model(self, request, obj, form, change):
        # print('OBJ:', obj.brands.all())
        if not obj.qr_image:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=1,
            )
            super().save_model(request, obj, form, change)
            url=request.build_absolute_uri(obj.get_absolute_url(request))
            qr.add_data(url)
            # print('URL:', obj.get_admin_url(request))
            qr.make(fit=True)
            img = qr.make_image()
            buffer = BytesIO()
            img.save(buffer)
            file_name = f'{obj.certificate_no}-{obj.id}qr.png'
            filebuffer = InMemoryUploadedFile(
                buffer, None, file_name, 'image/png', None, None)
            obj.qr_image.save(file_name, filebuffer, save=False)
        # print('ch',obj.template)
        super().save_model(request, obj, form, change)


admin.site.register(Certificate, CertAdmin)
admin.site.register(Standards)
# admin.site.register(Product)


class ProductDesInline(admin.StackedInline):
    model = ProductDescription
    readonly_fields = ('id',)
    extra = 1
    show_change_link = True


# class ProductDescriptionAdmin(admin.ModelAdmin):
#     inlines=[ProductDesInline]
#     # list_display = ('product', 'brand', 'model', 'rating', 'type', 'size', 'material')

# admin.site.register(Product, ProductDescriptionAdmin)
# admin.site.register(ProductDescription)


class BrandSiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'img_preview']
    readonly_fields = ['img_preview']


admin.site.register(Brand, BrandSiteAdmin)
admin.site.register(MigrationRecorder.Migration)

