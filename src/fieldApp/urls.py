from django.urls import path
from . import controller_field

urlpatterns = [
    path('all/', controller_field.get_all_fields, name='get_all_fields'),
    path('field/<int:field_id>/', controller_field.get_one_field, name='get_one_field'),
    path('field/create/', controller_field.create_field, name='create_field'),
    path('field/update/<int:field_id>/', controller_field.update_field, name='update_field'),
    path('field/delete/<int:field_id>/', controller_field.delete_field, name='delete_field'),
]
