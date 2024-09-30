from django.urls import path
from . import controller_cfaemployee_contact

urlpatterns = [
    path('all/', controller_cfaemployee_contact.get_all_exchanges, name='get_all_exchanges'),
    path('exchange/<int:exchange_id>/', controller_cfaemployee_contact.get_one_exchange, name='get_one_exchange'),
    path('exchange/create/', controller_cfaemployee_contact.create_exchange, name='create_exchange'),
    path('exchange/update/<int:exchange_id>/', controller_cfaemployee_contact.update_exchange, name='update_exchange'),
    path('exchange/delete/<int:exchange_id>/', controller_cfaemployee_contact.delete_exchange, name='delete_exchange'),
]
