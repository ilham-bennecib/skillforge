from django.urls import path
from django.http import JsonResponse
from . import controller_user


urlpatterns = [
    path('all/', controller_user.get_all_users, name='get_all_users'),
    path('user/<int:user_id>/', controller_user.get_one_user, name='get_one_user'),
    path('user/create/', controller_user.create_user, name='create_user'),
    path('user/delete/<int:user_id>/', controller_user.delete_user, name='delete_user'),
    path('user/update/<int:user_id>/', controller_user.update_user, name='update_user'),
]