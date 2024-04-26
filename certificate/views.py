import os

import PyPDF2
from django.contrib.staticfiles import finders
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

from certificate.models import Certificate
from ikramqa import settings


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
                path=result[0]
        else:
                sUrl = settings.STATIC_URL        # Typically /static/
                sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                mUrl = settings.MEDIA_URL         # Typically /media/
                mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

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


def render_pdf_view(request,cert_id):
    obj=Certificate.objects.get(id=cert_id)
    producer_code =''
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

    context = {'obj': obj, 'products': products, 'producer_code':producer_code}
    response = HttpResponse(content_type="application/pdf")
    # response["Content-Disposition"] = 'attachment; filename="report.pdf"'
    response["Content-Disposition"] = 'inline; filename="%s.pdf"' % obj.certificate_no
    # print('response', response)
    template = get_template(template_path)
    html = template.render(context)

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
        html, dest=response, link_callback=link_callback,encoding='utf-8')
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
