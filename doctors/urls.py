from django.urls import path
from django.http import HttpResponse
from . import views

app_name = 'doctors'

def temp_view(request):
    return HttpResponse("Doctors working 😌")

urlpatterns = [
    path('', temp_view),
    path('book/',    views.book_appointment, name='book'),
    path('success/', views.booking_success,  name='booking_success'),
    path('filter/',  views.filter_doctors,   name='filter'),
]