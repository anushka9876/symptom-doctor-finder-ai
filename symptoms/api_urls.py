from django.urls import path
from .api_views import SymptomCheckAPIView, SymptomHistoryAPIView

urlpatterns = [
    path('check/',   SymptomCheckAPIView.as_view(),   name='api_check'),
    path('history/', SymptomHistoryAPIView.as_view(), name='api_history'),
]