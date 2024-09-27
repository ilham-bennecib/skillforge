from django.urls import path
from . import controller_structure

urlpatterns = [
    path('all/', controller_structure.get_all_structures, name='get_all_structures'),
    path('structure/<int:structure_id>/', controller_structure.get_one_structure, name='get_one_structure'),
    path('structure/create/', controller_structure.create_structure, name='create_structure'),
    path('structure/delete/<int:structure_id>/', controller_structure.delete_structure, name='delete_structure'),
    path('structure/update/<int:structure_id>/', controller_structure.update_structure, name='update_structure'),
]
