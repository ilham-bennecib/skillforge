from django.urls import path
from . import controller_event

urlpatterns = [
    path('all/', controller_event.get_all_events, name='get_all_events'),
    path('event/<int:event_id>/', controller_event.get_one_event, name='get_one_event'),
    path('event/create/', controller_event.create_event, name='create_event'),
    path('event/update/<int:event_id>/', controller_event.update_event, name='update_event'),
    path('event/delete/<int:event_id>/', controller_event.delete_event, name='delete_event'),
]
