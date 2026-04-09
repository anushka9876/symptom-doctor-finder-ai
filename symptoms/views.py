from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import math
from doctors.models import Doctor
from .models import Symptom, SymptomCheck


# ─────────────────────────────────────────────────────────────
#  HELPER — haversine distance in km
# ─────────────────────────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    a = (math.sin((lat2 - lat1) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2)
         * math.sin((lon2 - lon1) / 2) ** 2)
    return round(R * 2 * math.asin(math.sqrt(a)), 1)


# ─────────────────────────────────────────────────────────────
#  PAGE 1 — symptom form (GET only, just renders)
# ─────────────────────────────────────────────────────────────
@login_required
def symptom_form(request):
    return render(request, 'symptoms/symptom_form.html')


# ─────────────────────────────────────────────────────────────
#  Receives symptom form POST → saves to session → location page
# ─────────────────────────────────────────────────────────────
@login_required
def check_symptoms(request):
    if request.method == 'POST':
        text = request.POST.get('symptoms_text', '').strip()
        if text:
            request.session['symptoms_text'] = text
            return redirect('symptoms:location')
    return redirect('symptoms:form')


# ─────────────────────────────────────────────────────────────
#  PAGE 2 — location picker (GET only, just renders)
# ─────────────────────────────────────────────────────────────
@login_required
def location_page(request):
    if 'symptoms_text' not in request.session:
        return redirect('symptoms:form')   # guard: can't skip step 1
    return render(request, 'symptoms/location.html')


# ─────────────────────────────────────────────────────────────
#  Receives lat/lng POST → NLP → haversine → results page
# ─────────────────────────────────────────────────────────────
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

    # ── NLP goes here (Week 3) ────────────────────────────────
    # disease, confidence = predict_disease(text)
    # Placeholder until Week 3:
    disease    = "Viral Fever"
    confidence = 87

    # ── Save to DB ────────────────────────────────────────────
    SymptomCheck.objects.create(
        user=request.user,
        raw_text=text,
        predicted_disease=disease,
        confidence=confidence,
    )

    # ── Nearby doctors ────────────────────────────────────────
    nearby = []
    for doc in Doctor.objects.all():
        dist = haversine(lat, lng, float(doc.latitude), float(doc.longitude))
        nearby.append({
            'id':          doc.id,
            'name':        doc.name,
            'specialty':   doc.specialty,
            'fee':         str(doc.fee),
            'latitude':    float(doc.latitude),
            'longitude':   float(doc.longitude),
            'distance_km': dist,
        })
    nearby.sort(key=lambda x: x['distance_km'])

    # ── Stash in session → redirect to results ────────────────
    request.session['results']        = {'disease': disease, 'confidence': confidence, 'text': text}
    request.session['nearby_doctors'] = nearby[:20]
    request.session['user_lat']       = lat
    request.session['user_lng']       = lng

    return redirect('symptoms:results')


# ─────────────────────────────────────────────────────────────
#  PAGE 3 — results (GET only, reads + clears session)
# ─────────────────────────────────────────────────────────────
@login_required
def results_page(request):
    results = request.session.pop('results', None)
    if not results:
        return redirect('symptoms:form')   # guard: can't skip step 2

    nearby  = request.session.pop('nearby_doctors', [])
    lat     = request.session.pop('user_lat', 0)
    lng     = request.session.pop('user_lng', 0)

    return render(request, 'symptoms/results.html', {
        'results':        results,
        'nearby_doctors': nearby,
        'user_lat':       lat,
        'user_lng':       lng,
    })


# ─────────────────────────────────────────────────────────────
#  HTMX live search (unchanged)
# ─────────────────────────────────────────────────────────────
def live_search(request):
    q = request.GET.get('q', '').strip()
    results = Symptom.objects.filter(name__icontains=q)[:8] if len(q) >= 2 else []
    return render(request, 'partials/symptom_suggestions.html', {'results': results})