"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('userApp.urls')),
    path('api/structures/', include('structureApp.urls')),
    path('api/companies/', include('companyApp.urls')),
    path('api/courses/', include('courseApp.urls')),
    path('api/candidates/', include('candidateApp.urls')),
    path('api/students/', include('studentApp.urls')),
    path('api/trainings/', include('trainingApp.urls')),
    path('api/roles/', include('roleApp.urls')),
    path('api/fields/', include('fieldApp.urls')),
    path('api/contacts/', include('contactApp.urls')),
    path('api/cfaEmployees/', include('cfaEmployeeApp.urls')),
    path('api/sessions/', include('sessionApp.urls')),
    # path('api/certificates/', include('certificateApp.urls')),
    path('api/tasks/', include('taskApp.urls')),
    path('api/news/', include('newsApp.urls')),
]
