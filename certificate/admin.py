from datetime import datetime
from io import BytesIO

from django.db.models import Max
from django.db.models.functions import Coalesce
from django.forms import widgets, BaseInlineFormSet
import qrcode
from adminsortable2.admin import SortableStackedInline, SortableAdminBase
from django.contrib import admin, messages
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.migrations.recorder import MigrationRecorder
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin
from certificate.forms import AutocompleteForm
from certificate.models import Certificate, Standards, Brand, ProductDescription, Product, PublishCertificate, \
    PublishProduct
from ikramqa import settings
from certificate.views import makeWatermark, render_pdf_view, publish_certificate


# Register your models here.
# class ProductInlineFormset(forms.models.BaseInlineFormSet):
class CustomInlineFormSetMixin:
    def __init__(self, default_order_direction=None, default_order_field=None, **kwargs):
        self.default_order_direction = default_order_direction
        self.default_order_field = default_order_field
        if default_order_field:
            if default_order_field in self.form.base_fields:
                print('default_order_field', default_order_field)
                order_field = self.form.base_fields[default_order_field]
            else:
                order_field = self.model._meta.get_field(default_order_field).formfield()
                self.form.base_fields[default_order_field] = order_field
                self.form.declared_fields[default_order_field] = order_field

            order_field.is_hidden = False
            order_field.required = False
            order_field.widget = widgets.NumberInput(attrs={'class': '_reorder_'})

        super().__init__(**kwargs)

    def get_max_order(self):
        query_set = self.model.objects.filter(
            **{self.fk.get_attname(): self.instance.pk}
        )
        return query_set.aggregate(
            max_order=Coalesce(Max(self.default_order_field), 0)
        )['max_order']

    def save_new(self, form, commit=True):
        """
        New objects do not have a valid value in their ordering field.
        On object save, add an order bigger than all other order fields
        for the current parent_model.
        Strange behaviour when field has a default, this might be evaluated
        on new object and the value will be not None, but the default value.
        """
        obj = super().save_new(form, commit=False)

        order_field_value = getattr(obj, self.default_order_field, None)
        if order_field_value is None or order_field_value >= 0:
            max_order = self.get_max_order()
            setattr(obj, self.default_order_field, max_order + 1)
        if commit:
            obj.save()
        # form.save_m2m() can be called via the formset later on
        # if commit=False
        if commit and hasattr(form, 'save_m2m'):
            form.save_m2m()
        return obj


class ProductInlineFormset(CustomInlineFormSetMixin,BaseInlineFormSet):

    def clean(self):
        # get forms that actually have valid data
        # count = 0
        # print('cd0', self.cleaned_data[0]['certificate'].template)

        for form in self.forms:
            try:
                if form.cleaned_data:
                    # count += 1
                    if form.cleaned_data['certificate'].template == '3' and form.cleaned_data[
                        'rmc_producer_code'] == "":
                        raise forms.ValidationError([{'rmc_producer_code': ['You must have selected template 3 and rmc producer code \
                        cannot be null!']}])

            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        # if count < 1:
        #     raise forms.ValidationError('You must have at least one order')


# class ProductInline(admin.StackedInline):
class ProductInline(SortableStackedInline):
    model = Product
    readonly_fields = ('id',)
    # ordering = ['order']

    extra = 0
    show_change_link = True
    verbose_name = "Annex"
    verbose_name_plural = "Annex"
    formset = ProductInlineFormset


class PublishProductInlineFormset(forms.models.BaseInlineFormSet):
    pass
    # def clean(self):
        # get forms that actually have valid data
        # count = 0
        # print('cd0', self.cleaned_data[0]['certificate'].template)
        # print('forms', self.forms)
        ## comment out for copy files
        # for form in self.forms:
        #     try:
        #         if form.cleaned_data:
        #             # count += 1
        #             if form.cleaned_data['certificate'].template == '3' and form.cleaned_data[
        #                 'rmc_producer_code'] == "":
        #                 raise forms.ValidationError([{'rmc_producer_code': ['You must have selected template 3 and rmc producer code \
        #                 cannot be null!']}])
        #
        #     except AttributeError:
        #         # annoyingly, if a subform is invalid Django explicity raises
        #         # an AttributeError for cleaned_data
        #         pass

        # if count < 1:
        #     raise forms.ValidationError('You must have at least one order')


class PublishProductInline(admin.StackedInline):
    model = PublishProduct
    exclude = ['order']
    readonly_fields = [f.name for f in model._meta.fields if f.name != 'order']
    ordering = ('id',)
    can_delete = False
    extra = 0
    show_change_link = True
    verbose_name = "Annex"
    verbose_name_plural = "Annex"
    formset = PublishProductInlineFormset


class CertAdmin(SortableAdminBase, SummernoteModelAdmin):
    # change_list_template = 'admin/custom_change_list.html'
    # change_form_template = 'admin/custom_change_form.html'
    change_form_template = "admin/custom_change_form.html"

    search_fields = ['certificate_no', 'certificate_holder__name']
    summernote_fields = ('information',)
    # autocomplete_fields = ['manufacturer', 'certificate_holder', 'manufacturer_address', 'holder_address']
    # actions = [makeWatermark]
    list_display = ('certificate_no', 'date_original', 'date_renew', 'expire_date',
                    'short_product_standard', 'status', 'generate_pdf_preview_html')
    exclude_fields = ['qr_image', 'image_tag']
    view_on_site = False
    readonly_fields = ('image_tag', 'publish_date')
    form = AutocompleteForm

    # temporary removed image_tag

    def short_product_standard(self, obj):
        if len(str(obj.product_standard)) > 26:
            return str(obj.product_standard)[:25] + '...'
        else:
            return str(obj.product_standard)

    def date_original(self, obj):
        if obj.date_original_issue != None:
            return obj.date_original_issue.strftime('%d.%m.%Y')
        else:
            return ""

    def date_renew(self, obj):
        if obj.date_renewal != None:
            return obj.date_renewal.strftime('%d.%m.%Y')
        else:
            return ""

    def expire_date(self, obj):
        if obj.expiry_date != None:
            return obj.expiry_date.strftime('%d.%m.%Y')
        else:
            return ""

    def generate_pdf_preview_html(self, obj):
        # return format_html(
        #     '<a class="button" target="_blank" rel="noopener noreferrer" href="/cert/download/%s">Generate '
        #     'preview</a> <a class="button" target="_blank" rel="noopener noreferrer" href="%s">QR Code</a>'
        #     % (obj.id, obj.qr_image.url))

        return format_html(
            '<a class="button" target="_blank" rel="noopener noreferrer" href="/cert/download/%s">Generate '
            'preview</a>'
            % (obj.id))

    short_product_standard.short_description = "Product Standard"
    generate_pdf_preview_html.short_description = 'Actions'
    date_original.short_description = 'Original Issue Date'
    date_renew.short_description = 'Renewal Date'
    expire_date.short_description = 'Expiry Date'
    # expire_date.short_description = 'Last Publish Date'
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
            'fields': (
            'certificate_no', 'certificate_holder', 'holder_address', 'country', 'template', 'status')
        }),
        ('Dates Info', {
            'fields': ('date_original_issue', 'date_renewal', 'date_amendment', 'expiry_date', 'publish_date')
        }),
        ('Product Info', {
            'fields': (
            'product_name', 'plant_identity', 'brands', 'product_standard', 'product_description', 'manufacturer',
            'manufacturer_address')
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
                    'fields': ('date_original_issue', 'date_renewal', 'date_amendment', 'expiry_date', 'publish_date')
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
        from urllib.parse import quote as urlquote
        from django.utils.translation import gettext as _
        if "_custom_button" in request.POST:
            # return render_pdf_view(request, obj)
            if request.POST.get('_custom_button') == 'Download':
                return redirect(reverse('download', kwargs={'cert_id': obj.id}))
            elif request.POST.get('_custom_button') == 'Publish':
                print('here')
                opts = obj._meta
                link = publish_certificate(request, obj)

                msg_dict = {
                    "name": opts.verbose_name,
                    "obj": format_html('<a href="{}">{}</a>',link, obj),
                }
                msg = format_html(
                    _(
                        "The {name} “{obj}” was publish successfully."
                    ),
                    **msg_dict,
                )
                self.message_user(request, msg, messages.SUCCESS)


                obj.publish_date = datetime.now()
                obj.save()
                # return
                redirect_url = request.path
                return HttpResponseRedirect(redirect_url)

            # Do something
            # return super().response_change(request, obj)
            # return HttpResponseRedirect(".")
        else:
            # print('123123')
            # Do something
            return super().response_change(request, obj)

    # def save_model(self, request, obj, form, change):
    #     # print('OBJ:', obj.brands.all())
    #     if not obj.qr_image:
    #         qr = qrcode.QRCode(
    #             version=1,
    #             error_correction=qrcode.constants.ERROR_CORRECT_L,
    #             box_size=6,
    #             border=1,
    #         )
    #         super().save_model(request, obj, form, change)
    #         url = request.build_absolute_uri(obj.get_absolute_url(request))
    #         qr.add_data(url)
    #         # print('URL:', obj.get_admin_url(request))
    #         qr.make(fit=True)
    #         img = qr.make_image()
    #         buffer = BytesIO()
    #         img.save(buffer)
    #         file_name = f'{obj.certificate_no}-{obj.id}qr.png'
    #         filebuffer = InMemoryUploadedFile(
    #             buffer, None, file_name, 'image/png', None, None)
    #         obj.qr_image.save(file_name, filebuffer, save=False)
    #     # print('ch',obj.template)
    #     super().save_model(request, obj, form, change)


admin.site.register(Certificate, CertAdmin)


class StandardAdmin(admin.ModelAdmin):
    search_fields = ['standard', 'standard_number', 'year']


admin.site.register(Standards, StandardAdmin)
admin.site.register(Product)


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


class PublishCertAdmin(admin.ModelAdmin):
    change_form_template = "admin/custom_change_form.html"
    change_list_template = "admin/custom_change_list.html"

    search_fields = ['certificate_no', 'certificate_holder__name']
    # summernote_fields = ('information',)
    # autocomplete_fields = ['manufacturer', 'certificate_holder', 'manufacturer_address', 'holder_address']
    # actions = [makeWatermark]
    list_display = ('certificate_no', 'expiry_date',
                    'status')
    # exclude_fields = ['qr_image']
    view_on_site = False
    # fields = ('image_tag',)

    def image_tag(self, request):
        return mark_safe('<img src="%s" width="150" height="150" />' % (request.qr_image.url))

    image_tag.short_description = 'Image'

    def get_readonly_fields(self, request, obj=None):
        # print('ro fields', [f.name for f in self.model._meta.fields if f.name != 'information'] + [field.name for field in obj._meta.many_to_many])
        return [f.name for f in self.model._meta.fields] + [field.name for field in obj._meta.many_to_many] + [
            'image_tag']

    inlines = [PublishProductInline]

    # def has_change_permission(self, request, obj=None):
    #     return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}

        if object_id != None:
            extra_context = dict(show_save=False, show_save_and_continue=False, show_delete=False, show_save_and_add_another=False)
            extra_context['custom_button_publish'] = True  # Here
        return super().changeform_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):  # Here

        if "_custom_button" in request.POST:
            # return render_pdf_view(request, obj)
            return HttpResponseRedirect(reverse('publish_download', kwargs={'cert_id': obj.id}))
            # Do something

        else:
            # Do something
            return super().response_change(request, obj)

    fieldsets = (
        ('Certificate Details', {
            'fields': (
                'certificate_no', 'certificate_holder', 'holder_address', 'country', 'template', 'status','image_tag')
        }),
        ('Dates Info', {
            'fields': ('date_original_issue', 'date_renewal', 'date_amendment', 'expiry_date')
        }),
        ('Product Info', {
            'fields': (
                'product_name', 'plant_identity', 'brands', 'product_standard', 'product_description', 'manufacturer',
                'manufacturer_address')
        }),
        ('Annex Info', {
            'fields': ('information',)
        }),
    )

admin.site.register(PublishCertificate, PublishCertAdmin)


# class PublishProductAdmin(admin.ModelAdmin):
#     list_display = ('certificate', 'brand')
#
#
# admin.site.register(PublishProduct, PublishProductAdmin)
