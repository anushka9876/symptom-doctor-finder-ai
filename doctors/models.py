from django.db import models
from django.conf import settings
from symptoms.models import SymptomCheck

User = settings.AUTH_USER_MODEL


# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=100,blank=True)
    specialty = models.CharField(max_length=100,blank=True)

    phone = models.CharField(max_length=15,blank=True)
    hospital = models.CharField(max_length=150,blank=True)

    city = models.CharField(max_length=100,blank=True)

    location = models.CharField(max_length=255,blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,  null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,  null=True, blank=True)

    fee = models.IntegerField(default=0)

    rating = models.FloatField(default=0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    symptom_check = models.ForeignKey(SymptomCheck, on_delete=models.SET_NULL, null=True,blank=True)

    date = models.DateTimeField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    sms_sent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.doctor}"

