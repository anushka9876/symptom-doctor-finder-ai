# from django.urls import path
# from . import views

# app_name = 'doctors'

# urlpatterns = [
#     path('',            views.doctor_list,  name='list'),
#     # DRF JSON endpoint — Leaflet.js fetches this for map pins
#     path('api/',         views.doctors_api,  name='api'),
#     path('<int:pk>/',    views.doctor_detail,name='detail'),
# ]
from django.urls import path
from django.http import HttpResponse

def temp_view(request):
    return HttpResponse("Doctors working 😌")

urlpatterns = [
    path('', temp_view),
]