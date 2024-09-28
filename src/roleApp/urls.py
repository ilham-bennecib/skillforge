from django.urls import path
from . import controller_role

urlpatterns = [
    path('all/', controller_role.get_all_roles, name='get_all_roles'),
    path('role/<int:role_id>/', controller_role.get_one_role, name='get_one_role'),
    path('role/create/', controller_role.create_role, name='create_role'),
    path('role/update/<int:role_id>/', controller_role.update_role, name='update_role'),
    path('role/delete/<int:role_id>/', controller_role.delete_role, name='delete_role'),
]
