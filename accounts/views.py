from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def register_view(request):
    # GET request → show empty form
    # POST request → validate and save
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():   # checks all fields pass validation
            user = form.save()  # saves User to database

            # Log user in immediately after registering
            login(request, user)
            return redirect('symptoms:home')
    else:
        form = RegisterForm() 

    return render(request, 'accounts/register.html', {'form': form})