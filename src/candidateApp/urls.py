from django.urls import path
from . import controller_candidate


urlpatterns = [
    # path('all/', controller_candidate.get_all_users, name='get_all_users'),
    # path('user/<int:user_id>/', controller_candidate.get_one_user, name='get_one_user'),
    path('candidate/create/<int:user_id>/', controller_candidate.create_candidate, name='create_candidate'),
#     path('user/delete/<int:user_id>/', controller_candidate.delete_user, name='delete_user'),
#     path('user/update/<int:user_id>/', controller_candidate.update_user, name='update_user'),
 ]