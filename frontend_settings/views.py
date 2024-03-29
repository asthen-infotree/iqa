from datatableview import Datatable, columns
from django.contrib import messages
# from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from certificate.models import Certificate
from frontend_settings.forms import FeedbackForm
from frontend_settings.models import Banner
from datatableview.views import DatatableView


# Create your views here.


def index(request):
    banners = Banner.objects.all()

    return render(request, 'index.html', {'banners': banners})


def services(request, name=None):
    # if request.method == "POST":
        # print(name)
        # if services == 'product-certification':
        #
        # elif services == 'ready-mixed':
        #
        # elif services == 'inspection':
        #
        # elif services == 'laboratory-test':
        #
        # elif services == 'laboratory-test':
        #
        # elif services == 'sample':
        #
        # elif services == 'government':

    return render(request, 'certificate/services.html', {'name': name})


def about(request):
    return render(request, 'certificate/about.html')


def organisation(request):
    return render(request, 'certificate/organisation.html')


def credential(request):
    return render(request, 'certificate/credential.html')


def vision_mission(request):
    return render(request, 'certificate/vision_mission.html')


def directory(request):
    return render(request, 'certificate/directory.html')


def guide(request):
    return render(request, 'certificate/guides.html')


def company_profile(request):
    return render(request, 'certificate/company.html')


def product_certification_guide(request):
    return render(request, 'certificate/product_certification_guide.html')


def consignment(request):
    return render(request, 'certificate/consignment.html')


def testing(request):
    return render(request, 'certificate/testing.html')


def inspection(request):
    return render(request, 'certificate/inspection_forms.html')


def general_info(request):
    return render(request, 'certificate/general_info.html')


def feedback(request):
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            new_feedback = form.save(commit=False)
            # new_feedback.name = form.cleaned_data['name']
            # new_feedback.email = form.cleaned_data['email']
            # new_feedback.phone_no = form.cleaned_data['phone_no']
            # new_feedback.subject = form.cleaned_data['subject']
            # new_feedback.message = form.cleaned_data['message']
            new_feedback.save()
            messages.success(request, 'Feedback submitted successfully')
            return HttpResponseRedirect('/frontend/feedback/')
    else:
        form = FeedbackForm()

    return render(request, 'certificate/feedback.html', context={'form': form})


from datatableview.views.legacy import LegacyDatatableView


class product(DatatableView):
    model = Certificate

    class datatable_class(Datatable):
        status = columns.TextColumn("Status", sources=None, processor="get_status_display")
        details = columns.TextColumn("Details", sources=None, processor="make_button")
        certificate_holder=columns.TextColumn("Certificate Holder", sources=['certificate_holder__name'])

        class Meta:
            columns = [
                        'certificate_no',
                        'certificate_holder',
                        'product_name',
                        'product_standard',
                        'country',
                        'expiry_date',
                        'status',
                        'details']

        def get_status_display(self, instance, **kwargs):
            return instance.get_status_display()

        def get_holder_name(self, instance, **kwargs):
            return instance.certificate_holder.name

        def make_button(self,instance, **kwargs):
            # print(Site.objects.get_current().domain)
            url = "/product/{}/detail/".format(instance.id)
            path=reverse('product_detail', args=[instance.id])
            return mark_safe(f"""<a href=%s target="_blank" rel="noopener noreferrer">View</a>""" % path)
    # datatable_options = {
    #     'columns':['certificate_holder',
    #                'certificate_no',
    #                'product_name',
    #                'product_standard',
    #                'country',
    #                'expiry_date',
    #                'status']
    # }
    template_name = "certificate/producttable.html"


def product_detail(request, obj_id):
    product=Certificate.objects.get(id=obj_id)
    product_descriptions = product.product_set.all()
    template='certificate/product_detail.html'
    if product.template == '3':
        template='certificate/product_detail_rmc.html'

    return render(request, template, context={'product': product, 'product_descriptions': product_descriptions})
