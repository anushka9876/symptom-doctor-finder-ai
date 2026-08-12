import requests, math, random, time

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]

DISEASE_SPECIALTY_MAP = {
    "Dengue":            "General Physician",
    "Malaria":           "General Physician",
    "Typhoid":           "General Physician",
    "Viral Fever":       "General Physician",
    "Fungal infection":  "Dermatologist",
    "Chicken pox":       "Dermatologist",
    "Migraine":          "Neurologist",
    "Paralysis":         "Neurologist",
    "Heart attack":      "Cardiologist",
    "Bronchial Asthma":  "Pulmonologist",
    "Pneumonia":         "Pulmonologist",
    "Diabetes":          "Diabetologist",
    "Arthritis":         "Orthopedic",
    "Allergy":           "ENT Specialist",
    "Jaundice":          "Gastroenterologist",
}


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    a = (math.sin((lat2-lat1)/2)**2
         + math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2)
    return round(R * 2 * math.asin(math.sqrt(a)), 1)


def fetch_nearby_hospitals(lat, lng, disease="", radius=0.05):
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="hospital"]({lat-radius},{lng-radius},{lat+radius},{lng+radius});
      node["amenity"="clinic"]({lat-radius},{lng-radius},{lat+radius},{lng+radius});
      node["amenity"="doctors"]({lat-radius},{lng-radius},{lat+radius},{lng+radius});
      way["amenity"="hospital"]({lat-radius},{lng-radius},{lat+radius},{lng+radius});
      way["amenity"="clinic"]({lat-radius},{lng-radius},{lat+radius},{lng+radius});
    );
    out center;
    """

    data = None
    for url in OVERPASS_URLS:
        try:
            resp = requests.get(
                url,
                params={"data": query},
                timeout=20,
                headers={"User-Agent": "MediCheck/1.0"}
            )
            if resp.status_code == 200 and resp.text.strip():
                data = resp.json()
                break
        except Exception as e:
            print(f"Overpass error ({url}): {e}")
            time.sleep(1)
            continue

    if not data:
        return []

    specialty = DISEASE_SPECIALTY_MAP.get(disease, "General Physician")
    results = []

    for el in data.get('elements', []):
        if el['type'] == 'node':
            elat, elng = el['lat'], el['lon']
        else:
            center = el.get('center', {})
            elat = center.get('lat')
            elng = center.get('lon')
            if not elat:
                continue

        tags = el.get('tags', {})
        name = (tags.get('name') or tags.get('name:en') or '').strip()
        if not name:
            continue
        dist = haversine(lat, lng, elat, elng)

        results.append({
            'id':          str(el.get('id', '')),
            'name':        name,
            'specialty':   specialty,
            'fee':         f"₹{random.randint(3,8)*100}",
            'latitude':    elat,
            'longitude':   elng,
            'distance_km': dist,
            'address':     tags.get('addr:street') or tags.get('addr:full') or "See on map",
            'phone':       tags.get('phone') or tags.get('contact:phone') or "",
        })

    results.sort(key=lambda x: x['distance_km'])
    return results[:20]