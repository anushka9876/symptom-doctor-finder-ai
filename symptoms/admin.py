from django.contrib import admin
from .models import Symptom, Disease, SymptomCheck

admin.site.register(Symptom)
admin.site.register(Disease)
admin.site.register(SymptomCheck)