from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from frontend_settings.models import Feedback, Banner

# Register your models here.
class FeedbackAdmin(admin.ModelAdmin):
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