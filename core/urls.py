"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path,include
from django.shortcuts import redirect
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('',        lambda request: redirect('symptoms:form')),  
    path('admin/',  admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('doctors/',  include('doctors.urls',  namespace='doctors')),
    path('symptoms/', include('symptoms.urls', namespace='symptoms')),


    # API routes
    path('api/auth/token/', obtain_auth_token),
    path('api/doctors/',   include('doctors.api_urls')),
    path('api/symptoms/',  include('symptoms.api_urls')),
]
