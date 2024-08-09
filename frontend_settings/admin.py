from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from frontend_settings.models import Feedback, Banner

# Register your models here.
class FeedbackAdmin(admin.ModelAdmin):

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}

        if object_id != None:
            extra_context = dict(show_save=False, show_save_and_continue=False, show_delete=False,
                                 show_save_and_add_another=False)
            extra_context['custom_button_feedback'] = True  # Here
        return super().changeform_view(request, object_id, form_url, extra_context)
    def response_change(self, request, obj):  # Here
        if "_custom_button" in request.POST:
            # return render_pdf_view(request, obj)
            return redirect(reverse('feedback_download', kwargs={'feedback_id': obj.id}))

            # Do something
            # return super().response_change(request, obj)
            # return HttpResponseRedirect(".")
        else:
            # print('123123')
            # Do something
            return super().response_change(request, obj)

admin.site.register(Feedback, FeedbackAdmin)



admin.site.register(Banner)