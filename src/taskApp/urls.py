from django.urls import path
from . import controller_task

urlpatterns = [
    path('all/', controller_task.get_all_tasks, name='get_all_tasks'),
    path('task/<int:task_id>/', controller_task.get_one_task, name='get_one_task'),
    path('task/create/', controller_task.create_task, name='create_task'),
    path('task/update/<int:task_id>/', controller_task.update_task, name='update_task'),
    path('task/delete/<int:task_id>/', controller_task.delete_task, name='delete_task'),
]
