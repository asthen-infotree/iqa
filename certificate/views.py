import os

import PyPDF2
import qrcode
from io import BytesIO
from django.db import transaction
from django.contrib.staticfiles import finders
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfFileReader, PdfFileWriter
from xhtml2pdf import pisa
from xhtml2pdf.files import pisaFileObject

from certificate.models import Certificate, PublishCertificate, Product, PublishProduct
from ikramqa import settings
from django.core import serializers


# Create your views here.

def makeWatermark(request):
    pdf_file = os.path.join('media', "files/original.pdf")
    watermark = os.path.join('media', "files/watermark.pdf")
    merged_file = "merged.pdf"

    input_file = open(pdf_file, 'rb')
    input_pdf = PyPDF2.PdfReader(input_file)

    watermark_file = open(watermark, 'rb')
    watermark_pdf = PyPDF2.PdfReader(watermark_file)

    pdf_page = input_pdf.pages[0]
    watermark_page = watermark_pdf.pages[0]
    watermark_page.merge_page(pdf_page)
    output = PyPDF2.PdfWriter()
    output.add_page(watermark_page)
    merged_file = open(merged_file, 'wb')
    output.write(merged_file)
    merged_file.close()
    watermark_file.close()
    input_file.close()

    return HttpResponse(status=204)


# def writeCert(record,request):
#
def link_callback(uri, rel):
    """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            print(1)
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
            print(path)
        elif uri.startswith(sUrl):
            print(2)
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
            print(path)
        else:
            return uri

    # make sure that file exists
    # print('path', os.path.isfile(path))
    if not os.path.isfile(path):
        raise RuntimeError(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


def render_pdf_view(request, cert_id):
    print('c_id',cert_id)
    obj = Certificate.objects.get(id=cert_id)
    producer_code = ''
    products = obj.product_set.all().order_by('id')
    if obj.template == '1':
        template_path = "certificate/certificate_template.html"
    elif obj.template == '2':
        template_path = "certificate/certificate_template2.html"
    elif obj.template == '4':
        template_path = "certificate/certificate_template4.html"
    elif obj.template == '3':
        template_path = "certificate/certificate_template3.html"
        producer_code = ", ".join(product.rmc_producer_code for product in products)
    # context = extract_request_variables(request)
    context = {'obj': obj, 'products': products, 'producer_code': producer_code}
    # print('rating',products[1].rating)
    response = HttpResponse(content_type="application/pdf")
    # response["Content-Disposition"] = 'attachment; filename="report.pdf"'
    response["Content-Disposition"] = 'inline; filename="draft-%s.pdf"' % obj.certificate_no
    # print('response', response)
    template = get_template(template_path)
    html = template.render(context).encode("utf-8")

    # if request.POST.get("show_html", ""):
    #     response["Content-Type"] = "application/text"
    #     response["Content-Disposition"] = 'attachment; filename="report.txt"'
    #     response.write(html)
    # else:
    #     pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    #     if pisaStatus.err:
    #         return HttpResponse(
    #             f"We had some errors with code {pisaStatus.err} <pre>{html}</pre>"
    #         )
    # create a pdf
    pisaFileObject.getNamedFile = lambda self: self.uri
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback, encoding='utf-8')
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def published_render_pdf_view(request, cert_id):
    obj = PublishCertificate.objects.get(id=cert_id)
    producer_code = ''
    products = obj.publishproduct_set.all().order_by('id')
    if obj.template == '1':
        template_path = "certificate/publish_certificate_template.html"
    elif obj.template == '2':
        template_path = "certificate/publish_certificate_template2.html"
    elif obj.template == '4':
        template_path = "certificate/publish_certificate_template4.html"
    elif obj.template == '3':
        template_path = "certificate/publish_certificate_template3.html"
        producer_code = ", ".join(product.rmc_producer_code for product in products)
    context = {'obj': obj, 'products': products, 'producer_code': producer_code}
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="%s.pdf"' % obj.certificate_no
    template = get_template(template_path)
    html = template.render(context).encode("utf-8")

    # create a pdf
    pisaFileObject.getNamedFile = lambda self: self.uri
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback, encoding='utf-8')
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def generate_qr(request, obj, form=None, change=None):
    # print('OBJ:', obj.brands.all())
    if not obj.qr_image:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=1,
        )
        # super().save_model(request, obj, form, change)
        url = request.build_absolute_uri(obj.get_absolute_url(request))
        qr.add_data(url)
        # print('URL:', obj.get_admin_url(request))
        qr.make(fit=True)
        img = qr.make_image()
        buffer = BytesIO()
        img.save(buffer)
        file_name = f'{obj.certificate_no}-{obj.id}qr.png'
        filebuffer = InMemoryUploadedFile(
            buffer, None, file_name, 'image/png', None, None)
        return obj.qr_image.save(file_name, filebuffer)
    # print('ch',obj.template)
    # super().save_model(request, obj, form, change)


def publish_certificate(request,obj):
    # obj = Certificate.objects.get(id=obj)

    if obj.get_draft_cert() is not None:  # update record function
        publish_obj = obj.get_draft_cert()
        publish_obj.publishproduct_set.all().delete()
        # print('set',publish_obj.publishproduct_set.all())
        text = 'update'
    else:  # new record
        publish_obj = PublishCertificate()
        text = 'new created'
    try:
        with transaction.atomic():
            publish_obj.draft_certificate = obj
            publish_obj.certificate_no = obj.certificate_no
            publish_obj.template = obj.template
            publish_obj.date_original_issue = obj.date_original_issue
            publish_obj.date_renewal = obj.date_renewal
            publish_obj.date_amendment = obj.date_amendment
            publish_obj.expiry_date = obj.expiry_date
            publish_obj.certificate_holder = obj.certificate_holder.name
            publish_obj.holder_address = obj.holder_address.address
            publish_obj.holder_address2 = obj.holder_address.address2
            publish_obj.holder_address3 = obj.holder_address.address3
            publish_obj.holder_city = obj.holder_address.city
            publish_obj.holder_state = obj.holder_address.state
            publish_obj.holder_postcode = obj.holder_address.postcode
            publish_obj.holder_country = obj.holder_address.country
            publish_obj.holder_status = obj.holder_address.status
            publish_obj.product_name = obj.product_name
            publish_obj.plant_identity = obj.plant_identity
            publish_obj.product_standard = obj.product_standard.__str__()
            publish_obj.product_description = obj.product_description

            publish_obj.country = obj.country
            publish_obj.manufacturer = obj.manufacturer.name
            publish_obj.manufacturer_address = obj.manufacturer_address.address
            publish_obj.manufacturer_address2 = obj.manufacturer_address.address2
            publish_obj.manufacturer_address3 = obj.manufacturer_address.address3
            publish_obj.manufacturer_city = obj.manufacturer_address.city
            publish_obj.manufacturer_state = obj.manufacturer_address.state
            publish_obj.manufacturer_postcode = obj.manufacturer_address.postcode
            # publish_obj.manufacturer_country = obj.manufacturer_address.country
            publish_obj.information = obj.information
            publish_obj.status = obj.status

            publish_obj.save()
            generate_qr(request, obj=publish_obj)
            publish_obj.brands.set(obj.brands.all())

            from copy import deepcopy

            fields = [f.name for f in Product._meta.get_fields()]
            fields.remove('productdescription')
            fields.remove('id')
            fields.remove('certificate')

            copied_obj = deepcopy(obj.product_set.all().values(*fields))
            # publish_obj.publishproduct_set.add(draft_certificate=publish_obj, *copied_obj)
            for a in copied_obj:
                productobj = PublishProduct.objects.create(certificate=publish_obj, **a)
                productobj.save()

            return publish_obj.get_admin_url(request)
    except Exception as e:
        # Handle exceptions, and the transaction will be rolled back automatically
        return HttpResponse("there is an error" + str(e))
