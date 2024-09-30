from django.urls import path
from . import controller_session

urlpatterns = [
    path('all/', controller_session.get_all_sessions, name='get_all_sessions'),
    path('session/<int:session_id>/', controller_session.get_one_session, name='get_one_session'),
    path('session/create/', controller_session.create_session, name='create_session'),
    path('session/update/<int:session_id>/', controller_session.update_session, name='update_session'),
    path('session/delete/<int:session_id>/', controller_session.delete_session, name='delete_session'),
]
