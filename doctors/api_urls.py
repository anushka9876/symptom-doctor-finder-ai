from django.urls import path
from .api_views import NearbyDoctorsAPIView

urlpatterns = [
    path('nearby/', NearbyDoctorsAPIView.as_view(), name='api_nearby'),
]