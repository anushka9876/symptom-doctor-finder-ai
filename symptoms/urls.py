from django.urls import path
from . import views

app_name = 'symptoms'

urlpatterns = [
    path('',           views.symptom_form,   name='form'),
    path('check/',     views.check_symptoms, name='check'),
    path('location/',  views.location_page,  name='location'),
    path('run/',       views.run_check,      name='run'),
    path('results/',   views.results_page,   name='results'),
    path('search/',    views.live_search,    name='search'),
]