from django.urls import path
from . import controller_training

urlpatterns = [
    path('all/', controller_training.get_all_trainings, name='get_all_trainings'),
    path('training/<int:training_id>/', controller_training.get_one_training, name='get_one_training'),
    path('training/create/', controller_training.create_training, name='create_training'),
    path('training/update/<int:training_id>/', controller_training.update_training, name='update_training'),
    path('training/delete/<int:training_id>/', controller_training.delete_training, name='delete_training'),
]
