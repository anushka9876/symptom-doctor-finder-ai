from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from .forms import RegisterForm
import json
from django.http import JsonResponse

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
            return redirect('symptoms:home') 
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password'
            })
            
    return render(request, 'accounts/login.html')