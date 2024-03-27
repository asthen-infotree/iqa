from .views import makeWatermark, render_pdf_view
from django.urls import path

urlpatterns = [
    path('generate/', makeWatermark, name='generate'),
    path('download/<int:cert_id>', render_pdf_view, name='download')
]
