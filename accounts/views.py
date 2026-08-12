from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from .forms import RegisterForm
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from symptoms.models import SymptomCheck
from doctors.models import HospitalAppointment

def register_view(request):
    # GET request → show empty form
    # POST request → validate and save
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():   # checks all fields pass validation
            user = form.save()  # saves User to database

            # Log user in immediately after registering
            #login(request, user)
            return redirect('accounts:login')
    else:
        form = RegisterForm() 

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            # Redirect straight to the Symptom Form (assuming its name is 'symptoms:home')
            return redirect('symptoms:form') 
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password'
            })
            
    return render(request, 'accounts/login.html')

@login_required
def dashboard(request):
    user = request.user

    # ── Stat cards ───────────────────────────────────────────
    total_checks   = SymptomCheck.objects.filter(user=user).count()
    total_bookings = HospitalAppointment.objects.filter(user=user).count()

    top_disease = (
        SymptomCheck.objects
        .filter(user=user)
        .values('predicted_disease__name')
        .annotate(count=Count('id'))
        .order_by('-count')
        .first()
    )
    top_disease_name = top_disease['predicted_disease__name'] if top_disease else 'None yet'

    # ── Bar chart — checks per day last 7 days ────────────────
    today = timezone.now().date()
    days  = [today - timedelta(days=i) for i in range(6, -1, -1)]

    daily_counts = []
    for day in days:
        count = SymptomCheck.objects.filter(
            user=user,
            created_at__date=day
        ).count()
        daily_counts.append(count)

    bar_labels = [d.strftime('%a %d') for d in days]
    bar_data   = daily_counts

    # ── Pie chart — top 5 predicted diseases ─────────────────
    disease_counts = (
        SymptomCheck.objects
        .filter(user=user)
        .values('predicted_disease__name')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    pie_labels = [d['predicted_disease__name'] or 'Unknown' for d in disease_counts]
    pie_data   = [d['count'] for d in disease_counts]

    # ── History timeline — last 10 checks ────────────────────
    history = (
        SymptomCheck.objects
        .filter(user=user)
        .select_related('predicted_disease')
        .order_by('-created_at')[:10]
    )

    return render(request, 'accounts/dashboard.html', {
        'total_checks':    total_checks,
        'total_bookings':  total_bookings,
        'top_disease':     top_disease_name,
        'bar_labels':      json.dumps(bar_labels),
        'bar_data':        json.dumps(bar_data),
        'pie_labels':      json.dumps(pie_labels),
        'pie_data':        json.dumps(pie_data),
        'history':         history,
    })