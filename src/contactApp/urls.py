from django.urls import path
from . import controller_contact

urlpatterns = [
    path('all/', controller_contact.get_all_contacts, name='get_all_contacts'),
    path('contact/<int:contact_id>/', controller_contact.get_one_contact, name='get_one_contact'),
    path('contact/create/from_user<int:user_id>/', controller_contact.create_contact, name='create_contact'),
    path('contact/update/<int:contact_id>/', controller_contact.update_contact, name='update_contact'),
    path('contact/delete/<int:contact_id>/', controller_contact.delete_contact, name='delete_contact'),
]
