from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import HospitalAppointment
from .overpass import fetch_nearby_hospitals
from symptoms.sms import send_appointment_sms


@login_required
def book_appointment(request):
    if request.method == 'POST':
        appt = HospitalAppointment.objects.create(
            user=request.user,
            hospital_name=request.POST.get('hospital_name', ''),
            hospital_osm=request.POST.get('hospital_id', ''),
            specialty=request.POST.get('specialty', ''),
            latitude=float(request.POST.get('latitude', 0)),
            longitude=float(request.POST.get('longitude', 0)),
            address=request.POST.get('address', ''),
        )
        # Send SMS if user has phone number
        send_appointment_sms(
            to_phone=request.user.phone,
            hospital_name=appt.hospital_name,
            specialty=appt.specialty,
        )
        return redirect('doctors:booking_success')
    return redirect('symptoms:form')


@login_required
def booking_success(request):
    return render(request, 'doctors/booking_success.html')


@login_required
def filter_doctors(request):
    specialty = request.GET.get('specialty', '')
    lat       = float(request.GET.get('lat', 0))
    lng       = float(request.GET.get('lng', 0))
    doctors   = fetch_nearby_hospitals(lat, lng, disease=specialty)
    return render(request, 'partials/doctor_cards.html', {'doctors': doctors})