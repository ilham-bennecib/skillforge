from django.urls import path
from . import controller_certificate

urlpatterns = [
    path('all/', controller_certificate.get_all_certificates, name='get_all_certificates'),
    path('certificate/<int:certificate_id>/', controller_certificate.get_one_certificate, name='get_one_certificate'),
    path('certificate/create/', controller_certificate.create_certificate, name='create_certificate'),
    path('certificate/update/<int:certificate_id>/', controller_certificate.update_certificate, name='update_certificate'),
    path('certificate/delete/<int:certificate_id>/', controller_certificate.delete_certificate, name='delete_certificate'),
]
