from django.urls import path
from .controller_account import login_user, logout_user, create_user

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', create_user, name='register'),
]
