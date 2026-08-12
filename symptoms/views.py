from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Symptom, SymptomCheck, Disease
from doctors.overpass import fetch_nearby_hospitals
from symptoms.ml.spacy_extractor import extract_symptoms
from symptoms.ml.predictor import predict_disease
from symptoms.ml.emergency import check_emergency

SPECIALTIES = [
    "General Physician", "Dermatologist", "Neurologist",
    "Cardiologist", "Pulmonologist", "Orthopedic",
    "Gastroenterologist", "ENT Specialist",
]

#  PAGE 1 — symptom form (GET only, just renders)
@login_required
def symptom_form(request):
    return render(request, 'symptoms/symptom_form.html')


#  Receives symptom form POST → saves to session → location page
@login_required
def check_symptoms(request):
    if request.method == 'POST':
        text     = request.POST.get('symptoms_text', '').strip()
        selected = request.POST.get('selected_symptoms', '').strip()

        if selected and text:
            combined = selected.replace(',', ', ') + '. ' + text
        elif selected:
            combined = selected.replace(',', ', ')
        else:
            combined = text

        if combined:
            request.session['symptoms_text'] = combined
            return redirect('symptoms:location')

    return redirect('symptoms:form')


#  PAGE 2 — location picker (GET only, just renders)
@login_required
def location_page(request):
    if 'symptoms_text' not in request.session:
        return redirect('symptoms:form')
    return render(request, 'symptoms/location.html')


#  Receives lat/lng POST → NLP → Overpass → results page
@login_required
def run_check(request):
    if request.method != 'POST':
        return redirect('symptoms:form')

    try:
        lat = float(request.POST['lat'])
        lng = float(request.POST['lng'])
    except (KeyError, ValueError):
        return redirect('symptoms:location')

    text = request.session.pop('symptoms_text', '')
    if not text:
        return redirect('symptoms:form')

    # 1. Extract symptoms from free text using spaCy
    symptoms_found = extract_symptoms(text)

    # 2. Get top 3 disease predictions
    top3           = predict_disease(symptoms_found)
    top_disease    = top3[0]['disease']
    top_confidence = top3[0]['confidence']

    # 3. Check for emergency symptoms
    is_emergency, emergency_msg = check_emergency(symptoms_found)

    # 4. Save to DB
    disease_obj, _ = Disease.objects.get_or_create(name=top_disease)
    SymptomCheck.objects.create(
        user=request.user,
        raw_text=text,
        predicted_disease=disease_obj,
        confidence_score=top_confidence,
        is_emergency=is_emergency,
    )

    # 5. Fetch real hospitals from OpenStreetMap via Overpass
    nearby = fetch_nearby_hospitals(lat, lng, disease=top_disease)
    nearby = [{
    'id':          d['id'],
    'name':        d['name'],
    'specialty':   d['specialty'],
    'fee':         d['fee'],
    'latitude':    d['latitude'],
    'longitude':   d['longitude'],
    'distance_km': d['distance_km'],
    'address':     d['address'],
} for d in nearby[:10]]

    # 6. Save to session → redirect to results
    request.session['results'] = {
        'top3':          top3,
        'text':          text,
        'symptoms':      symptoms_found,
        'is_emergency':  is_emergency,
        'emergency_msg': emergency_msg,
    }
    request.session['nearby_doctors'] = nearby
    request.session['user_lat']       = lat
    request.session['user_lng']       = lng

    return redirect('symptoms:results')


#  PAGE 3 — results (GET only, reads + clears session)
@login_required
def results_page(request):
    results = request.session.pop('results', None)
    if not results:
        return redirect('symptoms:form')

    nearby = request.session.pop('nearby_doctors', [])
    lat    = request.session.pop('user_lat', 0)
    lng    = request.session.pop('user_lng', 0)

    return render(request, 'symptoms/results.html', {
        'results':        results,
        'nearby_doctors': nearby,
        'user_lat':       lat,
        'user_lng':       lng,
        'specialties':    SPECIALTIES,
    })


#  HTMX live search 
def live_search(request):
    q = request.GET.get('q', '').strip()
    results = Symptom.objects.filter(name__icontains=q)[:5] if len(q) >= 2 else []
    return render(request, 'partials/symptom_suggestions.html', {'results': results})