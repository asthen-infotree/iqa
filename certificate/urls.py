from .views import makeWatermark, render_pdf_view, publish_certificate, published_render_pdf_view
from django.urls import path

urlpatterns = [
    path('generate/', makeWatermark, name='generate'),
    path('download/<int:cert_id>', render_pdf_view, name='download'),
    path('download/publish/<int:cert_id>', published_render_pdf_view, name='publish_download'),
    path('publish/', publish_certificate, name='publishcert')
]
