from frontend_settings.views import index, services, about, credential, organisation, vision_mission, \
    directory, guide, company_profile, product_certification_guide, consignment, testing, inspection, general_info, \
    feedback, product, product_detail, download_feedback_pdf
from django.urls import path


urlpatterns = [
    path('', index, name='home'),
    # path('services', services, name='service'),
    path('services/<str:name>/', services, name='service'),
    path('about/', about, name='about'),
    path('credential/', credential, name='credential'),
    path('organisation/', organisation, name='organisation'),
    path('visionmission/', vision_mission, name='vision_mission'),
    path('directory/', directory, name='directory'),
    path('guide/', guide, name='guide'),
    path('profile/', company_profile, name='company_profile'),
    path('product/guide/', product_certification_guide, name='product_certification_guide'),
    path('consignment/', consignment, name='consignment'),
    path('testing/', testing, name='testing'),
    path('inspection/', inspection, name='inspection'),
    path('general_info/', general_info, name='general_info'),
    path('feedback/',feedback, name="feedback"),
    path('producttable/', product.as_view(), name='producttable'),
    path('product/<int:obj_id>/detail/', product_detail, name='product_detail'),
    path('download_feedback/<int:feedback_id>/', download_feedback_pdf, name='feedback_download')
]