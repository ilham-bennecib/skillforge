from django.urls import path
from . import controller_cfaEmployee

urlpatterns = [
    path('all/', controller_cfaEmployee.get_all_cfaEmployees, name='get_all_cfaEmployees'),
    path('employee/<int:employee_id>/', controller_cfaEmployee.get_one_cfaEmployee, name='get_one_cfaEmployee'),
    path('employee/create/from_user<int:user_id>/', controller_cfaEmployee.create_cfaEmployee, name='create_cfaEmployee'),
    path('employee/update/<int:employee_id>/', controller_cfaEmployee.update_cfaEmployee, name='update_cfaEmployee'),
    path('employee/delete/<int:employee_id>/', controller_cfaEmployee.delete_cfaEmployee, name='delete_cfaEmployee'),
]
