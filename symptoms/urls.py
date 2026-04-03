from django.urls import path
from . import views

app_name = 'symptoms'

urlpatterns = [
    path('',views.symptom_page,  name='home'),
    # HTMX calls this URL as user types — returns partial HTML
    path('search/', views.live_search,   name='search'),
    # Form submit — runs AI prediction
    path('check/',  views.check_symptoms, name='check'),
]