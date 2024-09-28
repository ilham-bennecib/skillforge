from django.urls import path
from . import controller_company


urlpatterns = [
    path('all/', controller_company.get_all_companies, name='get_all_companies'),
    path('company/<int:company_id>/', controller_company.get_one_company, name='get_one_company'),
    path('company/create/from_structure<int:structure_id>/', controller_company.create_company, name='create_company'),
    path('company/delete/<int:company_id>/', controller_company.delete_company, name='delete_company'),
    path('company/update/<int:company_id>/', controller_company.update_company),
 ]