from django.urls import path
from . import controller_candidate


urlpatterns = [
    # path('all/', controller_candidate.get_all_users, name='get_all_users'),
    path('candidate/<int:candidate_id>/', controller_candidate.get_one_candidate, name='get_one_candidate'),
    path('candidate/create/<int:user_id>/', controller_candidate.create_candidate, name='create_candidate'),
    #path('candidate/delete/<int:user_id>/', controller_candidate.delete_candidate, name='delete_candidate'),
#     path('user/update/<int:user_id>/', controller_candidate.update_user, name='update_user'),
 ]