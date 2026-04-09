from django.db import models
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL

class Symptom(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
    
class Disease(models.Model):
    SEVERITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    name = models.CharField(max_length=100)
    symptoms = models.ManyToManyField(Symptom)

    description = models.TextField(blank=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES,default='low')
    specialist = models.CharField(max_length=100,blank=True)
    is_emergency = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class SymptomCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    symptoms = models.ManyToManyField(Symptom)

    predicted_disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, blank=True)

    raw_text = models.TextField(blank=True)

    confidence_score = models.FloatField(null=True, blank=True)

    is_emergency = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.created_at}"