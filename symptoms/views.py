from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Symptom, SymptomCheck

# @login_required redirects to /accounts/login/ if not logged in
def symptom_page(request):
    # Load all 132 symptoms for the checkbox list
    all_symptoms = Symptom.objects.all().order_by('name')
    return render(request, 'symptoms/symptom_form.html', {
        'symptoms': all_symptoms
    })


@login_required
def live_search(request):
    # ← HTMX calls this every time user types
    # It returns a small HTML snippet, NOT a full page
    query = request.GET.get('q', '').strip()

    if len(query) < 2:
        # Don't search for single characters — return empty
        return HttpResponse('')

    # Filter symptoms that contain the typed text
    results = Symptom.objects.filter(
        name__icontains=query  # icontains = case-insensitive contains
    )[:8]                    # limit to 8 suggestions

    # Return ONLY the suggestions partial — HTMX swaps this in
    return render(request,
        'partials/symptom_suggestions.html',
        {'symptoms': results})


@login_required
def check_symptoms(request):
    # Week 3 will fill this in with AI logic
    # For now, just confirm it receives the POST
    if request.method == 'POST':
        text = request.POST.get('symptoms_text', '')
        return HttpResponse(f'Received: {text} — AI coming in Week 3')
    return render(request, 'symptoms/symptom_form.html')