from django.urls import path
from django.http import HttpResponse

app_name = 'doctors'

def temp_view(request):
    return HttpResponse("Doctors working 😌")

urlpatterns = [
    path('', temp_view),
]